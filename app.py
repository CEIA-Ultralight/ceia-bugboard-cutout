from fastapi import FastAPI, HTTPException, BackgroundTasks
from models.schema import ImageRequest
import requests
from service.workflow import ImageProcessing
from service.utils.utils import generate_random_name

app = FastAPI()

processor = ImageProcessing()

@app.get("/")
def read_root():
    return {"message": "API online!!!"}

@app.post("/image_cut")
def process_image(data: ImageRequest, background_tasks: BackgroundTasks):
    try:
        response = requests.get(data.photo_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Não foi possível baixar a imagem")

        processor.image_queue.append(data.model_dump())
        image_name = generate_random_name()
        background_tasks.add_task(processor.process_next_image, image_name)

        return {
            "status": "ok",
            "image_name": image_name,
            "processed_image_url": f"https://tfiswpjimraodvnjbybx.supabase.co/storage/v1/object/boards/images/{image_name}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")