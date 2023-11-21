import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

st.title("Dashboard Afluencia de Clientes - Café Internet")

# Leer los datos
dfCafe = pd.read_excel("datos/resultadoslimpieza.xlsx")

meses_dict = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

meses = [meses_dict[m] for m in sorted(set(dfCafe["fechaEntrada"].dt.month))]
anios = list(set(dfCafe["fechaEntrada"].dt.year))

# Sidebar para selección de año y mes
anioSeleccionado = st.sidebar.selectbox('Seleccionar año', anios)
mesSeleccionado = st.sidebar.selectbox('Seleccionar mes', meses)

# Filtrado de datos según año y mes seleccionados
dfFiltradoMesanio = dfCafe[
    (dfCafe['fechaEntrada'].dt.month == list(meses_dict.keys())[list(meses_dict.values()).index(mesSeleccionado)]) &
    (dfCafe['fechaEntrada'].dt.year == anioSeleccionado)
]

# Visualización del df} filtrado
st.subheader("Datos Filtrados:")
st.write(dfFiltradoMesanio)

# Gráfica comparativa mes a mes de los dos años
dfmeses = dfCafe.groupby(pd.Grouper(key="fechaEntrada", freq="1M")).count().reset_index()
dfmeses['year'] = dfmeses['fechaEntrada'].dt.year
dfmeses['month'] = dfmeses['fechaEntrada'].dt.strftime('%B')
dfmeses['year_month'] = dfmeses['year'].astype(str) + '-' + dfmeses['fechaEntrada'].dt.month.astype(str).str.zfill(2)
dfmeses = dfmeses.sort_values('year_month')

fig_meses = px.bar(
    dfmeses,
    x='month',
    y='horaEntrada',
    facet_col='year',
    labels={'horaEntrada': 'Cantidad de Entradas'},
    title='Entradas Mensuales por Año',
    text='year',
    category_orders={'month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}
)

# Gráfica de dias por mes seleccionado
dfMes = dfFiltradoMesanio.groupby(pd.Grouper(key="fechaEntrada", freq="1D")).count().reset_index()
dfMes["fechaStr"] = dfMes["fechaEntrada"].astype(str) + " - "
dfMes["Day"] = dfMes["fechaEntrada"].dt.day_name()+"-"+dfMes["fechaStr"]

fig_dias = px.bar(dfMes, x='Day', y='horaEntrada', labels={'Dia': 'Numero de Clientes'}, title='Número de Clientes por semana')

# Visualización de las gráficas en el dashboard
st.plotly_chart(fig_meses, use_container_width=True)
st.plotly_chart(fig_dias, use_container_width=True)
