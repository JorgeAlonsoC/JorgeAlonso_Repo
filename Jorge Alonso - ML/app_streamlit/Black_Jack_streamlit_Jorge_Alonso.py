import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import numpy as np


# Cargar datasets
ds_blackjack = pd.read_csv("../data/blkjckhands.csv", nrows=200004)

#1 - LIMPIEZA Y TRASFORMACIÓN DE DATOS

#Eliminamos columnas referente a apuestas
ds_blackjack = ds_blackjack.drop(["plwinamt", "dlwinamt"], axis=1)

# Suma dos primeras cartas del jugador
ds_blackjack = ds_blackjack.rename(columns= {"player_2cards_sum": "ply2cardsum"})

# número de cartas totales pedidas por el jugador (cuenta en una única fila, el numero de cartas que ha pedido el jugador)
ds_blackjack["ply_No_cards"] = ds_blackjack[["card1", "card2", "card3", "card4", "card5"]].ne(0).sum(axis=1) #.e(0) quiere decir not equal 0

# número de cartas totales pedidas por el dealer (cuenta en una única fila, el numero de cartas que ha pedido el dealer)
ds_blackjack["deal_No_cards"] = ds_blackjack[["dealcard1", "dealcard2", "dealcard3", "dealcard4", "dealcard5"]].ne(0).sum(axis=1)

# Suma total de cartas del dealer en la mesa al empezar la partida (player vs crepier)
ds_blackjack["deal_2cards_sum"] = ds_blackjack[["dealcard1", "dealcard2"]].sum(axis=1)

# Suma total de cartas visibles en la mesa al empezar la partida (player vs crepier)
ds_blackjack["sum_3first_cards"] = ds_blackjack[["card1", "card2", "dealcard1"]].sum(axis=1)

#trasformar las variables categoricas en numericas, la mas importante win, los, push
def  numeric_def (x):
    if x == "Loss":
        return 0
    if x == "Push":
        return 1
    if x == "Win":
        return 2
    
ds_blackjack["winloss_numeric"] = ds_blackjack["winloss"].apply(numeric_def)

# Creamos la función para pasar la fencuin black jack a numerica y la aplicamos en un nueva columna
def blkjck_def (x):
    if x == "nowin":
        return 0
    if x == "Win":
        return 1    
ds_blackjack["blkjck_numeric"] = ds_blackjack["blkjck"].apply(blkjck_def)

# Creamos la columna plybustbeat en formato numerica
def plybustbeat_def (x):
    if x == "Push":
        return 0
    if x == "Plwin":
        return 1
    if x == "DlBust":
        return 2
    if x == "Beat":
        return 3
    if x == "Bust":
        return 4    
ds_blackjack["plybustbeat_numeric"] = ds_blackjack["plybustbeat"].apply(plybustbeat_def)


## FIN DE LA LIMPIEZA Y TRASFORMACIÓN DE LOS DATOS

# 2 - CREACIÓN Y REPRESENTACIÓN DE LOS GRÁFICOS

#suma de viscorias por cada jugador
win_counts = {} #diccionario que va a recoger todas las victorias de cada jugador

for i in range(1, 7):
    player= f"Player{i}"
    wins= ds_blackjack[(ds_blackjack["PlayerNo"]==player) & (ds_blackjack["winloss"]=="Win")].shape[0]

    win_counts[player]= wins #añadimos al diccionario el jugador como indice y como valor las partidas ganadas

wins_player1 = win_counts['Player1'] #asignamos a cada variable las victorias de dicho jugador
wins_player2 = win_counts['Player2']
wins_player3 = win_counts['Player3']
wins_player4 = win_counts['Player4']
wins_player5 = win_counts['Player5']
wins_player6 = win_counts['Player6']
wins_total = wins_player1 + wins_player2 + wins_player3 + wins_player4 + wins_player5 + wins_player6

#suma de derrotas de jugador
loss_counts = {} #diccionario que va a recoger todas las derrotas de cada jugador

for i in range(1, 7):
    player= f"Player{i}"
    loss= ds_blackjack[(ds_blackjack["PlayerNo"]==player) & (ds_blackjack["winloss"]=="Loss")].shape[0]

    loss_counts[player]= loss #añadimos al diccionario el jugador como indice y como valor las partidas perdidas

