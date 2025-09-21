from flask import Flask, render_template, jsonify
from google import genai
import random 

client = genai.Client(api_key="AIzaSyDGJ_tQZFbrLUCIfYwi_9OnRs-L-nQqKfs")

app = Flask(__name__)

# The list of known words is now part of this file
words_to_use = [
    "Auto", "Haus", "Tag", "Nacht", "Kind", "Frau", "Mann", "Freund", "Freundin", "Leute",
    "Arbeit", "Schule", "Universität", "Stadt", "Dorf", "Welt", "Leben", "Hand", "Kopf", "Herz",
    "Tür", "Fenster", "Straße", "Platz", "Bahnhof", "Flughafen", "Zimmer", "Bett", "Tisch", "Stuhl",
    "Buch", "Zeitung", "Brief", "Telefon", "Computer", "Internet", "Bild", "Film", "Musik", "Spiel",
    "Essen", "Trinken", "Brot", "Wasser", "Milch", "Kaffee", "Tee", "Bier", "Wein", "Fleisch",
    "Obst", "Gemüse", "Apfel", "Banane", "Kartoffel", "Tomate", "Reis", "Zucker", "Salz", "Ei",
    "Tag", "Woche", "Monat", "Jahr", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag",
    "Sonntag", "Frühling", "Sommer", "Herbst", "Winter", "Uhrzeit", "Minute", "Stunde", "Sekunde", "Moment",
    "heiß", "kalt", "warm", "neu", "alt", "jung", "schön", "hässlich", "freundlich", "nett",
    "langsam", "schnell", "früh", "spät", "richtig", "falsch", "wahr", "wichtig", "leicht", "schwer"
]

@app.route("/")
def home_page():
    # Call the function to get the data and pass it to the template
    data = get_data()
    return render_template('index.html', word=data['word'], definition=data['definition'])

@app.route("/get_data")
def get_data():
    try:
        current_word = random.choice(words_to_use)
    except IndexError:
        return jsonify({"error": "No more words left!"})
        
    language = "german"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"I will provide a list of {language} words and one new word not in that list. Using only words from the list, write an accurate, descriptive definition for the new word with simple tense conjugations as needed, clear enough for a learner to infer the meaning. Please use longer definitions if needed. It should be very easy to understand what the word is. You do not need to specify size unless it is very tiny (close to the size of a pin) or very large (like a mountain, skyscraper, etc.) or it's size is relative to the definition of another item (for example, calling a semi truck a big car). You do not have to say the word, as I am printing that above your response. Here is the list of known words: {words_to_use}. And, here is the new word: {current_word}",
    )
    definition = response.text
    return {"word": current_word, "definition": definition}

if __name__ == '__main__':
    app.run(debug=True)
