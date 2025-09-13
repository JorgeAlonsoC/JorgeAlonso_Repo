from flask import request, Flask, jsonify
import os
from funciones import llm, bbdd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True



#SE DEBERÍA HACER CON LAS VARIABES EN INGLES HTML?


#inicio de la API
@app.route("/", methods= ["GET"])
def main ():
    return "API creador de entrenamientos"

#Enpoint que recoge la pregunta (Json)
@app.route("/entrenamientos", methods = ["POST"])
def marketing():
    """
    {"pregunta": "Quiero que me des una rutina de entrenamiento para una persona que va a comenzar a sair a correr en calle, cuyo objetivo es correr una carrera de 10km dentro de 3 meses. Además tiene disponibilidad de entrenar 3 días por semana (aproximadamente 1 hora cada día)"}
    """
    data = request.get_json()
    pregunta = data.get("pregunta")

    respuesta = llm(pregunta) #le pasamos al llm la pregunta
    respuesta_bbdd = bbdd(pregunta, respuesta)

    if respuesta_bbdd == "Ok":
        return jsonify ({"pregunta": pregunta, "respuesta": respuesta})
    else:
        return jsonify({"error": "Error de la pregunta"})


app.run()

#if __name__ = "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=True) #app.run() es solo para local 

    #para iniciarlo docker build -t nombre_api . 