import requests
from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

API_URL = "https://gemma-api-url.com/inference" 
TRAIN_URL = "https://gemma-api-url.com/train"    
API_KEY = "YOUR_GEMMA_API_KEY"                 

ELIGIBLE_LANGUAGES = {
    "en": "Inglês (Americano)",
    "ar": "Árabe (Padrão Moderno)",
    "zh-CN": "Chinês (Simplificado)",
    "zh-TW": "Chinês (Tradicional)",
    "nl": "Holandês",
    "en-GB": "Inglês (Britânico)",
    "fr": "Francês (Europeu)",
    "de": "Alemão",
    "it": "Italiano",
    "ja": "Japonês",
    "ko": "Coreano",
    "pl": "Polonês",
    "pt-BR": "Português (Brasileiro)",
    "ru": "Russo",
    "es": "Espanhol (Europeu)",
    "th": "Tailandês",
    "tr": "Turco",
    "es-LA": "Espanhol (Latino-Americano)",
}

@app.route('/')
def home():
    return render_template('index.html', languages=ELIGIBLE_LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text')
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    if not text or not source_language or not target_language:
        return render_template('index.html', languages=ELIGIBLE_LANGUAGES, error="Por favor, preencha todos os campos.")

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'source_language': source_language,
        'target_language': target_language,
        'text': text
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        translation = response.json().get('translation', 'Tradução não encontrada.')
        return render_template(
            'index.html',
            languages=ELIGIBLE_LANGUAGES,
            original_text=text,
            translated_text=translation,
            source_language=source_language,
            target_language=target_language
        )
    except requests.exceptions.RequestException as e:
        return render_template(
            'index.html',
            languages=ELIGIBLE_LANGUAGES,
            error=f"Erro ao realizar a tradução: {str(e)}"
        )

@app.route('/train', methods=['POST'])
def train():
    file = request.files.get('file')
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    if not file or not source_language or not target_language:
        return render_template('index.html', languages=ELIGIBLE_LANGUAGES, error="Por favor, preencha todos os campos e envie um arquivo.")

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    files = {
        'file': (file.filename, file, file.content_type)
    }

    data = {
        'source_language': source_language,
        'target_language': target_language
    }

    try:
        response = requests.post(TRAIN_URL, data=data, files=files, headers=headers)
        response.raise_for_status()
        message = "Treinamento iniciado com sucesso! Acompanhe o progresso no painel."
        return render_template('index.html', languages=ELIGIBLE_LANGUAGES, training_status=message)
    except requests.exceptions.RequestException as e:
        return render_template(
            'index.html',
            languages=ELIGIBLE_LANGUAGES,
            error=f"Erro ao iniciar o treinamento: {str(e)}"
        )

@app.route('/export', methods=['POST'])
def export_csv():
    translations = [
        {"ID": 1, "Input": "Hello, how are you?", "Output": "Olá, como você está?"},
        {"ID": 2, "Input": "Good morning!", "Output": "Bom dia!"},
    ]

    df = pd.DataFrame(translations)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="submission.csv"
    )

if __name__ == '__main__':
    app.run(debug=True)
