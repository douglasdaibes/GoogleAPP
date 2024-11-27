import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# API do modelo Gemma
API_URL = "https://gemma-api-url.com/inference"  # Substitua pela URL da API do Gemma
TRAIN_URL = "https://gemma-api-url.com/train"    # Substitua pela URL de treinamento
API_KEY = "YOUR_GEMMA_API_KEY"                  # Substitua pela sua chave de API

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    # Captura os dados do formulário
    text = request.form.get('text')
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    # Valida entrada
    if not text or not source_language or not target_language:
        return render_template('index.html', error="Por favor, preencha todos os campos.")

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
        # Envia solicitação à API
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        translation = response.json().get('translation', 'Tradução não encontrada.')
        return render_template(
            'index.html',
            original_text=text,
            translated_text=translation,
            source_language=source_language,
            target_language=target_language
        )
    except requests.exceptions.RequestException as e:
        return render_template(
            'index.html',
            error=f"Erro ao realizar a tradução: {str(e)}"
        )

@app.route('/train', methods=['POST'])
def train():
    file = request.files.get('file')
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    # Valida entrada
    if not file or not source_language or not target_language:
        return render_template('index.html', error="Por favor, preencha todos os campos e envie um arquivo.")

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
        # Envia solicitação de treinamento à API
        response = requests.post(TRAIN_URL, data=data, files=files, headers=headers)
        response.raise_for_status()
        message = "Treinamento iniciado com sucesso! Acompanhe o progresso no painel."
        return render_template('index.html', training_status=message)
    except requests.exceptions.RequestException as e:
        return render_template(
            'index.html',
            error=f"Erro ao iniciar o treinamento: {str(e)}"
        )

if __name__ == '__main__':
    app.run(debug=True)
