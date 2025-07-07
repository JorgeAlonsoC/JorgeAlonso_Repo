import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

#Importamos los data sets para poder crear los gráficos en streamlit

ds_evs_clean = pd.read_csv("./Recursos/Data/ds_evs_clean_final.csv")
ds_population_final = pd.read_csv("./Recursos/Data/ds_population_final.csv")

#Empezamos a traer el código de los gráficos

