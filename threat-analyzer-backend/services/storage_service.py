"""
Service de stockage pour sauvegarder les analyses
Utilise MySQL pour un stockage persistant
"""
import pymysql
import json
from datetime import datetime
from typing import Optional, Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration MySQL depuis les variables d'environnement
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

def init_database():
    """
    Initialise la base de données MySQL et crée les tables si elles n'existent pas
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Créer la table users si elle n'existe pas
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                project_name VARCHAR(255) NOT NULL,
                user_id VARCHAR(255),
                app_type VARCHAR(100),
                architecture_description TEXT,
                score_risque INT,
                niveau_global VARCHAR(50),
                dashboard_data JSON,
                analysis_data JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menaces (
                id INT AUTO_INCREMENT PRIMARY KEY,
                analysis_id INT,
                nom VARCHAR(255),
                gravite VARCHAR(50),
                description TEXT,
                cwe_id VARCHAR(50),
                cvss_score VARCHAR(10),
                mitre_attack_id VARCHAR(50),
                owasp_category VARCHAR(50),
                score_confiance DECIMAL(5,2),
                recommandations JSON,
                FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def save_analysis(project_name: str, user_id: Optional[str], app_type: str,
                  architecture_description: str, dashboard: Dict, analysis: Dict) -> int:
    """
    Sauvegarde une analyse dans la base de données MySQL
    Retourne l'ID de l'analyse créée
    """
    init_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        score_risque = dashboard.get('resume', {}).get('score', 0)
        niveau_global = analysis.get('niveau_global', 'Faible')
        
        cursor.execute("""
            INSERT INTO analyses (project_name, user_id, app_type, architecture_description,
                                 score_risque, niveau_global, dashboard_data, analysis_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            project_name,
            user_id,
            app_type,
            architecture_description,
            score_risque,
            niveau_global,
            json.dumps(dashboard),
            json.dumps(analysis)
        ))
        
        analysis_id = cursor.lastrowid
        
        # Sauvegarder les menaces
        for menace in analysis.get('menaces', []):
            cursor.execute("""
                INSERT INTO menaces (analysis_id, nom, gravite, description, cwe_id,
                                   cvss_score, mitre_attack_id, owasp_category,
                                   score_confiance, recommandations)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                analysis_id,
                menace.get('nom'),
                menace.get('gravite'),
                menace.get('description'),
                menace.get('cwe_id', 'N/A'),
                menace.get('cvss_score', 'N/A'),
                menace.get('mitre_attack_id', 'N/A'),
                menace.get('owasp_category', 'N/A'),
                menace.get('score_confiance', 0.8),
                json.dumps(menace.get('recommandations', []))
            ))
        
        conn.commit()
        return analysis_id
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la sauvegarde: {e}")
        raise
    finally:
        conn.close()

def get_analysis_by_id(analysis_id: int) -> Optional[Dict]:
    """
    Récupère une analyse par son ID
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM analyses WHERE id = %s", (analysis_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        # Récupérer les menaces
        cursor.execute("SELECT * FROM menaces WHERE analysis_id = %s", (analysis_id,))
        menaces_rows = cursor.fetchall()
        
        menaces = []
        for menace_row in menaces_rows:
            menaces.append({
                'nom': menace_row['nom'],
                'gravite': menace_row['gravite'],
                'description': menace_row['description'],
                'cwe_id': menace_row['cwe_id'],
                'cvss_score': menace_row['cvss_score'],
                'mitre_attack_id': menace_row['mitre_attack_id'],
                'owasp_category': menace_row['owasp_category'],
                'score_confiance': float(menace_row['score_confiance']) if menace_row['score_confiance'] else 0.8,
                'recommandations': json.loads(menace_row['recommandations']) if menace_row['recommandations'] else []
            })
        
        dashboard_data = json.loads(row['dashboard_data']) if isinstance(row['dashboard_data'], str) else row['dashboard_data']
        
        return {
            'id': row['id'],
            'project_name': row['project_name'],
            'user_id': row['user_id'],
            'app_type': row['app_type'],
            'architecture_description': row['architecture_description'],
            'score_risque': row['score_risque'],
            'niveau_global': row['niveau_global'],
            'dashboard': dashboard_data,
            'analysis': {
                'niveau_global': row['niveau_global'],
                'menaces': menaces
            },
            'created_at': row['created_at'].isoformat() if row['created_at'] else None,
            'updated_at': row['updated_at'].isoformat() if row['updated_at'] else None
        }
    except Exception as e:
        print(f"Erreur lors de la récupération de l'analyse: {e}")
        return None
    finally:
        conn.close()

def get_analyses_by_user(user_id: str) -> List[Dict]:
    """
    Récupère toutes les analyses d'un utilisateur
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM analyses WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        
        analyses = []
        for row in rows:
            analysis = get_analysis_by_id(row['id'])
            if analysis:
                analyses.append(analysis)
        
        return analyses
    except Exception as e:
        print(f"Erreur lors de la récupération des analyses: {e}")
        return []
    finally:
        conn.close()

def delete_analysis(analysis_id: int) -> bool:
    """
    Supprime une analyse (les menaces seront supprimées automatiquement grâce à ON DELETE CASCADE)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM analyses WHERE id = %s", (analysis_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        return deleted
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression: {e}")
        return False
    finally:
        conn.close()
