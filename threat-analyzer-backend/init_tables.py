"""
Script pour initialiser les tables dans la base de données MySQL
Exécutez ce script pour créer toutes les tables nécessaires
"""
import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

# Configuration MySQL
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'menace_bd'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def create_tables():
    """
    Crée toutes les tables nécessaires dans la base de données
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Connexion à MySQL réussie!")
        print(f"Base de données: {DB_CONFIG['database']}")
        print("-" * 50)
        
        # Table users
        print("Création de la table 'users'...")
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
        print("✓ Table 'users' créée")
        
        # Table analyses
        print("Création de la table 'analyses'...")
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
        print("✓ Table 'analyses' créée")
        
        # Table menaces
        print("Création de la table 'menaces'...")
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
        print("✓ Table 'menaces' créée")
        
        conn.commit()
        
        # Vérifier les tables créées
        print("-" * 50)
        print("Vérification des tables créées...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\nTables trouvées dans '{DB_CONFIG['database']}':")
        for table in tables:
            table_name = list(table.values())[0]
            print(f"  - {table_name}")
        
        conn.close()
        print("\n✓ Toutes les tables ont été créées avec succès!")
        
    except pymysql.Error as e:
        print(f"Erreur MySQL: {e}")
        return False
    except Exception as e:
        print(f"Erreur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Initialisation des tables MySQL")
    print("=" * 50)
    print()
    
    success = create_tables()
    
    if success:
        print("\n✓ Initialisation terminée avec succès!")
    else:
        print("\n✗ Erreur lors de l'initialisation")
        exit(1)
