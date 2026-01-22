# Guide de Création des Tables MySQL

## Méthode 1 : Via phpMyAdmin (Recommandé)

### Étapes :

1. **Ouvrez phpMyAdmin** et sélectionnez la base de données `menace_bd`

2. **Cliquez sur l'onglet "SQL"** en haut de la page

3. **Copiez-collez ce script SQL** :

```sql
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
```

4. **Cliquez sur "Exécuter"** (ou appuyez sur Ctrl+Entrée)

5. **Vérifiez** que les 3 tables sont créées :
   - `users`
   - `analyses`
   - `menaces`

---

## Méthode 2 : Via Script Python

### Prérequis :
- Avoir installé `pymysql` : `pip install pymysql`
- Avoir configuré le fichier `.env` avec les identifiants MySQL

### Étapes :

1. **Ouvrez un terminal** dans le dossier `threat-analyzer-backend`

2. **Exécutez le script** :
   ```bash
   python init_tables.py
   ```

3. Le script va :
   - Se connecter à MySQL
   - Créer les 3 tables automatiquement
   - Afficher un message de confirmation

---

## Vérification

Après avoir créé les tables, vous devriez voir dans phpMyAdmin :

- ✅ Table `users` (4 colonnes)
- ✅ Table `analyses` (11 colonnes)
- ✅ Table `menaces` (11 colonnes)

---

## Dépannage

### Erreur "Table already exists"
- C'est normal si vous exécutez le script plusieurs fois
- Les tables existantes ne seront pas modifiées

### Erreur de connexion MySQL
- Vérifiez que MySQL est en cours d'exécution
- Vérifiez les identifiants dans le fichier `.env`
- Vérifiez que la base de données `menace_bd` existe

### Erreur "Access denied"
- Vérifiez les permissions de l'utilisateur MySQL
- Exécutez : `GRANT ALL PRIVILEGES ON menace_bd.* TO 'root'@'localhost';`
