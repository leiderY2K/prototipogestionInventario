from flask import Flask, jsonify
#from flask_migrate import Migrate
from models import db, Producto, TipoDeProducto, Investigador, InvestigadorProducto
from flask_cors import CORS 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost:3306/bdvirtus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

#migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"mensaje": "¡Bienvenido a la API del Repositorio Grupo Virtus UD!"})

@app.route('/productos', methods=['GET'])
def consultar_productos():
    try:
        productos = Producto.query.all()
        
        # Convertir los productos a diccionarios
        productos_dict = [producto.to_dict() for producto in productos]

        return jsonify(productos_dict), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)