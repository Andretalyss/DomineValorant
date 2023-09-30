from flask import Flask
# Importação de rotas.
from routes.login import auth_route
from routes.agents_info import agents_info_routes

app = Flask(__name__)

app.register_blueprint(auth_route, url_prefix='/auth')
app.register_blueprint(agents_info_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)