loss_player1 = loss_counts['Player1'] #asignamos a cada variable las derrotas de dicho jugador
loss_player2 = loss_counts['Player2']
loss_player3 = loss_counts['Player3']
loss_player4 = loss_counts['Player4']
loss_player5 = loss_counts['Player5']
loss_player6 = loss_counts['Player6']
loss_total = loss_player1 + loss_player2 + loss_player3 + loss_player4 + loss_player5 + loss_player6

#suma de empates de jugador
push_counts = {}  # Diccionario que va a recoger todos los empates de cada jugador

for i in range(1, 7):
    player = f"Player{i}"
    push = ds_blackjack[(ds_blackjack["PlayerNo"] == player) & (ds_blackjack["winloss"] == "Push")].shape[0]
    
    push_counts[player] = push  # Añadimos al diccionario el jugador como clave y las partidas empatadas como valor

# Asignamos a cada variable los empates de dicho jugador
push_player1 = push_counts['Player1']
push_player2 = push_counts['Player2']
push_player3 = push_counts['Player3']
push_player4 = push_counts['Player4']
push_player5 = push_counts['Player5']
push_player6 = push_counts['Player6']
push_total = push_player1 + push_player2 + push_player3 + push_player4 + push_player5 + push_player6

# % total de partidas ganadas, perdidas y empatadas para los jugadores
total_losses_per = loss_total / (loss_total + push_total + wins_total)
total_push_per = push_total / (loss_total + push_total + wins_total)
total_wins_per = wins_total / (loss_total + push_total + wins_total)

#-----------------------------

st.title("Black Jack - EDA Main graphs")

st.image("bj.jpg", caption="ML aplicado a Blackjack -  Jorge Alonso", use_container_width=True)

# Gráfico 1: Resultado total de las partidas para los jugadores

sns.set_theme(style="white")

# Datos
labels = ['Partidas ganadas', 'Partidas perdidas', 'Partidas empatadas']
sizes = [total_wins_per, total_losses_per, total_push_per]
colors = sns.color_palette("deep")[0:3]  # colores suaves y agradables
explode = (0.05, 0.05, 0.05)  # separación para cada porción

# Crear gráfico de pastel para Streamlit
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    colors=colors,
    startangle=90,
    explode=explode,
    shadow=True,
    textprops={'fontsize': 14, 'color': 'white'}  # 👈 texto blanco
)

# Poner también el texto de porcentajes en blanco
for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_backgroundcolor("none")  # 👈 sin fondo

# Poner el título en blanco
ax.set_title('Resultado total de las partidas para los jugadores',
             fontsize=16, weight='bold', color='white')

ax.axis('equal')

fig.patch.set_alpha(0.0)   # fondo de la figura transparente
ax.set_facecolor("none")   # fondo de los ejes transparente

st.pyplot(fig)


#-----
# Gráfico 2: Suma total de cartas (jugador) vs resultado final
orden_resultado = ["Loss", "Win", "Push"]
colores_resultado = {
    "Loss": "#636EFA",  # azul
    "Win": "#EF553B",   # rojo
    "Push": "#00CC96"   # verde
}

# Agrupar por las 3 cartas iniciales y resultado
grouped = ds_blackjack.groupby(["sumofcards", "winloss"]).size().reset_index(name="count")

# Forzar tipo categoría con orden específico
grouped["winloss"] = pd.Categorical(grouped["winloss"], categories=orden_resultado, ordered=True)

# Crear gráfica
fig = px.scatter(
    grouped,
    x="sumofcards",
    y="winloss",
    size="count",
    size_max=50,
    color="winloss",
    color_discrete_map=colores_resultado,
    category_orders={"winloss": orden_resultado},
    title="Dispersión: suma de cartas totales del jugador vs resultado",
    labels={
        "sumofcards": "Suma total de las cartas del jugador",
        "winloss": "Resultado",
        "count": "Cantidad de ocurrencias"
    },
)

st.plotly_chart(fig, use_container_width=True)

#Data Frame: suma total de las cartas del jugador, % de loss, push y win registrados anteriormente.

