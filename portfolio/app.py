import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from forms import ContactForm
from config import Config
from models import db, ContactMessage
from datetime import datetime
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)

# Extensions
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# Routes
@app.route('/')
def home():
    profile = {
    'name': os.getenv('PORTFOLIO_NAME', 'Shiva'),
    'title': os.getenv('PORTFOLIO_TITLE', 'Software Engineer'),
    'bio': os.getenv('PORTFOLIO_BIO', 'Passionate about building scalable web apps and solving problems.'),
    'skills': ['Python', 'Flask', 'SQL', 'HTML', 'CSS', 'JavaScript', 'Node.js'],
    'hobbies': ['Reading', 'Gaming', 'Gym', 'Coding Challenges'],
    'languages': ['English', 'Telugu', 'Hindi'],
    'internships': [
        {'company': 'Bluestock', 'role': 'Backend Developer & Team Lead', 'duration': '3 months', 'description': 'Worked on Node.js backend and managed a small team.'},
        {'company': 'Other Company', 'role': 'Intern', 'duration': '2 months', 'description': 'Worked on Flask project and API integrations.'}
    ]
}

    projects = [
    {'title': 'Voice Assistant', 'desc': 'Jarvis-like personal assistant using Python.', 'github': '#', 'demo': '#'},
    {'title': 'Portfolio Website', 'desc': 'Dynamic Flask portfolio website.', 'github': '#', 'demo': '#'},
    {'title': 'Web Scraper', 'desc': 'Scrapes news articles from multiple websites.', 'github': '#', 'demo': '#'}
]

    return render_template('index.html', profile=profile, projects=projects)


@app.route('/projects')
def projects():
    projects = [
    {'title': 'Voice Assistant', 'desc': 'Jarvis-like personal assistant using Python.', 'github': '#', 'demo': '#'},
    {'title': 'Portfolio Website', 'desc': 'Dynamic Flask portfolio website.', 'github': '#', 'demo': '#'},
    {'title': 'Web Scraper', 'desc': 'Scrapes news articles from multiple websites.', 'github': '#', 'demo': '#'}
]

    return render_template('projects.html', projects=projects)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data,
            created_at=datetime.utcnow()
        )
        db.session.add(msg)
        db.session.commit()

        flash('Message sent successfully. Thank you!', 'success')
        return redirect(url_for('success'))
    return render_template('contact.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
