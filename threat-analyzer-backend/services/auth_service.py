"""
Service d'authentification pour gérer les utilisateurs
Utilise MySQL pour stocker les utilisateurs avec mots de passe hashés
"""
import pymysql
import bcrypt
from typing import Optional, Dict
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration MySQL (même que storage_service)
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'menace_bd'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_connection():
    """
    Crée une connexion à la base de données MySQL
    """
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Erreur de connexion MySQL: {e}")
        raise

def init_users_table():
    """
    Initialise la table users si elle n'existe pas
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la création de la table users: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def hash_password(password: str) -> str:
    """
    Hash un mot de passe avec bcrypt
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """
    Vérifie un mot de passe contre son hash
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def register_user(email: str, password: str, name: str) -> Optional[Dict]:
    """
    Enregistre un nouvel utilisateur
    Retourne les données de l'utilisateur créé ou None si l'email existe déjà
    """
    init_users_table()
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Vérifier si l'email existe déjà
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return None
        
        # Hasher le mot de passe
        password_hash = hash_password(password)
        
        # Insérer le nouvel utilisateur
        cursor.execute("""
            INSERT INTO users (email, password_hash, name)
            VALUES (%s, %s, %s)
        """, (email, password_hash, name))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        return {
            'id': str(user_id),
            'email': email,
            'name': name
        }
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'inscription: {e}")
        return None
    finally:
        conn.close()

def login_user(email: str, password: str) -> Optional[Dict]:
    """
    Authentifie un utilisateur
    Retourne les données de l'utilisateur si les identifiants sont corrects, None sinon
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, email, password_hash, name 
            FROM users 
            WHERE email = %s
        """, (email,))
        
        user = cursor.fetchone()
        
        if not user:
            return None
        
        # Vérifier le mot de passe
        if verify_password(password, user['password_hash']):
            return {
                'id': str(user['id']),
                'email': user['email'],
                'name': user['name']
            }
        else:
            return None
    except Exception as e:
        print(f"Erreur lors de la connexion: {e}")
        return None
    finally:
        conn.close()

def get_user_by_id(user_id: str) -> Optional[Dict]:
    """
    Récupère un utilisateur par son ID
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, email, name 
            FROM users 
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if user:
            return {
                'id': str(user['id']),
                'email': user['email'],
                'name': user['name']
            }
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur: {e}")
        return None
    finally:
        conn.close()
