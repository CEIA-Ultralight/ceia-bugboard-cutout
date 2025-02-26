import requests

def patch(id, photo_url):
    
    url = f"https://tfiswpjimraodvnjbybx.supabase.co/rest/v1/Boards?id=eq.{id}"
    headers = { "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmaXN3cGppbXJhb2R2bmpieWJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMxNTIwNTUsImV4cCI6MjA0ODcyODA1NX0.I8UX36hAphowNk85VcL6iYh4TIBwsE0r3wgreTEDaII",
            "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmaXN3cGppbXJhb2R2bmpieWJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMxNTIwNTUsImV4cCI6MjA0ODcyODA1NX0.I8UX36hAphowNk85VcL6iYh4TIBwsE0r3wgreTEDaII",
            "Prefer": "return=representation"
    }

    data = {
        "trimmed_photo_url": photo_url
    }


    response = requests.patch(url, json=data, headers=headers)

    if response.status_code in [200, 204]:
        print("Atualização feita com sucesso!")
        print(response.json())  # Caso a API retorne um JSON
    else:
        print(f"Erro ao atualizar: {response.status_code}")
        print(response.text)  # Exibir a resposta do servidor
