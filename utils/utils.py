import requests
import os
from io import BytesIO


def download_image_temp(url, image_name):
    try:
        # Gerar um nome aleatório para a imagem
        image_name = image_name

        # Fazer a requisição da imagem
        response = requests.get(url, stream=True)
        response.raise_for_status()

        processed_photos_dir = "processed_photos"
        if not os.path.exists(processed_photos_dir):
            os.makedirs(processed_photos_dir)

        image_path = os.path.join(processed_photos_dir, image_name)

        # Escrever a imagem no arquivo temporário
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Imagem baixada temporariamente em {image_path}")

        return image_path  # Retorna o caminho do arquivo temporário

    except requests.exceptions.HTTPError as e:
        print(f"Erro ao baixar a imagem: {e}")
        return None
    
def delete_temp_file(file_path):
    try:
        os.remove(file_path)
        print(f"Arquivo temporário {file_path} removido com sucesso")
    except Exception as e:
        print(f"Erro ao remover o arquivo temporário {file_path}: {e}")