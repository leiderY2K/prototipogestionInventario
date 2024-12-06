from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo para TipoDeProducto
class TipoDeProducto(db.Model):
    __tablename__ = 'TipoDeProducto'
    
    idTipoDeProducto = db.Column(db.Integer, primary_key=True)
    nombreTipoDeProducto = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "idTipoDeProducto": self.idTipoDeProducto,
            "nombreTipoDeProducto": self.nombreTipoDeProducto
        }

# Modelo para Producto
class Producto(db.Model):
    __tablename__ = 'Producto'
    
    idProducto = db.Column(db.Integer, primary_key=True)
    TituloProducto = db.Column(db.String(255), nullable=False)
    linkVisualizacion = db.Column(db.String(500))
    codigoUnico = db.Column(db.String(50), unique=True, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    idTipoDeProducto = db.Column(db.Integer, db.ForeignKey('TipoDeProducto.idTipoDeProducto'), nullable=False)

    tipo_de_producto = db.relationship('TipoDeProducto', backref=db.backref('productos', lazy=True))

    def to_dict(self):
        return {
            "idProducto": self.idProducto,
            "TituloProducto": self.TituloProducto,
            "linkVisualizacion": self.linkVisualizacion,
            "codigoUnico": self.codigoUnico,
            "ano": self.ano,
            "idTipoDeProducto": self.idTipoDeProducto,
            "categoriaNombre": self.tipo_de_producto.nombreTipoDeProducto  # Incluimos el nombre de la categoría
        }

# Modelo para Investigador
class Investigador(db.Model):
    __tablename__ = 'Investigador'
    
    idInvestigador = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "idInvestigador": self.idInvestigador,
            "nombres": self.nombres,
            "apellidos": self.apellidos
        }

# Modelo para InvestigadorProducto (tabla intermedia)
class InvestigadorProducto(db.Model):
    __tablename__ = 'InvestigadorProducto'
    
    idInvestigador = db.Column(db.Integer, db.ForeignKey('Investigador.idInvestigador'), primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('Producto.idProducto'), primary_key=True)

    investigador = db.relationship('Investigador', backref=db.backref('productos', lazy=True))
    producto = db.relationship('Producto', backref=db.backref('investigadores', lazy=True))

    def to_dict(self):
        return {
            "idInvestigador": self.idInvestigador,
            "idProducto": self.idProducto
        }
