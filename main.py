import pandas as pd
from flask import Flask, jsonify, request
import os

app = Flask(__name__)
CLIENT_TOKEN = os.environ.get("API_TOKEN")

dataframe = pd.read_excel("convidados_casamento.xlsx")
dataframe["Nome Convidado"] = dataframe["Nome Convidado"].str.strip()

def verificar_token():
    token = request.headers.get("Authorization")
    return token == f"Bearer {CLIENT_TOKEN}"

@app.route('/')
def homepage():
    return 'API está ON'

@app.route('/convidados')
def convidados():
    if not verificar_token():
        return jsonify({"erro": "Token inválido ou ausente"}), 401

    resultado = {}
    for index, row in dataframe.iterrows():
        resultado[index] = dict(row)
    return jsonify(resultado)

@app.route('/valor')
def valor():
    if not verificar_token():
        return jsonify({"erro": "Token inválido ou ausente"}), 401

    total = dataframe["Custo Convidado"].sum()
    resultado = {'Valor Total': str(total)}
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
