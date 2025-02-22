<h1>Sahaya - AI Assistant</h1>

Sahaya is a local AI-powered desktop assistant built using PyQt6, Ollama, and Pyttsx3 for natural language interaction and PDF summarization. The assistant supports both text and voice input and provides spoken responses.

<h2>Features</h2>

Interactive Chat: Communicate with the AI assistant via text input.

Voice Interaction: Speak to the assistant using the microphone.

PDF Summarization: Upload PDFs and get AI-generated summaries.

Text-to-Speech (TTS): AI responses are spoken aloud.

Customizable Voices: Choose from multiple voices available on the system.

Dark Mode UI: Aesthetic and modern PyQt6-based user interface.

<h3>Installation</h3>

Prerequisites

Python 3.10+

Ollama (for AI processing)

PyQt6

Pyttsx3

SpeechRecognition

PyMuPDF (fitz)

PyInstaller (for building the .exe file)

Steps

Clone this repository:

git clone https://github.com/yourusername/sahaya.git
cd sahaya

Install dependencies:

pip install -r requirements.txt

Run the assistant:

python gui_assistant.py

Converting to Executable (.exe)

To create a standalone executable file:

pyinstaller --onefile --windowed gui_assistant.py

The executable will be found in the dist/ folder.

Usage

Open Sahaya and enter text to chat with the assistant.

Click the Voice Assistant button to use speech recognition.

Upload a PDF file to generate a summary.

Change the assistant's voice using the dropdown menu.

Contributing

Feel free to fork this repository and submit pull requests. Contributions are welcome!

License

This project is licensed under the MIT License.

Made with ❤️ by Sreejith

