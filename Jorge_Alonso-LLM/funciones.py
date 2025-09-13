
from datetime import datetime
from groq import Groq
import os
import psycopg2
from variables import config

def bbdd (pregunta, respuesta):
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    query =  f"INSERT INTO preguntas_respuestas (preguntas, respuesta, fecha) VALUES (%s, %s, %s);"

    cursor.execute(query, (pregunta, respuesta, datetime.now())) #se le pasa los datto en tupla, para ser añadidos en la base de datos

    conn.commit() #Siempre que hay un insert se pone un commit
    cursor.close() #Cerramos el cursos 
    conn.close() 

    return "Ok"


#Funcion Groq


def llm(pregunta):
  client = Groq(
      api_key=os.environ.get("GROQ_API_KEY"),
  )

  chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "system", #revisar cómo usar esto
              "content": "Quiero que seas mi modelo de IA para recomendaciones sobre campañas de marketing. Si te preguntan sobre cualquier tema externo al marketing, publicidad y negocios relacionados, tienes que responder que no pudes hablar de temas que no sean marketing y publicidad. Quiero que todas tus respuesta tengan respuesta bien estructurada y con terminología de marketing",
          }, 
          {"role": "user", 
            "content": "pregunta"
          }
      ],
      model="openai/gpt-oss-20b",
      stream=False,
  )

  return(chat_completion.choices[0].message.content)