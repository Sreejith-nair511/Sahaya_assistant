import sys
import ollama
import pyttsx3
import fitz  # PyMuPDF
import speech_recognition as sr
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QFileDialog, QLineEdit, QMenuBar, QComboBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QThread, pyqtSignal, Qt

# Initialize text-to-speech engine with SAPI5
engine = pyttsx3.init()
engine.setProperty("rate", 180)  # Adjust speed for natural flow
engine.setProperty("volume", 1.0)  # Max volume

# Function to set voice dynamically
def set_voice(voice_name="Zira"):
    voices = engine.getProperty("voices")
    for voice in voices:
        if voice_name in voice.name:
            engine.setProperty("voice", voice.id)
            break

set_voice()

# Function to process AI response
def chat_with_ai(user_input):
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": user_input}])
    return response['message']['content']

# Background Thread for Summarizing PDFs
class PDFWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path

    def run(self):
        doc = fitz.open(self.pdf_path)
        text = "".join(page.get_text() for page in doc)
        text = text[:500] if len(text) > 500 else text
        summary_prompt = f"Summarize this document: {text}"
        summary = chat_with_ai(summary_prompt)
        self.finished.emit(summary)

# Main GUI Class
class AIChatbot(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Offline AI Assistant")
        self.setGeometry(100, 100, 600, 600)

        layout = QVBoxLayout()

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)

        self.menu_bar.addAction(exit_action)
        self.menu_bar.addAction(about_action)
        layout.setMenuBar(self.menu_bar)

        # Voice Selection Dropdown
        self.voice_selector = QComboBox(self)
        self.voice_selector.addItems([voice.name for voice in engine.getProperty("voices")])
        self.voice_selector.currentTextChanged.connect(self.change_voice)
        layout.addWidget(self.voice_selector)

        # Chat section
        self.label = QLabel("Enter your message:")
        layout.addWidget(self.label)

        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        self.chat_output = QTextEdit(self)
        self.chat_output.setReadOnly(True)
        layout.addWidget(self.chat_output)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.get_response)
        layout.addWidget(self.send_button)

        # Voice Assistant Section
        self.voice_button = QPushButton("🎤 Voice Assistant", self)
        self.voice_button.clicked.connect(self.voice_assistant)
        layout.addWidget(self.voice_button)

        # PDF Summarization Section
        self.upload_label = QLabel("Upload a PDF to summarize:")
        layout.addWidget(self.upload_label)

        self.upload_button = QPushButton("Select PDF", self)
        self.upload_button.clicked.connect(self.upload_pdf)
        layout.addWidget(self.upload_button)

        self.summary_output = QTextEdit(self)
        self.summary_output.setReadOnly(True)
        layout.addWidget(self.summary_output)

        self.setLayout(layout)

        # Apply Stylesheet for Colors
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
                font-size: 14px;
            }
            QTextEdit, QLineEdit {
                background-color: #3B4252;
                color: #ECEFF4;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #81A1C1;
                color: black;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)

    def get_response(self):
        user_input = self.text_input.text()
        if user_input:
            self.chat_output.append(f"You: {user_input}")
            ai_response = chat_with_ai(user_input)
            self.chat_output.append(f"AI: {ai_response}")
            self.speak(ai_response)
            self.text_input.clear()

    def upload_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.summary_output.append(f"Processing: {file_path} ...")
            self.worker = PDFWorker(file_path)
            self.worker.finished.connect(self.display_summary)
            self.worker.start()

    def display_summary(self, summary):
        self.summary_output.append(f"\nSummary:\n{summary}")
        self.speak(summary)

    def voice_assistant(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.chat_output.append("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                self.chat_output.append(f"You (voice): {user_input}")
                ai_response = chat_with_ai(user_input)
                self.chat_output.append(f"AI: {ai_response}")
                self.speak(ai_response)
            except sr.UnknownValueError:
                self.chat_output.append("Could not understand audio.")
            except sr.RequestError:
                self.chat_output.append("Could not request results.")

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def change_voice(self, voice_name):
        set_voice(voice_name)
        self.chat_output.append(f"Voice changed to {voice_name}.")

    def show_about(self):
        self.chat_output.append("AI Assistant v1.0\nCreated using PyQt6, Ollama, and Pyttsx3")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIChatbot()
    window.show()
    sys.exit(app.exec())
