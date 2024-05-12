from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from waitress import serve
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a random secret key

# Configuring Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user store
users = {
    'admin': generate_password_hash('password123')
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    def __repr__(self):
        return "%s" % self.id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        url = request.form['url']
        open_url_in_chrome(url)
        open_url_in_edge(url)
        return render_template('index.html', message="URL opened in both browsers successfully!")
    return render_template('index.html', message="Enter a URL to open in Chrome and Edge.")

# Add your browser control functions here
def open_url_in_chrome(url):
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # Uncomment to run headless
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

def open_url_in_edge(url):
    service = EdgeService(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    # Uncomment to run headless
    # options.add_argument('--headless')
    driver = webdriver.Edge(service=service, options=options)
    driver.get(url)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
