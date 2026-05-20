from flask import Flask
from flask_cors import CORS

from database.db import init_db
from routes.auth_routes import auth_bp
from routes.review_routes import review_bp
from routes.user_routes import user_bp

app = Flask(__name__)
CORS(app)

init_db(app)

app.register_blueprint(auth_bp)
app.register_blueprint(review_bp)
app.register_blueprint(user_bp)
from flask import jsonify

@app.route("/")
def home():
    return jsonify({
        "message": "AI Code Review System API Running"
    })
    import subprocess



if __name__ == "__main__":
    app.run(debug=True)