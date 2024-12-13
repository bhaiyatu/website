from flask import Flask, render_template, send_file, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
import json
from flask_frozen import Freezer
import sys

# Load environment variables
load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap5(app)
freezer = Freezer(app)


# Load project data
def load_projects():
    with open('projects/projects.json') as f:
        return json.load(f)

# Add these configuration lines
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects/')
def projects():
    projects = load_projects()
    return render_template('projects.html', projects=projects)

@app.route('/skills/')
def skills():
    return render_template('skills.html')

@app.route('/cv/')
def cv():
    return render_template('cv.html')

@app.route('/download-cv/')
def download_cv():
    cv_path = os.path.join('static', 'cv', 'UmarCV-UK.pdf')
    return send_file(cv_path, as_attachment=True, mimetype='application/pdf')

@app.route('/certifications/')
def certifications():
    return render_template('certifications.html')

# Updated URL generators for Frozen-Flask
@freezer.register_generator
def url_generator():
    # Return a list of URLs for Frozen-Flask to generate
    urls = [
        ('home', {}),
        ('projects', {}),
        ('skills', {}),
        ('cv', {}),
        ('certifications', {}),
        ('download_cv', {})
    ]
    for endpoint, kwargs in urls:
        yield endpoint, kwargs

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(debug=True) 