# 1. Agrupar y contar ocurrencias
conteo_sumofcards = ds_blackjack.groupby(["sumofcards", "winloss"]).size().reset_index(name="count")

# 2. Calcular el total por cada valor de sumofcards
conteo_sumofcards["total"] = conteo_sumofcards.groupby("sumofcards")["count"].transform("sum")

# 3. Calcular el porcentaje
conteo_sumofcards["percentage"] = (conteo_sumofcards["count"] / conteo_sumofcards["total"] * 100).round(2)

# 4. Pivotear la tabla para ver los porcentajes
tabla_porcentajes_sumofcards = conteo_sumofcards.pivot(
    index="sumofcards", columns="winloss", values="percentage"
).fillna(0)

# 5. Convertir a DataFrame con índice plano
df_porcentajes_sumofcards = tabla_porcentajes_sumofcards.reset_index()

st.dataframe(df_porcentajes_sumofcards)

#---------------------------------------------------------------------MODELO DE PREDICCIÓN-------------------------------------------------------------

#importamos los archivos pkl de grid_cv y model

grid_cv = joblib.load("grid_cv.pkl")
model = joblib.load("model.pkl")

#Importamos el Witget de predicción del modelo final y lo adaptamos a streamlit


# Diccionario de resultados posibles en la partida
label_map = {0: "Loss", 1: "Push", 2: "Win"}

def get_probabilities_safe(model, X):

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)
        classes = getattr(model, "classes_", None)
        return proba, classes, False

    if hasattr(model, "decision_function"):
        scores = model.decision_function(X)
        if scores.ndim == 1:
            scores = np.column_stack([-scores, scores])
        scores = scores - scores.max(axis=1, keepdims=True)
        exp_s = np.exp(scores)
        proba = exp_s / exp_s.sum(axis=1, keepdims=True)
        classes = getattr(model, "classes_", np.arange(proba.shape[1]))
        return proba, classes, True

    classes = getattr(model, "classes_", np.array([0, 1, 2]))
    n_classes = len(classes)
    proba = np.full((len(X), n_classes), 1.0 / n_classes)
    return proba, classes, True

# Encabezado para streamlit
st.header("Predicción Blackjack")

# Inputs (equivalentes a tus IntText)
col1, col2 = st.columns(2)
with col1:
    w_sumofcards   = st.number_input("sumofcards",  min_value=0, step=1, value=10)
    w_ply2cardsum  = st.number_input("ply2cardsum", min_value=0, step=1, value=10)
with col2:
    w_dealcard1    = st.number_input("dealcard1",   min_value=0, step=1, value=5)
    w_ply_No_cards = st.number_input("ply_No_cards",min_value=0, step=1, value=2)

if st.button("Predecir", type="primary"):
    # Construir DataFrame igual que en tu notebook
    X_manual = pd.DataFrame([{
        "sumofcards": w_sumofcards,
        "dealcard1": w_dealcard1,
        "ply2cardsum": w_ply2cardsum,
        "ply_No_cards": w_ply_No_cards
    }])

    # Predicción
    pred = model.predict(X_manual)[0]
    st.write(f"**Predicción:** {label_map[int(pred)]}  *(0=Loss, 1=Push, 2=Win)*")

    # Probabilidades
    proba, classes, aproximadas = get_probabilities_safe(model, X_manual)
    classes = np.asarray(classes).astype(int)
    labels = [label_map.get(c, str(c)) for c in classes]

    perc = (proba[0] * 100).round(2)
    perc_dict = dict(zip(labels, perc))

    ordered_cols = ["Loss", "Push", "Win"]
    df_proba = pd.DataFrame([{col: perc_dict.get(col, 0.0) for col in ordered_cols}])

    titulo = "Probabilidades por clase (%)"
    if aproximadas:
        titulo += " (aprox.)"
    st.subheader(titulo)
    st.dataframe(df_proba.style.format("{:.2f}%"), use_container_width=True)

    # Recomendación según % Loss
    loss_pct = perc_dict.get("Loss", 0.0)
    if loss_pct > 50:
        st.success("♣️ **Recomendación:** Pedir carta")
    else:
        st.info("♣️ **Recomendación:** Plantarse")
