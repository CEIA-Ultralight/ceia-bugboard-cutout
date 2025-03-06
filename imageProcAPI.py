from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from workflow import workImage
import threading
import time
import random
import string

app = Flask(__name__)
api = Api(app, version='1.0', title='API de Processamento de Imagens',
          description='Uma API para processamento de imagens de forma assíncrona.',
          doc='/docs')

# Namespace para organização dos endpoints
ns = api.namespace('processamento', description='Operações relacionadas ao processamento de imagens')

# Modelo de entrada para a requisição
image_model = api.model('Imagem', {
    'photo_url': fields.String(required=True, description='URL da foto a ser processada'),
    'id': fields.String(required=True, description='Identificador único do usuário')
})

# Modelo de resposta
response_model = api.model('Resposta', {
    'status': fields.String(description='Status da requisição'),
    'image_name': fields.String(description='Nome da imagem gerado'),
    'processed_image_url': fields.String(description='URL da imagem processada')
})

image_queue = []  # Lista para armazenar as URLs da fila
processing = False  # Flag para indicar se há uma imagem sendo processada

def process_next_image():
    """Processa as imagens da fila"""
    global processing
    while True:
        if image_queue and not processing:
            processing = True
            image_data = image_queue.pop(0)
            image_name = image_data["image_name"]
            print(f"Processando imagem: {image_name}")

            # Processa a imagem e obtém os dados da imagem no bucket
            workImage(image_data["photo_url"], image_name, image_data["id"])

            processing = False
        time.sleep(1)  # Pequeno delay para evitar loop intenso

def generate_random_name(length=10):
    """Gera um nome aleatório para a imagem"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length)) + ".jpg"

@api.route("/")
class Home(Resource):
    def get(self):
        """Endpoint para verificar se a API está online"""
        return {"message": "API de Processamento de Imagens - Online"}

@ns.route("/create-procimage")
class CreateProcImage(Resource):
    @ns.expect(image_model)  # Define o modelo esperado na requisição
    @ns.marshal_with(response_model, code=201)  # Define o modelo da resposta
    def post(self):
        """Adiciona uma nova imagem à fila de processamento"""
        data = request.get_json()

        if "photo_url" not in data:
            api.abort(400, "Parâmetro 'photo_url' é obrigatório")
        
        if "id" not in data:
            api.abort(400, "Parâmetro 'id' é obrigatório")

        image_name = generate_random_name()
        data["image_name"] = image_name
        image_queue.append(data)
        print(f"Imagem recebida e adicionada na fila com nome: {data['image_name']}")

        return {
            "status": "ok",
            "image_name": image_name,
            "processed_image_url": f"https://tfiswpjimraodvnjbybx.supabase.co/storage/v1/object/boards/images/{image_name}"
        }, 201

# Adiciona o namespace à API
api.add_namespace(ns, path='/processamento')

if __name__ == "__main__":
    # Iniciar a thread para processar a fila em background
    processing_thread = threading.Thread(target=process_next_image, daemon=True)
    processing_thread.start()

    app.run(host="0.0.0.0", debug=True)