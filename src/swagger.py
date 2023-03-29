from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/docs'  
API_URL = 'http://localhost:5000/swagger'


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  
        'app_name': "FLASK-API"
    },
)
