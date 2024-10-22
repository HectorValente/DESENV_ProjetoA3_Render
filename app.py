from flask import Flask, render_template, request, redirect, url_for, jsonify
import random

app = Flask(__name__)

# Dicionário para armazenar as salas e os jogadores conectados
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room', methods=['POST'])
def create_room():
    # Gera um código de sala aleatório de 3 dígitos
    room_code = str(random.randint(100, 999))
    rooms[room_code] = {"players": []}
    return jsonify({"room_code": room_code})

@app.route('/join_room', methods=['POST'])
def join_room():
    room_code = request.json.get('room_code')

    # Verifica se a sala existe e se não está cheia
    if room_code in rooms and len(rooms[room_code]["players"]) < 2:
        rooms[room_code]["players"].append(f"Player {len(rooms[room_code]['players']) + 1}")
        
        # Verifica se a sala está cheia
        if len(rooms[room_code]["players"]) == 2:
            return jsonify({"status": "ready", "players": rooms[room_code]["players"]})
        return jsonify({"status": "waiting"})
    
    return jsonify({"status": "full_or_invalid"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
