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
import winsound  # Para reproducir sonidos en Windows

# Ruta del archivo de configuración
CONFIG_FILE = "config.json"
SOUND_SUCCESS = "recording-end.wav"
SOUND_ERROR = "recording-cancel.wav"

# Cargar configuración desde config.json
try:
    with open(CONFIG_FILE, "r") as config_file:
        config = json.load(config_file)
        API_URL = config.get("API_URL", "http://localhost:11434/api/chat")
        MODEL = config.get("MODEL", "llama3.2")
        DEFAULT_PROMPT = config.get("DEFAULT_PROMPT", "Por favor, procesa el siguiente texto: {texto}")
        PROMPT_TRANSLATE = config.get("PROMPT_TRANSLATE", "Traduce al español: {texto}")
        PROMPT_SUMMARY = config.get("PROMPT_SUMMARY", "Crea un sumario del siguiente texto: {texto}")
        HOTKEY_CHAT = config.get("HOTKEY_CHAT", "ctrl+alt+shift+1")
        HOTKEY_TRANSLATE = config.get("HOTKEY_TRANSLATE", "ctrl+alt+shift+2")
        HOTKEY_SUMMARY = config.get("HOTKEY_SUMMARY", "ctrl+alt+shift+3")
except FileNotFoundError:
    print(f"Error: Archivo '{CONFIG_FILE}' no encontrado.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: No se pudo parsear '{CONFIG_FILE}': {e}")
    sys.exit(1)

# Historial de mensajes
message_history = []
current_prompt = DEFAULT_PROMPT  # Prompt inicial

def play_sound(sound_file):
    try:
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
    except Exception as e:
        print(f"Error al reproducir el sonido '{sound_file}': {e}")

def query_ollama_api(input_text):
    global message_history
    message_history.append({"role": "user", "content": input_text})

    request_body = {
        "model": MODEL,
        "messages": [{"role": "system", "content": current_prompt}] + message_history,
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
        prompt_text = current_prompt.replace("{texto}", original_text)
        processed_text = query_ollama_api(prompt_text)
        if "Error" not in processed_text:
            pyperclip.copy(processed_text)
            play_sound(SOUND_SUCCESS)
        else:
            print(processed_text)
            play_sound(SOUND_ERROR)

def set_prompt_and_process(prompt):
    global current_prompt
    current_prompt = prompt
    process_clipboard()

def start_keyboard_listener():
    keyboard.add_hotkey(HOTKEY_CHAT, lambda: set_prompt_and_process(DEFAULT_PROMPT))
    keyboard.add_hotkey(HOTKEY_TRANSLATE, lambda: set_prompt_and_process(PROMPT_TRANSLATE))
    keyboard.add_hotkey(HOTKEY_SUMMARY, lambda: set_prompt_and_process(PROMPT_SUMMARY))
    print(f"Hotkeys activados:")
    print(f" - Responder a chats: {HOTKEY_CHAT}")
    print(f" - Traducir: {HOTKEY_TRANSLATE}")
    print(f" - Crear sumario: {HOTKEY_SUMMARY}")
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

def tray_app():
    icon = Icon(
        "Clipboard AI",
        Image.open("icon.ico"),
        menu=Menu(
            MenuItem("Responder a Chats", lambda: set_prompt_and_process(DEFAULT_PROMPT)),
            MenuItem("Traducir", lambda: set_prompt_and_process(PROMPT_TRANSLATE)),
            MenuItem("Crear Sumario", lambda: set_prompt_and_process(PROMPT_SUMMARY)),
            MenuItem("Editar Configuración", open_config_file),
            MenuItem("Salir", on_quit)
        )
    )
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=start_keyboard_listener, daemon=True).start()
    tray_app()
