import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.routes import initialize_routes


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

initialize_routes(api)


if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1',port=int(os.environ.get('PORT', 8080)))


