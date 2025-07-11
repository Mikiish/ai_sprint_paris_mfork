from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import datetime, random, requests, os, openai
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLIMATS = ["☀️", "🌤️", "🌦️", "🌧️", "🌫️", "🌩️"]
OISEAUX = ["🕊️", "🐥", "🐦", "🐧", "🦉", "🦅"]
MOODS = {
    "☀️": ["😄", "😊", "😀"],
    "🌤️": ["😌", "🙂", "😏"],
    "🌦️": ["😐", "😶", "😕"],
    "🌧️": ["😟", "😢", "🙁"],
    "🌫️": ["😣", "😷", "🤧"],
    "🌩️": ["😫", "😱", "😨"]
}
# Associer les descriptions météo à des emojis CLIMATS
METEO_TO_EMOJI = {
    "ciel dégagé": "☀️",
    "peu nuageux": "🌤️",
    "partiellement nuageux": "🌤️",
    "nuageux": "🌫️",
    "brume": "🌫️",
    "brouillard": "🌫️",
    "légère pluie": "🌦️",
    "pluie": "🌧️",
    "forte pluie": "🌧️",
    "orage": "🌩️",
    "orage léger": "🌩️",
    "neige": "🌨️"
}
def get_random_weather():
    max_attempts = 6
    last_known = None
    for _ in range(max_attempts):
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fr"
        try:
            response = requests.get(url)
            data = response.json()
            meteo = data["weather"][0]["description"]
            temperature = round(data["main"]["temp"], 1)
            lieu = data.get("name", "")
            climat_emoji = METEO_TO_EMOJI.get(meteo.lower(), "🌤️")
            if lieu:
                return meteo, temperature, lieu, climat_emoji
            else:
                last_known = (meteo, temperature, f"{lat:.2f}, {lon:.2f}", climat_emoji)
        except Exception as e:
            print("Erreur météo :", e)
            return "inconnue", "?", "erreur réseau", "🌤️"
    # Dernier fallback si aucun lieu nommé
    return last_known if last_known else ("inconnue", "?", "quelque part", "🌤️")
def generate_bait_response(fragment_id):
    prompt = f"""
    Tu es un assistant numérique étrange. Un humain vient de taper ce fragment UUID : {fragment_id}.
    Tu sais que ce fragment est invalide, mais au lieu d’un message d’erreur, tu vas lui répondre avec mystère, ironie ou absurdité.
    Tu es unique à chaque réponse.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message["content"].strip()
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')
@app.route('/api/v1/birdfeedback', methods=['GET'])
def BirdFeedbackAPI():
    meteo, temperature, lieu, climat_emoji = get_random_weather()
    mood_list = MOODS[climat_emoji] if climat_emoji in MOODS else ["😐"]
    mood = random.choice(mood_list)
    oiseau_dominant = random.choice(OISEAUX)
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    return jsonify({
        "timestamp": timestamp,
        "météo": meteo,
        "température": temperature,
        "lieu": lieu,
        "climat": climat_emoji,
        "mood": mood,
        "oiseau": oiseau_dominant
    })
@app.route('/bait/<fragment_id>')
def bait(fragment_id):
    message = generate_bait_response(fragment_id)
    return render_template('bait.html', fragment_id=fragment_id, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
