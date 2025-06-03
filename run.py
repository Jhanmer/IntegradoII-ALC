# run.py
from app import create_app # Importa la función create_app desde tu paquete 'app'

app = create_app() # Llama a la función para crear y configurar tu aplicación Flask

if __name__ == '__main__':
    app.run(debug=True)