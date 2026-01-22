# Configuration MySQL pour Threat Analyzer

## Prérequis

1. MySQL installé et en cours d'exécution
2. Base de données `menace_bd` créée

## Configuration

### 1. Créer la base de données

Si vous ne l'avez pas déjà fait, créez la base de données :

```sql
CREATE DATABASE menace_bd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configurer les variables d'environnement

Éditez le fichier `.env` dans le dossier `threat-analyzer-backend` et ajoutez :

```env
# Configuration MySQL
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=votre_mot_de_passe
MYSQL_DATABASE=menace_bd
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Cela installera `pymysql` nécessaire pour la connexion MySQL.

### 4. Initialiser les tables

Les tables seront créées automatiquement lors de la première utilisation. Vous pouvez aussi les créer manuellement en exécutant le backend une première fois.

## Structure des tables

### Table `analyses`
- `id` : Identifiant unique (AUTO_INCREMENT)
- `project_name` : Nom du projet
- `user_id` : ID de l'utilisateur
- `app_type` : Type d'application
- `architecture_description` : Description de l'architecture
- `score_risque` : Score de risque (0-100)
- `niveau_global` : Niveau global (Faible, Élevé, Critique)
- `dashboard_data` : Données du dashboard (JSON)
- `analysis_data` : Données de l'analyse (JSON)
- `created_at` : Date de création
- `updated_at` : Date de mise à jour

### Table `menaces`
- `id` : Identifiant unique (AUTO_INCREMENT)
- `analysis_id` : ID de l'analyse (FOREIGN KEY)
- `nom` : Nom de la menace
- `gravite` : Gravité (Critique, Élevée, Moyenne, Faible)
- `description` : Description de la menace
- `cwe_id` : Identifiant CWE
- `cvss_score` : Score CVSS
- `mitre_attack_id` : ID MITRE ATT&CK
- `owasp_category` : Catégorie OWASP
- `score_confiance` : Score de confiance IA (0-1)
- `recommandations` : Recommandations (JSON)

## Vérification

Pour vérifier que tout fonctionne, démarrez le backend :

```bash
python -m uvicorn main:app --reload --port 8000
```

Les tables seront créées automatiquement lors de la première analyse.

## Dépannage

### Erreur de connexion
- Vérifiez que MySQL est en cours d'exécution
- Vérifiez les identifiants dans le fichier `.env`
- Vérifiez que la base de données `menace_bd` existe

### Erreur de permissions
- Assurez-vous que l'utilisateur MySQL a les permissions nécessaires :
```sql
GRANT ALL PRIVILEGES ON menace_bd.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```
