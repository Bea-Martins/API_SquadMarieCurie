# import dos packges usados na aplicação
from flask import Flask, render_template
import urllib.request, json
import ssl

# desativa verificacao do certificado SSL
ssl._create_default_https_context = ssl._create_unverified_context

# inicializa uma aplicação flask
app = Flask(__name__)

# Rota para a página inicial do aplicativo. 
@app.route('/')
def get_list_elements_page():
    url = "https://rickandmortyapi.com/api/character/"
    response = urllib.request.urlopen(url) # solicitação HTTP para a url
    data = response.read() # lê e armazena os dados da resposta HTTP
    dict = json.loads(data) # converte os dados em um dicionário Python.

    return render_template("characters.html", characters=dict['results'])

@app.route('/profile/<id>')
def get_profile(id):
  url = "https://rickandmortyapi.com/api/character/" + id
  response = urllib.request.urlopen(url)
  data = response.read()
  dict = json.loads(data)

  return render_template("profile.html", profile=dict)

@app.route('/lista')
def get_list_characters():
  url = "https://rickandmortyapi.com/api/character"
  response = urllib.request.urlopen(url)
  characters = response.read()
  dict = json.loads(characters)

  characters_list = []

  for character in dict["results"]:
    character_data = {
      "name": character["name"],
      "status": character["status"]
    }
    characters_list.append(character_data)

# Retorna um dicionário contendo a chave "characters" com a lista de personagens.
  return {"characters": characters_list}