from flask import Flask, request, send_file
import edge_tts
import asyncio
import os

app = Flask(__name__)

async def generate_tts(text, voice, file_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)

@app.route('/api/tts', methods=['GET'])
def tts():
    # Get text from the URL, default to Maisie
    text = request.args.get('text', 'Hello from Vercel!')
    voice = request.args.get('voice', 'en-GB-MaisieNeural')
    
    # Vercel only allows writing to the /tmp folder
    output_path = f'/tmp/output_{os.urandom(4).hex()}.mp3'
    
    try:
        asyncio.run(generate_tts(text, voice, output_path))
        return send_file(output_path, mimetype="audio/mpeg")
    except Exception as e:
        return str(e), 500
