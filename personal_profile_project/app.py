from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Import the voice agent analyzer
from modules.voice_agent.analyze import analyze_conversation

# Sample profile data - you can modify this according to your needs
profile_data = {
    "name": "Peng A",
    "title": "Founder",
    "bio": "I am a recent PhD graduate from McGill University. I am interested in using AI to help students.",
    "skills": [
        "Python", "Flask", "HTML/CSS", "JavaScript",
        "Git", "Database Management", "API Development"
    ],
    "projects": [
        {
            "name": "High-throughput Image segmentation&Analysis",
            "description": "This is associated with my PhD research. I developed a high-throughput image segmentation and analysis pipeline for Nucleolus in C.elegans.",
            "technologies": ["Python", "ImageJ"]
        },
        {
            "name": "Startup:Gradually",
            "description": "Description of your second project",
            "technologies": ["Python", "Flask", "HTML/CSS", "JavaScript", "React", "Node.js"]
        }
    ],
    "contact": {
        "email": "your.email@example.com",
        "linkedin": "https://www.linkedin.com/in/peng-a-3065018b/",
        "github": "https://github.com/ashapeng"
    }
}

@app.route('/')
def home():
    return render_template('index.html', profile=profile_data)

# Voice agent page
@app.route('/voice-agent')
def voice_agent():
    return render_template('voice_agent.html')

# API endpoint for voice agent analysis
@app.route('/api/voice-agent/analyze', methods=['POST'])
def voice_agent_analyze():
    data = request.get_json()
    text = data.get('text', '')
    audio_features = data.get('audio_features', None)
    result = analyze_conversation(text, audio_features)
    return jsonify(result)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=profile_data['projects'])

@app.route('/contact')
def contact():
    return render_template('contact.html', contact=profile_data['contact'])

if __name__ == '__main__':
    app.run(debug=True) 