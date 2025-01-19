import requests
import os
import random
import string

def download_image(url, image_name=None, folder="photos"):
    try:
        
        if not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.isdir('processed_photos'):
            os.makedirs('processed_photos')

        if not image_name:
            image_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        if not image_name.endswith(".jpg"):
            image_name += ".jpg"

        path = os.path.join(folder, image_name)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Imagem baixada com sucesso em {path}")
    
    except requests.exceptions.HTTPError as e:
        print(f"Erro ao baixar a imagem: {e}")