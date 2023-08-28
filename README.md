Proyecto de Scraping y Dashboard de Análisis de Videojuegos
Este proyecto consta de dos scripts: uno para realizar el scraping de datos de análisis de videojuegos desde una página web y otro para crear un dashboard interactivo utilizando los datos recopilados. El proceso incluye recopilar los datos, guardarlos en un archivo CSV, notificar a través de un bot de Telegram y visualizarlos en un dashboard de análisis.

Script de Scraping (get_data_url.py)
Este script recopila datos de análisis de videojuegos desde una página web y los almacena en un archivo CSV. Utiliza las siguientes bibliotecas:

requests: Para realizar solicitudes HTTP y obtener el contenido de la página web.
lxml.html: Para analizar el contenido HTML y extraer los datos relevantes.
re: Para trabajar con expresiones regulares y limpiar el texto del precio.
pandas: Para crear y manipular el DataFrame que contendrá los datos recopilados.
os: Para manejar la creación de carpetas y archivos.
subprocess: Para ejecutar el script del dashboard desde este script.
webbrowser: Para abrir una ventana del navegador automáticamente.
requests: Para realizar solicitudes HTTP y notificar a través del bot de Telegram.
Script de Dashboard (dashboard.py)
Este script crea un dashboard interactivo utilizando los datos recopilados del script de scraping. Utiliza las siguientes bibliotecas:

pandas: Para cargar los datos desde el archivo CSV.
dash: Para crear la aplicación de dashboard interactivo.
dash.dependencies: Para manejar las dependencias entre componentes del dashboard.
plotly.express: Para crear gráficos interactivos en el dashboard.



Requisitos
Asegúrate de tener instaladas las siguientes bibliotecas antes de ejecutar los scripts:

requests
lxml
pandas
dash
plotly

Instrucciones de Uso
Ejecuta el script de scraping "python3 scrapper.py" en la ruta donde se encuentre el script para recopilar los datos de análisis de videojuegos desde la página web.