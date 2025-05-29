from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Sample profile data - you can modify this according to your needs
profile_data = {
    "name": "Your Name",
    "title": "Your Professional Title",
    "bio": "A brief description about yourself and your professional journey.",
    "skills": [
        "Python", "Flask", "HTML/CSS", "JavaScript",
        "Git", "Database Management", "API Development"
    ],
    "projects": [
        {
            "name": "Project 1",
            "description": "Description of your first project",
            "technologies": ["Python", "Flask", "SQLAlchemy"]
        },
        {
            "name": "Project 2",
            "description": "Description of your second project",
            "technologies": ["JavaScript", "React", "Node.js"]
        }
    ],
    "contact": {
        "email": "your.email@example.com",
        "linkedin": "https://linkedin.com/in/yourprofile",
        "github": "https://github.com/yourusername"
    }
}

@app.route('/')
def home():
    return render_template('index.html', profile=profile_data)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=profile_data['projects'])

@app.route('/contact')
def contact():
    return render_template('contact.html', contact=profile_data['contact'])

if __name__ == '__main__':
    app.run(debug=True) 