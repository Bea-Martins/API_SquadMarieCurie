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

@app.route('/location/<id>')
def get_locations(id):
    url = "https://rickandmortyapi.com/api/location/" + id
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    residents = []
    for resident_url in dict['residents']:
        response = urllib.request.urlopen(resident_url)
        data = response.read()
        resident_dict = json.loads(data)
        residents.append({'name': resident_dict['name'], 'id': resident_dict['id']})

    return render_template("location.html", location=dict, residents=residents)

@app.route("/locations")
def get_list_locations():
    url = "https://rickandmortyapi.com/api/location/"
    response = urllib.request.urlopen(url) # abrir url
    locations_data = response.read() # ler os dados recebidos
    locations_dict = json.loads(locations_data) # formatar para json

    locations = [] # criar uma lista

    for location in locations_dict ["results"]:
        location_info = {
            "name": location["name"],
            "type": location["type"],
            "dimension": location["dimension"]
        }

        locations.append(location_info)
    return render_template("locations.html", locations=locations)

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

    @app.route('/episode/<int:id>')
def episode(id):
    # Obtem dos dados do episódio
    episode_response = requests.get(f'https://rickandmortyapi.com/api/episode/{id}')
    episode_data = episode_response.json()

    # Inicializa da lista para armazenar informações dos personagens
    characters_info = []

    # Obtem das informações de cada personagem que aparece no episódio
    for character_url in episode_data['characters']:
        character_response = requests.get(character_url)
        character_data = character_response.json()
        characters_info.append({
            'name': character_data['name'],
            'image': character_data['image'],
            'url': character_data['url']
        })

    # Prepara dos dados para serem enviados ao template
    episode_info = {
        'name': episode_data['name'],
        'air_date': episode_data['air_date'],
        'episode': episode_data['episode'],
        'characters': characters_info
    }

    # Renderiza do template, passando os dados do episódio
    return render_template('episode.html', episode=episode_info)

if __name__ == '__main__':
    app.run(debug=True)
