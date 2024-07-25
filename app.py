from flask import Flask, render_template_string, request
import speech_recognition as sr
from deep_translator import GoogleTranslator

app = Flask(__name__)

recognizer = sr.Recognizer()
recognized_text = ""
translated_text = ""

# Supported languages including Tamil
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'hi': 'Hindi',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ru': 'Russian',
    'pt': 'Portuguese',
    'it': 'Italian',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'vi': 'Vietnamese',
    'ta': 'Tamil'  # Added Tamil
}

@app.route('/', methods=['GET', 'POST'])
def index():
    global recognized_text, translated_text
    if request.method == 'POST':
        language = request.form.get('language')
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                recognized_text = recognizer.recognize_google(audio).lower()
                translated_text = GoogleTranslator(source='auto', target=language).translate(recognized_text)
        except sr.UnknownValueError:
            recognized_text = "Could not understand audio"
            translated_text = ""

    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Speech Recognition and Translation</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                color: #333;
                text-align: center;
                padding: 0;
                margin: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
              }
              h1 {
                color: #fff;
                margin-bottom: 20px;
                font-size: 2.5rem;
              }
              form {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                max-width: 600px;
                width: 100%;
              }
              select, button {
                padding: 10px;
                margin-top: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 1rem;
              }
              button {
                background-color: #ff7e5f;
                color: white;
                cursor: pointer;
                border: none;
                font-size: 1rem;
              }
              button:hover {
                background-color: #feb47b;
              }
              p {
                font-size: 1.2rem;
                margin-top: 20px;
                color: #333;
              }
            </style>
          </head>
          <body>
            <h1>Speech Recognition and Translation</h1>
            <form method="post">
              <label for="language">Choose a language:</label>
              <select name="language" id="language">
                {% for code, name in supported_languages.items() %}
                  <option value="{{ code }}">{{ name }}</option>
                {% endfor %}
              </select>
              <br><br>
              <button type="submit">Speak and Translate</button>
            </form>
            <p>Your Speech: {{ recognized_text }}</p>
            <p>Translated Text: {{ translated_text }}</p>
          </body>
        </html>
    ''', recognized_text=recognized_text, translated_text=translated_text, supported_languages=SUPPORTED_LANGUAGES)

if __name__ == '__main__':
    app.run()
