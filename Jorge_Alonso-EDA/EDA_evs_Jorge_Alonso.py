import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datasets
ds_evs_clean = pd.read_csv("./Data/ds_evs_clean_final.csv")
ds_population = pd.read_csv("./Data/ds_population_final.csv")

st.title("Análisis de Carga de Vehículos Eléctricos")

# Gráfico 1: Porcentaje de cargas por modelo de vehículo

st.header("Porcentaje de cargas por modelo de vehículo")

model_counts = ds_evs_clean['Vehicle Model'].value_counts()
total_cargas = model_counts.sum()
model_percentages = (model_counts / total_cargas * 100).round(2)

trace = go.Bar(
    x=model_counts.index,
    y=model_percentages.values,
    text=[f'{pct:.2f}%' for pct in model_percentages],
    textposition='outside',
    insidetextanchor='middle',
    hovertemplate=[
        f'{model}<br>{pct:.2f}% ({count} cargas)' 
        for model, pct, count in zip(model_counts.index, model_percentages, model_counts)
    ]
)

layout = go.Layout(
    title='Porcentaje de cargas por modelo de vehículo',
    xaxis=dict(title='Modelo de vehículo'),
    yaxis=dict(title='Porcentaje de cargas (%)',
        showgrid=True,
        gridcolor='lightgray'),
    margin=dict(b=100),
    width=800,
    height=600,
    template='plotly_white'
)

fig1 = go.Figure(data=[trace], layout=layout)
st.plotly_chart(fig1)


# Gráfico 2: Porcentaje total de cargas por ciudad y modelo de vehículo

st.header("Porcentaje total de cargas por ciudad y modelo de vehículo")

pivot_table = pd.crosstab(ds_evs_clean['Charging Station Location'], ds_evs_clean['Vehicle Model'])
total_cargas = pivot_table.values.sum()
pivot_percent_total = pivot_table.div(total_cargas) * 100
ordered_index = pivot_percent_total.sum(axis=1).sort_values(ascending=False).index
pivot_percent_total = pivot_percent_total.loc[ordered_index]

model_colors = {
    'Tesla Model 3': '#CC0000',
    'Nissan Leaf': '#efefef',
    'Hyundai Kona': '#00287A',
    'Chevy Bolt': '#c5b358',
    'BMW i3': '#81C4FF'
}

data = []
for model in pivot_percent_total.columns:
    color = model_colors.get(model, '#888888')
    trace = go.Bar(
        x=pivot_percent_total.index,
        y=pivot_percent_total[model],
        name=model,
        marker=dict(color=color),
        hovertemplate='%{x}<br>Modelo: ' + model + '<br>% Cargas: %{y:.2f}%',
    )
    data.append(trace)

layout = go.Layout(
    title='Porcentaje total de cargas por ciudad y modelo de vehículo',
    xaxis=dict(title='Ciudad'),
    yaxis=dict(
        title='Porcentaje de cargas (%) sobre total general',
        range=[0, 20],
        showgrid=True,
        gridcolor='lightgray'
    ),
    barmode='stack',
    width=900,
    height=600,
    template='plotly_white'  # ← mismo estilo del gráfico ejemplo
)

fig2 = go.Figure(data=data, layout=layout)
st.plotly_chart(fig2)




# Gráfico 3: Eficiencia por vehículo
st.header("Eficiencia por vehículo (km por kWh cargado)")

ds_filtered_efficency = ds_evs_clean[ds_evs_clean['Efficiency'] < 50]

fig3 = px.box(
    ds_filtered_efficency,
    x='Vehicle Model',
    y='Efficiency',
    points='outliers',
    title='Eficiencia por vehículo (km por kWh cargado)',
    labels={
        'Efficiency': 'Eficiencia (km/kWh)',
        'Vehicle Model': 'Modelo de vehículo'
    },
    template='plotly_white'
)

fig3.update_layout(
    xaxis_tickangle=-45,
    yaxis=dict(range=[0, 50], showgrid=True, gridcolor='lightgray'),
    width=900,
    height=600,
)

st.plotly_chart(fig3)


# Gráfico 4: Porcentaje de cargas por localización
st.header("Porcentaje de cargas por localización")

location_counts = ds_evs_clean['Charging Station Location'].value_counts()
total_locations = location_counts.sum()
location_percentages = (location_counts / total_locations * 100).round(2)

trace = go.Bar(
    x=location_counts.index,
    y=location_percentages.values,
    text=[f'{pct:.2f}%' for pct in location_percentages],
    textposition='outside',
    insidetextanchor='middle',
    # Usamos estilo por defecto para las etiquetas (negras)
    hovertext=[
        f'{location}<br>{pct:.2f}% ({count} cargas)' 
        for location, pct, count in zip(location_counts.index, location_percentages, location_counts)
    ],
    hoverinfo='text'  # Indicamos que use hovertext
)

layout = go.Layout(
    title='Porcentaje de cargas por localización (ciudad)',
    xaxis=dict(title='Localización de la carga'),
    yaxis=dict(
        title='Porcentaje de localización (%)',
        showgrid=True,
        gridcolor='lightgray'
    ),
    margin=dict(b=100),
    width=800,
    height=600,
    template='plotly_white'  # ← Estilo del gráfico ejemplo
)

fig4 = go.Figure(data=[trace], layout=layout)
st.plotly_chart(fig4)


# Gráfico 5: Ratio de energía suministrada por densidad de población
st.header("Ratio de energía suministrada por densidad de población")

ds_population_sorted = ds_population.sort_values(by="(kW) / (hab/km²)", ascending=False)

trace = go.Bar(
    x=ds_population_sorted["City"],
    y=ds_population_sorted["(kW) / (hab/km²)"],
    text=[f'{val:.2f}' for val in ds_population_sorted["(kW) / (hab/km²)"]],
    textposition='outside',
    insidetextanchor='middle',
    hovertext=[
        f'{city}<br>{ratio:.2f} kW por hab/km²<br>Densidad: {density} hab/km²<br>Total kW: {kws:.0f} kW'
        for city, ratio, density, kws in zip(
            ds_population_sorted["City"],
            ds_population_sorted["(kW) / (hab/km²)"],
            ds_population_sorted["Population Density (people/km²)"],
            ds_population_sorted["Total kW supplied"]
        )
    ],
    hoverinfo='text'
)

layout = go.Layout(
    title='Ratio de energía suministrada por densidad de población',
    xaxis=dict(title='Ciudad'),
    yaxis=dict(
        title='kW / hab/km²',
        showgrid=True,
        gridcolor='lightgray'
    ),
    margin=dict(b=100),
    width=800,
    height=600,
    template='plotly_white'  # ← Estilo unificado
)

fig5 = go.Figure(data=[trace], layout=layout)
st.plotly_chart(fig5)



# Gráfico 6: Coste de electricidad por kW suministrado
st.header("Coste de electricidad (USD) por kW suministrado en la carga")

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=ds_evs_clean,
    x="Charging Rate (kW)",
    y="Charging Energy Cost (USD /kW)",
    hue="Charging Station Location",
    alpha=0.7
)
plt.title("Coste de electricidad (USD) por kW suministrado en la carga")
plt.xlabel("Carga suministrada (kW)")
plt.ylabel("Coste de la energía suministrada (USD/kW)")
plt.tight_layout()
st.pyplot(plt)
