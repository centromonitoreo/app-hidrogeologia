# Herramienta de Análisis de Calidad de Agua Subterránea

Este repositorio contiene una herramienta desarrollada en Python con una interfaz gráfica basada en tkinter para analizar la calidad de agua subterránea a partir de datos de monitoreo. La herramienta genera análisis de balance iónico y visualizaciones como gráficos de Piper, Stiff, Mifflin y Gibbs.

## Características

- **Análisis de Balance Iónico**: Evalúa la coherencia química de las muestras.
- **Visualización**: Gráficos hidrogeoquímicos para análisis detallado.
- **Interfaz Gráfica**: Interacción sencilla a través de una ventana GUI.
- **Versatilidad**: Usable desde Python o como un archivo ejecutable (.exe) en Windows.

## Requisitos

- Python 3.x
- Dependencias:

    ```bash
    imageio==2.34.2
    matplotlib==3.7.1
    numpy==1.24.3
    openpyxl==3.1.5
    pandas==1.4.2
    seaborn==0.11.2
    tkinter (incluido en Python estándar)
    ```

Instalación de dependencias:

    ```bash
    pip install -r requirements.txt
    ```

## Instalación

### Desde Python

1. Clona el repositorio:

    ```bash
    git clone https://github.com/centromonitoreo/app-hidrogeologia.git
    ```

2. Ejecuta el script principal con la interfaz gráfica:

    ```bash
    python src/main.py
    ```

### Desde el ejecutable (.exe)

1. Navega al directorio `dist/main` donde se encuentra el archivo `main.exe`.
2. Haz doble clic en `main.exe` para abrir la aplicación.

## Formato de Datos

Los datos deben estar en formato *melt* con las siguientes columnas mínimas:

- `punto`: Identificación del punto de monitoreo.
- `fecha`: Fecha de la medición.
- `parametro`: Tipo de parámetro (ej. pH, conductividad).
- `valores`: Valores correspondientes a cada parámetro.

## Contribuciones

Las contribuciones son bienvenidas. Sigue las normas del repositorio para más detalles.

