Clipboard Processor with LLM Integration

Project Overview
This project is a clipboard management tool that integrates with a local Language Model (LLM) through an API. Its primary goal is to process text copied to the clipboard based on predefined tasks (prompts) and return the processed output back to the clipboard for further use.

Key Features
1. Clipboard Processing
Automatically processes text copied to the clipboard by sending it to the configured LLM for processing.
Once the processing is complete, the result is copied back to the clipboard, ready for pasting.
2. Support for Multiple Tasks (Prompts)
The project supports the following tasks, defined as prompts in config.json:

Respond to Chats: Uses the DEFAULT_PROMPT to generate professional responses to social media or chat texts.
Translate: Translates the clipboard text into Spanish.
Create Summary: Generates a short, understandable summary of the clipboard text.

3. Configurable Hotkeys
Each task can be triggered using a dedicated hotkey, configurable in config.json. Examples:

ctrl+alt+shift+c: Respond to Chats.
ctrl+alt+shift+t: Translate.
ctrl+alt+shift+s: Create Summary.

4. System Tray Integration
The project features a system tray icon with the following menu options:

Switch between tasks (prompts).
Open config.json for quick configuration edits.
Exit the program.

5. Audio Feedback
recording-end.wav: Played when the text is successfully processed and copied back to the clipboard.
recording-cancel.wav: Played if an error occurs during processing.

6. Customizable Configuration
Key parameters like the API URL, prompts, and hotkeys are stored in config.json, making it easy to personalize without modifying the code.

7. Local LLM Integration
The tool is designed to work with local LLMs (e.g., Ollama, llama.cpp) via an HTTP API, ensuring low latency and data privacy.

8. Message History
A basic history of user queries and assistant responses is maintained to provide context when required by the LLM.

Purpose and Use Cases
Automation: Simplifies repetitive tasks like translations, generating professional replies, or creating summaries.
Productivity: Reduces time spent on text processing by integrating directly with the clipboard.
Flexibility: Supports multiple tasks with quick switching via hotkeys or the system tray menu.
Customization: Designed for advanced users who want to leverage a local LLM with tailored prompts.

How to Test and Compile the Script
Testing the Script Locally
To run the script, you can set up a Python virtual environment (venv) and install the required dependencies. Follow these steps:

Clone or Download the Project:

https://github.com/SergeWinters/clipboard-ollama.git
cd clipboard-ollama.git
Create and Activate a Virtual Environment:

On Windows:
python -m venv venv
.\venv\Scripts\activate
On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Install Dependencies:
pip install pyperclip keyboard requests pystray pillow pyinstaller

Edit the Configuration File (config.json):

Set the correct API_URL for your local LLM.
Customize prompts, hotkeys, and other settings as needed.

Run the Script:
python clipboard_processor.py
Once running, you can use the defined hotkeys or the system tray menu to test clipboard interactions.

Compiling the Script to an Executable
You can compile the script into a standalone executable for Windows, macOS, or Linux using PyInstaller.

Windows
Install PyInstaller:

pip install pyinstaller
Compile to .exe:

pyinstaller --onefile --windowed --icon=icon.ico clipboard_processor.py
--onefile: Bundles the application into a single executable.
--windowed: Prevents the terminal from appearing.
--icon=icon.ico: Uses a custom icon for the executable.

Locate the Executable:
The compiled .exe will be in the dist folder.

macOS
Install PyInstaller:

pip install pyinstaller
Compile to macOS App:

pyinstaller --onefile --windowed --icon=icon.icns clipboard_processor.py
Use .icns format for the macOS app icon.
Run the App:

The generated file will be in the dist folder. Double-click it to launch.

Linux
Install PyInstaller:

pip install pyinstaller
Compile to Executable:

pyinstaller --onefile clipboard_processor.py
Run the Executable:

Navigate to the dist folder and execute the file:
./clipboard_processor
Testing the Executable
Ensure you have recording-end.wav and recording-cancel.wav in the same directory as the executable, or modify the script to provide absolute paths.
Test each hotkey and menu option to verify clipboard processing and audio feedback.
Troubleshooting
Missing Permissions:

Run the compilation commands as an administrator if you encounter permission errors.
Dependency Issues:

Ensure all dependencies in requirements.txt are installed.
Icons Not Working:

Verify the icon format:
Windows: Use .ico.
macOS: Use .icns.
Linux: Use .png.
LLM Connection Issues:

Ensure the LLM API is running and accessible at the specified API_URL in config.json.
