import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

URL = 'https://es.wikipedia.org/wiki/Python' # URL de la página a la que se le extraerán los links

#  función para obtener el html de la página
def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return None

# función para obtener el objeto soup
def get_soup(html):
    if html:
        return BeautifulSoup(html, 'html.parser')
    return None

# Función para obtener los links de las imágenes
def get_links(soup):
    links = []  # Lista para almacenar los links
    formatos = {'png', 'jpg', 'webp'}  # Extensiones válidas

    for img in soup.find_all('img'):  # Se busca la etiqueta img
        src = img.get('src')
        if src:
            ext = src.split('.')[-1].lower()
            if ext in formatos:
                links.append(src)  # Se obtiene el link de la imagen y se añade a la lista
    
    return links

# Función para crear la carpeta imagenes
def crear_carpeta():
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

# Función para descargar una imagen desde una URL y guardarla en la carpeta imagenes
def decargar_imagen(url, base_url, folder="imagenes"):
    try:
        # Asegurarse de que la URL sea absoluta
        img_url = urljoin(base_url, url)
        response = requests.get(img_url, stream=True) # Realizar la solicitud en fragmentos
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        filename = os.path.join(folder, os.path.basename(urlparse(img_url).path)) # Obtener el nombre del archivo

        with open(filename, 'wb') as file: # Guardar la imagen en la carpeta imagenes
            for datos in response.iter_content(1024): # Iterar sobre los datos de la imagen
                file.write(datos) # Escribir los datos en el archivo
        print(f"Imagen descargada: {filename}")
    # Manejo de errores
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar {url}: {e}")


# Función principal para extraer y descargar imágenes
def main():
    crear_carpeta() # Se crea la carpeta imagenes
    html = get_html(URL)  # Se obtiene el HTML de la página
    soup = get_soup(html)  # Se obtiene el objeto soup

    if soup:
        links = get_links(soup)  # Se obtienen los links de las imágenes 

        for link in links:  # Se descargan las imágenes
            decargar_imagen(link, URL)

main()