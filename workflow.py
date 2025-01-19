from connection.rds_connection import RDSConnection
from connection.s3_connection import S3Connection
import utils.utils as utils
import random
import string
import scan

## Receber a imagem e os dados da api
"""Gerar forma de conexão com a API"""
photo_url = "https://imagens-ultralight.s3.us-east-2.amazonaws.com/teste2.jpg?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEIv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJIMEYCIQDWiYPc0xVinRBL1vaq%2Fza0jJciqavpM2xy%2BdonhSqhkAIhAMUrBvK2Lvmh1WWIe4GWPZgyEmQLA9Cj2OhOarKfk%2FceKtADCIT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjkyODU5OTQ4MDE2Igz1YnI1b45i2b8uDU0qpAOQsnO4Gnxn%2BQizcDunCRmcdRnhTXC8BbpAWpxV4dOaRO7nRxEZFsDT8P8cjb0oF3VnmWUol4pM%2FDVcGeb9mkvJXgvZqkOEfbSq6TmJ158s6jwmuSLtVVDPwCAm2OHKPCZ3I7LwG9h1%2B4uRu7sElBEI%2FyMR31ro%2BMG5Yrn33Rq1xfk9Lrv3cjwR%2FK%2BVO7ppsjkIhLoWABnY5ppes5aSU9sUl8DXQEQ9CNfJM%2FJClknTRx1pWJ228UbmSqPSkXCrkdyKR4Z97fvK%2FiB1MWLD0ZcMXjJQjxqBmW86bgkrNt7u5y5OneaTdKHQRuONC45xUS9Zz06OQbvk30VXj%2BTrrJo%2F57DFQ8kI1eu6CTDtjLa%2B7FEEPWNYP5XEatTYO21rz68CXdxM2U1kE5N6cZvJmDmwTsE%2FF5N01%2FpC9SUdhmrYGn0Zdo5365thIp7InFoP9LKNUj%2BjneV6DOPTa%2BgxUfBbd6w31kImgqQTesb7Hx62kNRqbF3zZ981fkuLtqBNdiK8OeVKvFCeb6cpznZmCEiq2d4F43mhitwB2knYprs5K7odd1ww3L2xvAY64wJiFWeSPffXXXWEVKdZylrP%2B69AlkASM01kMZINfjJqYKU9MQRdhDa%2FuFMkEHtgDlwHWkzYDIWmIcz0H%2BYDjwV41gdQzoSQSMeWBtvV4jlqZQlwVocdkCd%2BcarKT0wqEvoG04rIuAddDlt8%2BbB%2B3Kdl8OvCFuXry1MXvpFinzkVJdZZlHwbZDKLuBBpHNdTor%2B2LM7O%2F9Q31nctIhJ5W%2BJ9wFukPxs8EbAWDHp4TdT7CWUKleAPknu4VVSoWIEmlRs6OQN4O3As0ljB4idcS7WKD3yDdsfdB7SAUKWMxUZ1TUjgCAK7nXcLsLnyevgbpsDP6zU%2BVEqlGXoCL%2F45Iiws44ud%2BdfJrLWbMVgzy8EEZgYQgKO%2F6gPcxwHhfcq1JMQuDRmd3zNDkiS7TRP%2Bi55IW0CdW%2Fc1c3ElD4W497AgD9VYev3INnbBEX%2B2fGe18B%2FfxlUqvcska0A%2FC3v91e57qEhv&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA2CUNLZPYBP2J52XB%2F20250119%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20250119T030008Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=133713a0bace52a44dec99969431cfcdfe628d095c7abafcbb28ad6f69906d26"
trap_id = "esquina"
user_id = "pedro"
status = "processando"

# Baixar a imagem localmente

image_name = trap_id

if not image_name.endswith(".jpg"):
    image_name += ".jpg"

utils.download_image(photo_url, image_name)

## Conectar ao banco de dados RDS e publicar os dados

rds = RDSConnection()

cursor = rds.cursor

rds.insert_data(trap_id, user_id, status)

## Processar a imagem e publicar o resultado no S3

# Processar a imagem localmente

scan.main(["--image", f"photos\\{image_name}"])

# Publicar no S3

s3 = S3Connection()

processed_image = image_name.replace(".jpg", "_processed.jpg")

s3.upload_to_s3(f"processed_photos\\{image_name}", processed_image)

## Obter o URL da imagem no S3

s3.get_url(processed_image)

## Retornar o URL da imagem para a API 

"""Gerar forma de conexão com a API"""
