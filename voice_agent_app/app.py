from flask import Flask, render_template, request, jsonify
from modules.analyze import analyze_conversation

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('voice_agent.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    audio_features = data.get('audio_features', None)
    result = analyze_conversation(text, audio_features)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)