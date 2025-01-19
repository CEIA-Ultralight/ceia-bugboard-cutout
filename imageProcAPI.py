from flask import Flask, request, jsonify
from workflow import workImage

app = Flask(__name__)

# get_url
@app.route("/")
def imageURL():
    return "Teste Imagem url"

@app.route("/create-procimage", methods = ["POST"])
def create_procimage():
    data = request.get_json()

    #processamento será feito dentro ou fora da requisição post?
    #caso seja dentro terá que ser mais curta do que o time out de 6 segundos
    #caso seja fora o data deve ser salvo no BD nosso

    data["photo_url"] = workImage(data["photo_url"], data["trap_id"], data["user_id"], data["status"])
    data["status"] = "Finalizado"

    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug = True) 