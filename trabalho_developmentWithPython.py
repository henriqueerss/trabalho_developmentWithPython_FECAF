# INSTALANDO A APLICAÇÃO:
# python3 -m venv venv
# source venv/bin/activate
# pip install flask flask-cors

# TRABALHO DE DESENVOLVIMENTO COM PYTHON - 4º SEMESTRE
# CIÊNCIA DA COMPUTAÇÃO - UNIFECAF - 2025

"""
    Nome: Bruno Menezes Gomes, RA: 108775
    Nome: Henrique Ribeiro Siqueira, RA: 50129
"""

from flask import Flask, Response, request
from flask_cors import CORS
import json

app = Flask(__name__)

# Garante que o JSON não será ASCII (acentos, emojis etc.)
app.config["JSON_AS_ASCII"] = False

# Configurando CORS
CORS(app)

def json_response(payload, status=200, headers=None):
    """Retorna JSON com Content-Type explícito em UTF-8."""
    resp = Response(
        json.dumps(payload, ensure_ascii=False),
        status=status,
        mimetype="application/json; charset=utf-8"
    )
    if headers:
        for k, v in headers.items():
            resp.headers[k] = v
    return resp

# "Banco de dados" em memória
personagens = [
    {"id": 1, "nome": "Link", "classe": "Arqueira", "poder": "Precisão", "fraqueza": "Combate corpo a corpo"},
    {"id": 2, "nome": "Mario", "classe": "Encanador", "poder": "nenhum", "fraqueza": "Inimigos (ex. Goomba, Koopa, etc.)"},
    {"id": 3, "nome": "Pikachu", "classe": "Elétrico", "poder": "Choque do trovão", "fraqueza": "Terra"},
    {"id": 4, "nome": "Luigi", "classe": "Encanador", "poder": "nenhum", "fraqueza": "Inimigos (ex. Goomba, Koopa, etc.)"},
    {"id": 5, "nome": "Zelda", "classe": "Maga", "poder": "Magia", "fraqueza": "Combate corpo a corpo"},
    {"id": 6, "nome": "Bowser", "classe": "Rei dos Koopas", "poder": "Força bruta", "fraqueza": "Velocidade"},
    {"id": 7, "nome": "Charizard", "classe": "Fogo/Voador", "poder": "Lança-chamas", "fraqueza": "Água"},
    {"id": 8, "nome": "Peach", "classe": "Princesa", "poder": "Coração puro", "fraqueza": "Inimigos (ex. Bowser)"},
    {"id": 9, "nome": "Yoshi", "classe": "Dinossauro", "poder": "Língua longa", "fraqueza": "Velocidade"},
    {"id": 10, "nome": "Ganondorf", "classe": "Rei dos Gerudo", "poder": "Magia negra", "fraqueza": "Luz"},
    {"id": 11, "nome": "Donkey Kong", "classe": "Gorila", "poder": "Força bruta", "fraqueza": "Velocidade"},
    {"id": 12, "nome": "Wario", "classe": "Aventureiro", "poder": "Força bruta", "fraqueza": "Ganância"},
    {"id": 13, "nome": "Mewtwo", "classe": "Psíquico", "poder": "Telecinese", "fraqueza": "Inimigos (ex. Darkrai)"},
    {"id": 14, "nome": "Waluigi", "classe": "Aventureiro", "poder": "Agilidade", "fraqueza": "Ganância"},
]

# Utilitário
def find_index_by_id(pid: int):
    for i, p in enumerate(personagens):
        if p.get("id") == pid:
            return i
    return None

# GET - listar todos os personagens
@app.route("/personagens", methods=["GET"])
def listar_personagens():
    return json_response(personagens)

# GET - selecionar o personagem pelo id
@app.route("/personagens/<int:personagem_id>", methods=["GET"])
def obter_personagem(personagem_id):
    personagem = next((p for p in personagens if p["id"] == personagem_id), None)
    if personagem:
        return json_response(personagem)
    return json_response({"error": "Personagem não encontrado"}, status=404)

# POST - criar um novo personagem
@app.route("/personagens", methods=["POST"])
def criar_personagem():
    data = request.get_json(silent=True) or {}

    # Validação simples
    required = {"id", "nome", "classe", "poder", "fraqueza"}
    missing = [k for k in required if k not in data]
    if missing:
        return json_response({"error": f"Campos obrigatórios ausentes: {', '.join(missing)}"}, status=400)

    if any(p["id"] == data["id"] for p in personagens):
        return json_response({"error": f"Já existe personagem com id={data['id']}"}, status=409)

    personagens.append(data)
    return json_response(data, status=201, headers={"Location": f"/personagens/{data['id']}"})

# PUT - atualizar um personagem existente (não altera o id)
@app.route("/personagens/<int:personagem_id>", methods=["PUT"])
def atualizar_personagem(personagem_id):
    data = request.get_json(silent=True) or {}
    idx = find_index_by_id(personagem_id)
    if idx is None:
        return json_response({"error": "Personagem não encontrado"}, status=404)

    # Evita troca de id via payload
    if "id" in data and data["id"] != personagem_id:
        return json_response({"error": "Não é permitido alterar o 'id' do personagem"}, status=400)

    personagens[idx].update({k: v for k, v in data.items() if k != "id"})
    return json_response(personagens[idx])

# DELETE - remover personagem
@app.route("/personagens/<int:personagem_id>", methods=["DELETE"])
def excluir_personagem(personagem_id):
    global personagens
    before = len(personagens)
    personagens = [p for p in personagens if p["id"] != personagem_id]
    if len(personagens) == before:
        return json_response({"error": "Personagem não encontrado"}, status=404)
    return json_response({"msg": f"Personagem {personagem_id} removido"})

if __name__ == "__main__":
    app.run(debug=True, port=3344)
