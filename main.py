from fastapi import FastAPI, HTTPException 
from fastapi.responses import StreamingResponse
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional

app = FastAPI()

RUTA_CSV = "ventas_sinteticas.csv"
df = pd.read_csv(RUTA_CSV)
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

@app.get("/")
def saludo():
    return{"mensaje":"hola desde mi API pandas"}

columnas_cuantitativas=["precio_unitario","cantidad","descuento","total"]

@app.get("/metrica/{columna}")
def calcular_metrica(columna):
    if columna not in columnas_cuantitativas:
        raise HTTPException("Esa columna no es cuantitativa, ndm")
    datos=df[columna]
    media=datos.mean(),
    mediana=datos.median(),
    minimo=datos.min(),
    maximo=datos.max(),
    desvest=datos.std()

    return{
        "media":media,
        "mediana":mediana,
        "minimo":minimo,
        "maximo":maximo,
        "desvest":desvest,
        "saludos":"Saludos Cordiales"
    }

@app.get("/ventas_x_region")
def ventas(regiones: Optional[str] = None):
    if regiones:
        lista_regiones=regiones.split(",")
        lista_filtrada=df.groupby("region")["total"].sum().loc[lista_regiones]
        return lista_filtrada
    else:
        data = df.groupby("region")["total"].sum()
        return data. to_dict()
        

@app.get("/graficas/precios")
def grafica_precios():
    
    fig, ax = plt.subplots()
    ax.hist(df["precio_unitario"].dropna(), bins=20)
    ax.set_title("Distribución de precios unitarios")
    ax.set_xlabel("Precio unitario")
    ax.set_ylabel("Frecuencia")

    imagen = BytesIO()
    fig.savefig(imagen, format="png", bbox_inches="tight")
    plt.close(fig)
    imagen.seek(0)

    return StreamingResponse(imagen, media_type="image/png")