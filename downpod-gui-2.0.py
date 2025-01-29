# DOWNPOD-GUI-2.0
# ===============
# Desarrollador: Yago Llopis
# E-Mail: hola@yagollopis.com
# Web de descarga: https://www.santiagodelgado.com/software/downpod-gui.html
#
# Eres libre de usar, modificar y redistribuir este programa. 
# Si realizas alguna mejora, por favor, mándame un correo-e con tu versión.
# 
# Este programa descarga todos los audios de un pódcast a partir de su feed.
#
# Hay que tener en cuenta que la descarga dependerá de la configuración que 
# tenga el alojamiento del pódcast, pudiéndose descargar todos los audios o
# sólo un número determinado.

import os
import re
import feedparser
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def download_podcasts(feed_url, download_dir, progress_bar):
    # Crear directorio si no existe
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Analizar el feed
    feed = feedparser.parse(feed_url)

    total_entries = len(feed.entries)
    if total_entries == 0:
        messagebox.showinfo("Sin episodios", "No se encontraron episodios en el feed proporcionado.")
        return

    progress_bar["maximum"] = total_entries

    for idx, entry in enumerate(feed.entries):
        # Suponiendo que el enlace al archivo MP3 está en 'enclosures'
        if 'enclosures' in entry and len(entry.enclosures) > 0:
            mp3_url = entry.enclosures[0].href
            mp3_title = entry.title.replace('/', '_')  # Limpia el título para usarlo como nombre de archivo
            mp3_title = re.sub(r'[^\w\-_\.]', '_', mp3_title)
            mp3_filename = os.path.join(download_dir, f"{mp3_title}.mp3")

            # Descargar el archivo MP3
            try:
                response = requests.get(mp3_url, stream=True)
                response.raise_for_status()  # Lanza un error si la solicitud falla
                with open(mp3_filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Descargado: {mp3_filename}")
            except requests.exceptions.RequestException as e:
                print(f"Error al descargar {mp3_url}: {e}")

        # Actualizar barra de progreso
        progress_bar["value"] = idx + 1
        progress_bar.update()

    messagebox.showinfo("Descarga completada", "Los episodios del podcast han sido descargados correctamente.")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        download_dir_entry.delete(0, tk.END)
        download_dir_entry.insert(0, directory)

def start_download():
    feed_url = feed_url_entry.get()
    download_dir = download_dir_entry.get()

    if not feed_url or not download_dir:
        messagebox.showerror("Error", "Por favor, ingrese la URL del feed y el directorio de descarga.")
        return

    progress_bar["value"] = 0
    download_podcasts(feed_url, download_dir, progress_bar)

# Crear la ventana principal
root = tk.Tk()
root.title("Downpod-gui v. 2.0")

# Etiqueta y campo para la URL del feed
tk.Label(root, text="URL del Feed del Podcast:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
feed_url_entry = tk.Entry(root, width=50)
feed_url_entry.grid(row=0, column=1, padx=10, pady=5)

# Etiqueta y campo para el directorio de descarga
tk.Label(root, text="Directorio de Descarga:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
download_dir_entry = tk.Entry(root, width=50)
download_dir_entry.grid(row=1, column=1, padx=10, pady=5)

# Botón para seleccionar el directorio
download_dir_button = tk.Button(root, text="Seleccionar...", command=select_directory)
download_dir_button.grid(row=1, column=2, padx=10, pady=5)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=2, column=0, columnspan=3, pady=10)

# Botón para iniciar la descarga
download_button = tk.Button(root, text="Descargar", command=start_download)
download_button.grid(row=3, column=0, columnspan=3, pady=10)

# Iniciar el bucle de la interfaz
tk.mainloop()
