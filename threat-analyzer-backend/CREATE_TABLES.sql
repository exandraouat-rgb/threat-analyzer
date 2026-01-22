-- Script SQL pour créer les tables de la base de données menace_bd
-- Vous pouvez exécuter ce script dans votre interface MySQL (phpMyAdmin, MySQL Workbench, etc.)

-- Table pour les utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table principale pour les analyses
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table pour les menaces détectées
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Vérification : Afficher les tables créées
SHOW TABLES;
