from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from waitress import serve
import subprocess

app = Flask(__name__)
app.secret_key = 'change me and use something safe for Pete's'

# Configuring Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user store
users = {
    'change': generate_password_hash('me')
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


def open_url_in_edge(url):
    try:
        # Command to open Microsoft Edge with the specified URL
        command = f"start msedge {url}"
        # Execute the command using subprocess
        subprocess.run(command, shell=True, check=True)
        print("URL opened successfully in Microsoft Edge.")
    except subprocess.CalledProcessError as e:
        # Handle cases where the subprocess call fails
        print(f"Failed to open URL: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

def open_url_in_chrome(url):
    try:
        # Command to open Microsoft Edge with the specified URL
        command = f"start chrome {url}"
        # Execute the command using subprocess
        subprocess.run(command, shell=True, check=True)
        print("URL opened successfully in Google Chrome.")
    except subprocess.CalledProcessError as e:
        # Handle cases where the subprocess call fails
        print(f"Failed to open URL: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
