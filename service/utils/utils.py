import requests
import os
import string
import random
from PIL import Image
import cv2
import easyocr
import numpy as np
import logging

def download_image(url, image_name):
    try:
        # Gerar um nome aleatório para a imagem
        image_name = image_name

        # Fazer a requisição da imagem
        response = requests.get(url, stream=True)
        response.raise_for_status()

        photos_dir = "download_phots"
        if not os.path.exists(photos_dir):
            os.makedirs(photos_dir)

        processed_photos_dir = "processed_photos"
        if not os.path.exists(processed_photos_dir):
            os.makedirs(processed_photos_dir)

        image_path = os.path.join(photos_dir, image_name)

        # Escrever a imagem no arquivo temporário
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logging.info(f"Imagem baixada temporariamente em {image_path}")

        return image_path  # Retorna o caminho do arquivo temporário

    except requests.exceptions.HTTPError as e:
        logging.error(f"Erro ao baixar a imagem: {e}")
        return None
    
def delete_file(file_path):
    try:
        os.remove(file_path)
        logging.info(f"Arquivo temporário {file_path} removido com sucesso")
    except Exception as e:
        print(f"Erro ao remover o arquivo temporário {file_path}: {e}")

def generate_random_name(length=10):
    """Gera um nome aleatório para a imagem"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length)) + ".jpg"

def verificar_rotacionar(image_path):
    
    try:
        with Image.open(image_path) as img:
            largura, altura = img.size

            if largura > altura:
                return 'Horizontal'
            elif largura < altura:
                
                img_rotacionada = img.rotate(-90, expand=True)
                
                img_rotacionada.save(image_path)
            
    except Exception as e:
        logging.error(f'Erro ao carregar a imagem {e}')