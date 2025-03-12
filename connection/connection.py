import requests
import logging

class SupabaseConnection:
    """
    Classe para gerenciar a conexão e upload de arquivos para o Supabase Storage.
    """

    def __init__(self):
        """
        Inicializa a conexão com os parâmetros fornecidos.

        :param supabase_url: URL do Supabase
        :param bucket_name: Nome do bucket no Supabase
        :param file_key: Caminho onde será salvo no Supabase
        :param file_path: Caminho do arquivo local
        :param jwt_token: JWT Token para autenticação
        """
        self.supabase_url = "https://tfiswpjimraodvnjbybx.supabase.co"
        self.bucket_name = "boards"
        self.jwt_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmaXN3cGppbXJhb2R2bmpieWJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMxNTIwNTUsImV4cCI6MjA0ODcyODA1NX0.I8UX36hAphowNk85VcL6iYh4TIBwsE0r3wgreTEDaII"
        self.headers = {
            "Authorization": f"{self.jwt_token}",
            "Content-Type": "image/jpeg"
        }

    def upload_file_to_supabase(self, image_name, image_path):
        """
        Faz o upload do arquivo para o Supabase Storage.
        """
        upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/images/{image_name}"

        try:
            with open(image_path, "rb") as file:
                response = requests.put(upload_url, headers=self.headers, data=file)

            # Verificar resposta
            if response.status_code == 200:
                logging.info(f"Upload bem-sucedido! Arquivo salvo como: images/{image_name}")
                response_json = response.json()
                response_json.update({"url": f"{upload_url}"})
                return response_json
            else:
                logging.error(f"Erro no upload: {response.status_code} - {response.text}")

        except Exception as e:
            logging.error("Erro ao enviar a imagem:", e)
            
def patch(id, photo_url):
    
    url = f"https://tfiswpjimraodvnjbybx.supabase.co/rest/v1/Boards?id=eq.{id}"
    headers = { "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmaXN3cGppbXJhb2R2bmpieWJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMxNTIwNTUsImV4cCI6MjA0ODcyODA1NX0.I8UX36hAphowNk85VcL6iYh4TIBwsE0r3wgreTEDaII",
            "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmaXN3cGppbXJhb2R2bmpieWJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMxNTIwNTUsImV4cCI6MjA0ODcyODA1NX0.I8UX36hAphowNk85VcL6iYh4TIBwsE0r3wgreTEDaII",
            "Prefer": "return=representation"
    }

    data = {
        "trimmed_photo_url": photo_url
    }

    
    try:
        response = requests.patch(url, json=data, headers=headers)

        if response.status_code in [200, 204]:
            logging.info("Atualização no banco feita com sucesso!")
        else:
            logging.error(f"Erro ao atualizar: {response.status_code}")
            logging.error(response.text)  # Exibir a resposta do servidor
    except Exception as e:
        logging.error(f"Erro durante a requisição PATCH: {e}")
