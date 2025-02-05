from connection.rds_connection import RDSConnection
from connection.s3_connection import S3Connection
import utils.utils as utils
import random
import string
import scan

# Baixar a imagem localmente
def workImage(photo_url, trap_id, user_id, status):
    image_name = trap_id

    if not image_name.endswith(".jpg"):
        image_name += ".jpg"

    utils.download_image(photo_url, image_name)

## Conectar ao banco de dados RDS e publicar os dados

    rds = RDSConnection()

    rds.insert_data(trap_id, user_id, status)

## Processar a imagem e publicar o resultado no S3

# Processar a imagem localmente

    scan.main(["--image", f"photos/{image_name}"])

# Publicar no S3

    s3 = S3Connection()

    processed_image = image_name.replace(".jpg", "_processed.jpg")

    s3.upload_to_s3(f"processed_photos/{image_name}", processed_image)

## Obter e retornar o URL da imagem para a API 
    return s3.get_url(processed_image)
