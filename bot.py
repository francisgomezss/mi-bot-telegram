import telebot
import requests
import re

TOKEN = "8715656299:AAGrAp4-_9a2jlE0ZKJ5Tk9UlP3hOaVhacc"
GEMINI_KEY = "AQ.Ab8RN6Ik-5aAZsKT8PrnQf8WQBJ0aSAJ-egNT2qcf-8efceDSg"

bot = telebot.TeleBot(TOKEN)

def pronunciacion(palabra):
    simples = {
        'beautiful': 'biutiful',
        'hello': 'jelou', 
        'happy': 'japi',
        'run': 'ran',
    }
    return simples.get(palabra.lower(), palabra.lower())

@bot.message_handler(commands=['start'])
def start(m):
    m.reply_text("Envía una palabra en inglés y te digo cómo se pronuncia y qué significa")

@bot.message_handler(func=lambda m: True)
def traducir(m):
    palabra = m.text.split()[0]
    
    # Llamar a Gemini simple
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"
    
    prompt = f"Traduce '{palabra}' al español. Responde SOLO la traducción, nada más"
    
    try:
        respuesta = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        })
        data = respuesta.json()
        traduccion = data['candidates'][0]['content']['parts'][0]['text']
    except:
        traduccion = "traducción no disponible"
    
    pron = pronunciacion(palabra)
    
    m.reply_text(f"📖 {palabra}\n🔊 {pron}\n🇪🇸 {traduccion}")

bot.infinity_polling()
