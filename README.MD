# **Clipboard Processor with LLM Integration**

## **Project Overview**
This project is a **clipboard management tool** that integrates with a local Language Model (LLM) through an API. Its primary goal is to process text copied to the clipboard based on predefined tasks (prompts) and return the processed output back to the clipboard for further use.

---

## **Key Features**

### 1. **Clipboard Processing**
- Automatically processes text copied to the clipboard by sending it to the configured LLM.
- Once processed, the result is copied back to the clipboard, ready for pasting.

### 2. **Support for Multiple Tasks (Prompts)**
Tasks are defined in `config.json` and include:
- **Respond to Chats**: Generates professional responses using the `DEFAULT_PROMPT`.
- **Translate**: Translates the clipboard text into Spanish.
- **Create Summary**: Generates a concise, understandable summary of the clipboard text.

### 3. **Configurable Hotkeys**
Each task can be triggered using a dedicated hotkey, configurable in `config.json`. Examples:
- `ctrl+alt+shift+c`: Respond to Chats.
- `ctrl+alt+shift+t`: Translate.
- `ctrl+alt+shift+s`: Create Summary.

### 4. **System Tray Integration**
The system tray menu provides options to:
- Switch between tasks (prompts).
- Open `config.json` for quick edits.
- Exit the program.

### 5. **Audio Feedback**
- **`recording-end.wav`**: Played when text is successfully processed and copied back to the clipboard.
- **`recording-cancel.wav`**: Played if an error occurs during processing.

### 6. **Customizable Configuration**
- Key parameters like the **API URL**, prompts, and hotkeys are stored in `config.json`, enabling easy personalization.

### 7. **Local LLM Integration**
- The tool works with local LLMs (e.g., Ollama, llama.cpp) via an HTTP API for low latency and data privacy.

### 8. **Message History**
- Maintains a basic history of user queries and LLM responses for context when required.

---

## **Purpose and Use Cases**
- **Automation**: Simplifies repetitive tasks like translations, generating replies, or creating summaries.
- **Productivity**: Reduces time spent on text processing with clipboard integration.
- **Flexibility**: Supports multiple tasks with hotkeys and a system tray menu.
- **Customization**: Designed for advanced users leveraging local LLMs with tailored prompts.

---

## **How to Test and Compile the Script**

### **Testing the Script Locally**
1. **Clone or Download the Project**:
   ```bash
   git clone https://github.com/SergeWinters/clipboard-ollama.git
   cd clipboard-ollama
   ```

2. **Create and Activate a Virtual Environment**:
   - On **Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install pyperclip keyboard requests pystray pillow pyinstaller
   ```

4. **Edit the Configuration File (`config.json`)**:
   - Set the correct `API_URL` for your local LLM.
   - Customize prompts, hotkeys, and other settings as needed.

5. **Run the Script**:
   ```bash
   python clipboard_processor.py
   ```
   - Use the defined hotkeys or the system tray menu to test clipboard interactions.

---

### **Compiling the Script to an Executable**

#### **Windows**
1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Compile to `.exe`**:
   ```bash
   pyinstaller --onefile --windowed --icon=icon.ico clipboard_processor.py
   ```
   - `--onefile`: Bundles the application into a single executable.
   - `--windowed`: Prevents the terminal from appearing.
   - `--icon=icon.ico`: Uses a custom icon for the executable.

3. **Locate the Executable**:
   - The compiled `.exe` will be in the `dist` folder.

#### **macOS**
1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Compile to macOS App**:
   ```bash
   pyinstaller --onefile --windowed --icon=icon.icns clipboard_processor.py
   ```
   - Use `.icns` format for the macOS app icon.

3. **Run the App**:
   - The generated file will be in the `dist` folder. Double-click it to launch.

#### **Linux**
1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Compile to Executable**:
   ```bash
   pyinstaller --onefile clipboard_processor.py
   ```

3. **Run the Executable**:
   - Navigate to the `dist` folder and execute the file:
     ```bash
     ./clipboard_processor
     ```

---

### **Testing the Executable**
- Ensure `recording-end.wav` and `recording-cancel.wav` are in the same directory as the executable, or provide absolute paths in the script.
- Test all hotkeys and menu options to verify clipboard processing and audio feedback.

---

### **Troubleshooting**
1. **Missing Permissions**:
   - Run the compilation commands as an administrator if you encounter permission errors.

2. **Dependency Issues**:
   - Ensure all dependencies are installed using:
     ```bash
     pip install -r requirements.txt
     ```

3. **Icons Not Working**:
   - Verify the correct icon format:
     - **Windows**: Use `.ico`.
     - **macOS**: Use `.icns`.
     - **Linux**: Use `.png`.

4. **LLM Connection Issues**:
   - Ensure the LLM API is running and accessible at the specified `API_URL` in `config.json`.