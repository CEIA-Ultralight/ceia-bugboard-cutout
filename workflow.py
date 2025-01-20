from connection.rds_connection import RDSConnection
from connection.s3_connection import S3Connection
import utils.utils as utils
import random
import string
import scan

## Receber a imagem e os dados da api
"""Gerar forma de conexão com a API"""
#photo_url = "https://imagens-ultralight.s3.us-east-2.amazonaws.com/img%206.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIA2CUNLZPYDQAF3FPV%2F20250119%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20250119T150719Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJGMEQCIHQNXuhMMpC7pJSPVMF8PmXnqbWmkRFTgiSQmc9UfuXZAiA%2B6nfgaHxcHQ6%2Fd%2F36aPQZ5%2FxV%2FcBCeDobG1uPUOUl1irxAgiQ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDY5Mjg1OTk0ODAxNiIMOj1tx8Ua20CxXMr0KsUCkvatW9ChYWfgbHCwuULTxMaAX5SkUZNWPQPCg63cSwC5lQ4MOt3fxcn09snEydJWhofRDW0YAQ7X15vBz%2BARAmAjuRlwc6lIOKiilH06Ju7TmH3AxWhEMcfkcLaJXs9dIOEDicayJjMSdt1rz%2F0Fl7kUx4If7amdAShHXhFsp41%2Fc8WnibUHyrJFPj4%2BWqk%2F01Yy0C6awbideLzMaysE1KZi%2FAc6sWSg9S3CB%2FnEAcePIM8SjCSCCLpj0ENd4enU1K06Z72BleMKrgXpRH95TYqsTlnAaK5JTjEy4lR7Sh%2BZajAzsRLfgNMBqblbDh1rw3q%2BwKzhOG8dxzfbvOs6LSmYyGba9HbOOiCarORCvOP88dMTEbMElnSWSFyuWcp7COka5iEdbIi1dGPSGjWYFPDTywE%2BghPeNTCe3U5Bauh0eybiETCyo7S8Bjq0Aswa4L6aE4sb6HeUkrBMQd9mUy1vkMNFTMGa1PMC%2BshpXJRtj%2BYnvahVCH7mxH7EQMrN6rOHRlfVVM87x3d%2BoHMIs2NkYYm8WVU8cJ%2Be%2B6soi0vt2UCjECpxJTTynt%2F5hTNYYZnBCbfqEW5dTUFv%2By6WPRj%2BDJdtpVUdKVjV1cy8jZ%2BfzDTu4%2Btoi%2BJFHDJdvc2CqxtbugQBwZm1c%2FTnGxX2CO5w1DfyP894uwvi0Z8PeAxNEpGSepRNBWj9%2B9XFCiilTrOnJBeRVgb8joTnjbJaXQukh05mEraIFF3iyKhI4%2FOeGXAj1OpFXA01iPt%2Fyrzg0MrPExjYuWnPajgNC1%2B4c0S1FB7ncLkXGAl59QBtKviuxha%2BfLGr36%2F9j1yE%2BD6IRhJixbgY8QHsBPKjv2occTfu&X-Amz-Signature=f5b1b4f2541f842f18df3be93c4a564c0c7645487e8b735d0c79cbbc471be184&X-Amz-SignedHeaders=host&response-content-disposition=inline"
#trap_id = "img2"
#user_id = "pedro"
#status = "processando"
# dados presentes no body do request (POST) feito por eles na nossa API

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

## Obter o URL da imagem no S3

## Retornar o URL da imagem para a API 
    return s3.get_url(processed_image)

# fazer requisição Patch da nossa API para a deles e alterar o campo photo_url

"""Gerar forma de conexão com a API"""
