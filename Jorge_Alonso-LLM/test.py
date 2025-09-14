import requests

def entrenamientos():
    url = 'http://localhost:5000/entrenamientos'
    data = {"pregunta": "Quiero que me des una rutina de entrenamiento para una persona que va a comenzar a sair a correr en calle, cuyo objetivo es correr una carrera de 10km dentro de 3 meses. Además tiene disponibilidad de entrenar 3 días por semana (aproximadamente 1 hora cada día)"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    json_resp = response.json()
    assert "pregunta" in json_resp or "error" in json_resp
    print("OK:", json_resp)

if __name__ == "__main__":
    entrenamientos()
