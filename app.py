from flask import Flask
from penyakit import penyakit_bp
from jenis import jenis_bp
from weather import weather_bp
from history import history_bp
from login_routes import login_bp
from register import register_bp
from logout_routes import logout_bp

app = Flask(__name__)

@app.route('/')
def home():
    return "Server Flask Aktif"

# Register Blueprints
app.register_blueprint(penyakit_bp)
app.register_blueprint(jenis_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(history_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(logout_bp)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    