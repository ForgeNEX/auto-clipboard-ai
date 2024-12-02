import pyperclip
import keyboard
import requests
import time
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import sys
import json
import os
import subprocess

# Ruta del archivo de configuración
CONFIG_FILE = "config.json"

# Cargar configuración desde config.json
try:
    with open(CONFIG_FILE, "r") as config_file:
        config = json.load(config_file)
        API_URL = config.get("API_URL", "http://localhost:11434/api/chat")
        MODEL = config.get("MODEL", "llama3.2")
        DEFAULT_PROMPT = config.get("DEFAULT_PROMPT", "Por favor, procesa el siguiente texto: {texto}")
        HOTKEY = config.get("HOTKEY", "ctrl+alt+shift+o")
except FileNotFoundError:
    print(f"Error: Archivo '{CONFIG_FILE}' no encontrado.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: No se pudo parsear '{CONFIG_FILE}': {e}")
    sys.exit(1)

# Historial de mensajes
message_history = []

def query_ollama_api(input_text):
    global message_history
    message_history.append({"role": "user", "content": input_text})

    request_body = {
        "model": MODEL,
        "messages": [{"role": "system", "content": DEFAULT_PROMPT}] + message_history,
        "stream": False,
        "options": {
            "top_p": 0.7,
            "temperature": 0.8,
            "repeat_penalty": 1.2
        }
    }

    try:
        response = requests.post(API_URL, json=request_body)
        response.raise_for_status()
        response_data = response.json()
        if "message" in response_data and response_data["message"]["content"]:
            message_history.append({"role": "assistant", "content": response_data["message"]["content"]})
            return response_data["message"]["content"]
        else:
            return "Error: respuesta vacía o no válida."
    except requests.RequestException as e:
        return f"Error al conectar con la API: {e}"

def process_clipboard():
    original_text = pyperclip.paste()
    if original_text.strip():
        processed_text = query_ollama_api(original_text)
        pyperclip.copy(processed_text)

def start_keyboard_listener():
    global HOTKEY
    keyboard.add_hotkey(HOTKEY, process_clipboard)
    print(f"Presiona {HOTKEY} para procesar el texto en el clipboard.")
    while True:
        time.sleep(0.1)

def update_hotkey(new_hotkey):
    global HOTKEY
    keyboard.remove_hotkey(HOTKEY)
    HOTKEY = new_hotkey
    keyboard.add_hotkey(HOTKEY, process_clipboard)
    print(f"Combinación de teclas cambiada a {HOTKEY}.")

    # Actualizar el archivo de configuración
    try:
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
        config["HOTKEY"] = new_hotkey
        with open(CONFIG_FILE, "w") as config_file:
            json.dump(config, config_file, indent=4)
        print("Archivo de configuración actualizado.")
    except Exception as e:
        print(f"Error al actualizar '{CONFIG_FILE}': {e}")

def create_image():
    width, height = 64, 64
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill=(30, 144, 255))
    draw.text((width // 4, height // 4), "AI", fill=(255, 255, 255))
    return image

def on_quit(icon, item):
    icon.stop()
    sys.exit()

def open_config_file(icon, item):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(CONFIG_FILE)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.call(["xdg-open", CONFIG_FILE])
        else:
            print("Sistema operativo no soportado para abrir el archivo.")
    except Exception as e:
        print(f"Error al abrir '{CONFIG_FILE}': {e}")

def change_hotkey(icon, item):
    new_hotkey = input("Introduce la nueva combinación de teclas (ejemplo: ctrl+shift+x): ").strip()
    if new_hotkey:
        update_hotkey(new_hotkey)

def tray_app():
    icon = Icon(
        "Clipboard AI",
        create_image(),
        menu=Menu(
            MenuItem("Cambiar Combinación de Teclas", change_hotkey),
            MenuItem("Editar Configuración", open_config_file),
            MenuItem("Salir", on_quit)
        )
    )
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=start_keyboard_listener, daemon=True).start()
    tray_app()
