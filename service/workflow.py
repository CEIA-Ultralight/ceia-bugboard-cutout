from connection.connection import SupabaseConnection, patch
from service.utils.utils import download_image, delete_file, verificar_rotacionar
import service.scan as scan
import logging

class ImageProcessing:
    def __init__(self):
        self.image_queue = []
        self.processing = False
        self.bucket = SupabaseConnection()
    
    def process_next_image(self, image_name:str):
            
        if not self.image_queue or self.processing:
            return
        
        self.processing = True

        try:
            image_data = self.image_queue.pop(0)

            image_path = download_image(image_data["photo_url"], image_name)

            processed_path = scan.main(["--image", f"{image_path}"])

            verificar_rotacionar(processed_path)

            data = self.bucket.upload_file_to_supabase(image_name, processed_path)

            patch(image_data["id"], data["url"])

            delete_file(processed_path)
            delete_file(image_path)

        except Exception as e:
            logging.error(f"Erro durante o processamento: {e}")

        finally:
            self.processing = False