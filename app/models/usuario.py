# app/models/usuario.py
from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, CodUsu, nombre, rol, login, password, estado):
        self.CodUsu = CodUsu
        self.nombre = nombre
        self.rol = rol
        self.login = login
        self.password = password
        self.estado = estado

    def __repr__(self):
        return f"Usuario('{self.nombre}', '{self.login}', '{self.rol}')"

    def get_id(self):
        return str(self.CodUsu)

    def check_password(self, password):
        return self.password == password