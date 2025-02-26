from flask import Flask, request, jsonify
from workflow import workImage
import threading
import time
import random
import string

app = Flask(__name__)

image_queue = [] # Lista para armazenar as URLs da fila
processing = False  # Flag para indicar se há uma imagem sendo processada

def process_next_image():
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
    letters = string.ascii_lowercase
    image_name = ''.join(random.choice(letters) for _ in range(length))
    return image_name + ".jpg"

@app.route("/")
def imageURL():
    return "API de Processamento de Imagens - Online"

@app.route("/create-procimage", methods=["POST"])
def create_procimage():
    data = request.get_json()

    if "photo_url" not in data:
        return jsonify({"error": "Parâmetro 'photo_url' é obrigatório"}), 400
    
    if "id" not in data:
        return jsonify({"error": "Parâmetro 'id' é obrigatório"}), 400

    image_name = generate_random_name()
    data["image_name"] = image_name
    image_queue.append(data)
    print(f"Imagem recebida e adicionada na fila com nome: {data['image_name']}")
    
    return jsonify({"status": "ok", "image_name": image_name, "processed_image_url": f"https://tfiswpjimraodvnjbybx.supabase.co/storage/v1/object/boards/images/{image_name}"}), 201

if __name__ == "__main__":
    # Iniciar a thread para processar a fila em background
    processing_thread = threading.Thread(target=process_next_image, daemon=True)
    processing_thread.start()

    app.run(host="0.0.0.0", debug=True)
