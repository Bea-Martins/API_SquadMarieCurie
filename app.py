from flask import Flask, render_template, jsonify
import urllib.request
import json
import ssl

# desativa verificacao do certificado SSL
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

@app.route('/')
def get_list_elements_page():
    url = "https://rickandmortyapi.com/api/character/"
    with urllib.request.urlopen(url) as response:
        data = response.read()
        characters_dict = json.loads(data)
    return render_template("characters.html", characters=characters_dict['results'])

@app.route('/profile/<id>')
def get_profile(id):
    url = f"https://rickandmortyapi.com/api/character/{id}"
    with urllib.request.urlopen(url) as response:
        data = response.read()
        profile = json.loads(data)
    return render_template("profile.html", profile=profile)

@app.route('/profile/location/<id>')
def get_profile_locations(id):
    url = f"https://rickandmortyapi.com/api/location/{id}"
    with urllib.request.urlopen(url) as response:
        profile_location_data = response.read()
        profile_location_dict = json.loads(profile_location_data)

    residents = []
    for resident_url in profile_location_dict['residents']:
        with urllib.request.urlopen(resident_url) as response:
            resident_data = response.read()
            resident_dict = json.loads(resident_data)
            residents.append({'name': resident_dict['name'], 'id': resident_dict['id']})

    return render_template("profile-location.html", prof_location=profile_location_dict, residents=residents)

@app.route('/location/<id>')
def get_locations(id):
    url = f"https://rickandmortyapi.com/api/location/{id}"
    with urllib.request.urlopen(url) as response:
        location_data = response.read()
        location_dict = json.loads(location_data)
    
    residents = []
    for resident_url in location_dict['residents']:
        with urllib.request.urlopen(resident_url) as response:
            resident_data = response.read()
            resident_dict = json.loads(resident_data)
            residents.append({'name': resident_dict['name'], 'id': resident_dict['id']})
    
    return render_template("location.html", location=location_dict, residents=residents)

@app.route("/locations")
def get_list_locations():
    url = "https://rickandmortyapi.com/api/location/"
    with urllib.request.urlopen(url) as response:
        locations_data = response.read()
        locations_dict = json.loads(locations_data)
    
    locations = []
    for location in locations_dict["results"]:
        locations.append({
            "id": location["id"],
            "name": location["name"],
            "type": location["type"],
            "dimension": location["dimension"]
        })
    return render_template("locations.html", locations=locations)

@app.route("/episodes")
def get_list_episodes():
    url = "https://rickandmortyapi.com/api/episode"
    with urllib.request.urlopen(url) as response:
        episodes_data = response.read()
        episodes_dict = json.loads(episodes_data)
    
    episodes = []
    for episode in episodes_dict["results"]:
        episodes.append({
           "id": episode["id"],
            "name": episode["name"],
            "air_date": episode["air_date"],
            "episode": episode["episode"]
        })
    
    return render_template("episodes.html", episodes=episodes)

@app.route('/lista')
def get_list_characters():
    url = "https://rickandmortyapi.com/api/character"
    with urllib.request.urlopen(url) as response:
        characters_data = response.read()
        characters_dict = json.loads(characters_data)
    
    characters_list = []
    for character in characters_dict["results"]:
        characters_list.append({
            "name": character["name"],
            "status": character["status"]
        })
    
    return jsonify(characters=characters_list)

@app.route('/episode/<int:id>')
def episode(id):
    episode_url = f'https://rickandmortyapi.com/api/episode/{id}'
    with urllib.request.urlopen(episode_url) as response:
        episode_data = json.loads(response.read())

    characters_info = []
    for character_url in episode_data['characters']:
        with urllib.request.urlopen(character_url) as response:
            character_data = json.loads(response.read())
            characters_info.append({
                'name': character_data['name'],
                'image': character_data['image'],
                'url': character_data['url']
            })

    episode_info = {
        'name': episode_data['name'],
        'air_date': episode_data['air_date'],
        'episode': episode_data['episode'],
        'characters': characters_info
    }

    return render_template('episode.html', episode=episode_info)

if __name__ == '__main__':
    app.run(debug=True)
