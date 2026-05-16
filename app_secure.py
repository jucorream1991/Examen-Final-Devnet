# app_secure.py
# Script para gestión de usuarios, base de datos SQL y contraseñas en formato HASH

import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "usuarios_seguros.db"

def inicializar_base_datos():
    """Crea la base de datos y almacena los dos usuarios con contraseña en HASH"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Definir los dos usuarios requeridos por la pauta
    # 1. Obligatorio: Tu nombre y apellido
    # 2. A elección: Un usuario administrador alternativo
    usuarios_iniciales = [
        ("juan_correa", "Juan2026"),
        ("admin_redes", "net_devnet_2026")
    ]
    
    for user, password in usuarios_iniciales:
        # Aplicar Hash SHA-256 a la contraseña por seguridad
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute('INSERT INTO usuarios (username, password_hash) VALUES (?, ?)', (user, hash_password))
        except sqlite3.IntegrityError:
            # Si el usuario ya existe, no se vuelve a insertar
            pass
            
    conn.commit()
    conn.close()

def validar_usuario_comando(username, password):
    """Permite validar credenciales directamente por terminal"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    hash_buscar = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password_hash = ?', (username, hash_buscar))
    resultado = cursor.fetchone()
    
    conn.close()
    return resultado is not None

# --- Rutas del Servidor Web (Puerto 5800) ---
@app.route('/')
def home():
    return "<h1>Servidor Seguro Levantado - Puerto 5800 exitoso</h1>"

@app.route('/login', methods=['POST'])
def login_api():
    """Endpoint para validar usuarios vía API o Postman"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"status": "Error", "message": "Datos incompletos"}), 400
        
    username = data['username']
    password = data['password']
    
    if validar_usuario_comando(username, password):
        return jsonify({"status": "Éxito", "message": f"Usuario {username} autenticado correctamente."}), 200
    else:
        return jsonify({"status": "Denegado", "message": "Credenciales inválidas o hash incorrecto."}), 401

if __name__ == '__main__':
    # Inicializar la base de datos local SQLite
    inicializar_base_datos()
    print("\n[INFO] Base de datos SQLite inicializada con éxito.")
    print("[INFO] Usuarios registrados con contraseñas en formato HASH SHA-256.")
    
    # Validación por comando interactivo (Requerimiento Ítem 3)
    print("\n=== VALIDACIÓN DE USUARIOS POR COMANDO ===")
    user_test = input("Ingrese nombre de usuario para validar: ").strip()
    pass_test = input("Ingrese contraseña: ").strip()
    
    if validar_usuario_comando(user_test, pass_test):
        print(f"✅ Validación exitosa en Base de Datos para el usuario: {user_test}")
    else:
        print("❌ Error de autenticación: Usuario o contraseña incorrectos.")
    
    print("\n[INFO] Levantando el sitio web en el puerto 5800...")
    # Iniciar sitio web en el puerto 5800 como lo solicita el examen
    app.run(host='0.0.0.0', port=5800, debug=False)