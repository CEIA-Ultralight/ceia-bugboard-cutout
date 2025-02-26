from connection.supabase_connection import SupabaseConnection
import utils.utils as utils
import scan
import connection.patch as patch

# Baixar a imagem localmente
def workImage(photo_url, image_name, image_id):

    image_path = utils.download_image_temp(photo_url, image_name)

    processed_path = scan.main(["--image", f"{image_path}"])

    utils.delete_temp_file(image_path)

    bucket = SupabaseConnection()

    data = bucket.upload_file_to_supabase(image_name, processed_path)

    patch.patch(image_id, data["url"])

    utils.delete_temp_file(processed_path)