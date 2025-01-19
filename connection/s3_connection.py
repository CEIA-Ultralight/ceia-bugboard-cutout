import boto3
from botocore.exceptions import NoCredentialsError

class S3Connection:
    
    def __init__(self):
        self.client = boto3.client('s3')
        print("Conexão com o S3 estabelecida com sucesso!")

    def upload_to_s3(self, file_directory, object_name, bucket="imagens-ultralight"):
        if object_name is None:
            object_name = file_directory  # If no custom object name is provided, use file_directory

        try:
            self.client.upload_file(file_directory, bucket, object_name)
            print(f"File '{file_directory}' uploaded to S3 bucket '{bucket}' successfully.")
        except FileNotFoundError:
            print(f"The file '{file_directory}' was not found.")
        except NoCredentialsError:
            print("Credentials not available.")

    def get_url(self, object_key, bucket="imagens-ultralight"):

        try:
            url_pre_assinada = self.client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket, 'Key': object_key},
                                                        ExpiresIn=300)
            print(f"URL gerada com sucesso: {url_pre_assinada}")

        except Exception as e:
            print(f"Erro ao gerar a URL: {e}")