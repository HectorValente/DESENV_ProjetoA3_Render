import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# URL da API externa para validação do login
API_URL = 'https://projetoa3-glitch.glitch.me/api/jogador/'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    # Fazendo o request para a API externa
    try:
        response = requests.get(API_URL + email)
        # Verifica se a resposta da API foi bem-sucedida (status code 200)
        if response.status_code == 404:
            response = requests.post(API_URL, json={"nome": nome, "email": email, "senha": senha})
            if response.status_code == 200:
                data = response.json()
                # Supondo que a API retorna um campo 'valid' que indica se as credenciais são válidas
                if data.get('valid'):
                    return render_template('home.html', email=email)
                else:
                    return render_template('error.html', message=data.get('message', 'Email ou senha incorretos.'))
            else:
                return render_template('error.html', message='Erro ao se comunicar com a API. Tente novamente mais tarde.')
    except requests.exceptions.RequestException as e:
        return render_template('error.html', message=f'Erro de conexão: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)