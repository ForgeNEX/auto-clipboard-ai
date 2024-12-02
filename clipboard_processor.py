import pyperclip
import keyboard
import requests
import time
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import sys
import json

# Cargar configuración desde config.json
try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        API_URL = config.get("API_URL", "http://localhost:11434/api/chat")
        MODEL = config.get("MODEL", "llama3.2")
        DEFAULT_PROMPT = config.get("DEFAULT_PROMPT", "Por favor, procesa el siguiente texto: {texto}")
except FileNotFoundError:
    print("Error: Archivo 'config.json' no encontrado.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: No se pudo parsear 'config.json': {e}")
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
    keyboard.add_hotkey("ctrl+alt+shift+o", process_clipboard)
    print("Presiona Ctrl+Alt+Shift+O para procesar el texto en el clipboard.")
    while True:
        time.sleep(0.1)

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

def tray_app():
    icon = Icon(
        "Clipboard AI",
        create_image(),
        menu=Menu(
            MenuItem("Salir", on_quit)
        )
    )
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=start_keyboard_listener, daemon=True).start()
    tray_app()
