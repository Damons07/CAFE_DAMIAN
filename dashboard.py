import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

st.title("Dashboard afluencia de clientes - Cafe internet ")

# Leer datos
dfCafe = pd.read_excel("datos/resultadoslimpieza.xlsx")

# Filtro
selected_year = st.selectbox('Selecciona el año:', sorted(dfCafe['fechaEntrada'].dt.year.unique()))
selected_month = st.selectbox('Selecciona el mes:', sorted(dfCafe['Month'].unique()))

# se aplica
df_selected = dfCafe[(dfCafe['fechaEntrada'].dt.year == selected_year) & (dfCafe['Month'] == selected_month)]

# Mostrar el df
st.subheader(f'Datos para {calendar.month_name[int(selected_month)]} del {selected_year}')
st.write(df_selected)

# Gráfica de año
df_compare = dfCafe[dfCafe['fechaEntrada'].dt.year == selected_year].groupby('Month').size().reset_index(name='Number of Clients')
fig_compare = px.bar(df_compare, x='Month', y='Number of Clients',
                     labels={'Month': 'Mes', 'Number of Clients': 'Número de Clientes'},
                     title=f'Comparación mes a mes de {selected_year}')

# Mapear el número del mes a su nombre correspondiente
fig_compare.update_xaxes(
    tickmode='array',
    tickvals=list(range(1, 13)),
    ticktext=[calendar.month_abbr[i] for i in range(1, 13)]
)

st.plotly_chart(fig_compare)

# Gráfica de días del mes
df_selected['fechaEntrada'] = pd.to_datetime(df_selected['fechaEntrada'])
df_selected_month = df_selected.groupby(df_selected['fechaEntrada'].dt.day).size().reset_index(name='Number of Clients')

# Agregar una columna con el nombre del día
df_selected_month['Day of Week'] = df_selected['fechaEntrada'].dt.day_name()

fig_days = px.bar(df_selected_month, x='fechaEntrada', y='Number of Clients',
                  labels={'fechaEntrada': 'Día del Mes', 'Number of Clients': 'Número de Clientes'},
                  title=f'Afluencia de clientes para {calendar.month_name[int(selected_month)]} del {selected_year}')

# Formato legible en el eje x
fig_days.update_xaxes(type='category')

st.plotly_chart(fig_days)

