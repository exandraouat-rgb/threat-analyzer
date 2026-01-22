"""
Service pour enrichir les données avec des informations MITRE ATT&CK
"""
import requests
from typing import Optional, Dict

def get_mitre_technique_info(technique_id: str) -> Optional[Dict]:
    """
    Récupère des informations sur une technique MITRE ATT&CK
    Note: Utilise l'API publique MITRE ATT&CK si disponible
    Sinon retourne des informations basiques basées sur l'ID
    """
    if not technique_id or technique_id == "N/A":
        return None
    
    # Nettoyer l'ID (enlever les espaces, etc.)
    technique_id = technique_id.strip().upper()
    
    # Informations basiques basées sur les IDs communs
    mitre_info = {
        "id": technique_id,
        "name": "",
        "description": "",
        "url": f"https://attack.mitre.org/techniques/{technique_id.replace('T', '')}"
    }
    
    # Mapping étendu de techniques MITRE ATT&CK communes
    technique_names = {
        "T1190": "Exploit Public-Facing Application",
        "T1078": "Valid Accounts",
        "T1565": "Data Manipulation",
        "T1557": "Adversary-in-the-Middle",
        "T1005": "Data from Local System",
        "T1530": "Data from Cloud Storage",
        "T1040": "Network Sniffing",
        "T1105": "Ingress Tool Transfer",
        "T1499": "Endpoint Denial of Service",
        "T1203": "Exploitation for Client Execution",
        "T1471": "Data Encrypted for Impact",
        "T1542": "Pre-OS Boot",
        "T1486": "Data Encrypted for Impact",
        "T1059": "Command and Scripting Interpreter",
        "T1055": "Process Injection",
        "T1021": "Remote Services",
        "T1071": "Application Layer Protocol",
        "T1566": "Phishing",
        "T1189": "Drive-by Compromise",
        "T1134": "Access Token Manipulation",
        "T1083": "File and Directory Discovery",
        "T1110": "Brute Force",
        "T1070": "Indicator Removal on Host",
        "T1036": "Masquerading",
        "T1053": "Scheduled Task/Job",
        "T1547": "Boot or Logon Autostart Execution"
    }
    
    # Descriptions détaillées pour certaines techniques
    technique_descriptions = {
        "T1190": "Les attaquants exploitent les vulnérabilités dans les applications accessibles publiquement pour obtenir un accès initial au système.",
        "T1078": "Les attaquants utilisent des comptes valides pour accéder aux systèmes, contournant ainsi les contrôles d'accès.",
        "T1557": "Les attaquants interceptent les communications entre deux parties pour voler des informations ou modifier les données.",
        "T1005": "Les attaquants collectent des données depuis le système local de la victime.",
        "T1530": "Les attaquants accèdent aux données stockées dans des services cloud."
    }
    
    if technique_id in technique_names:
        mitre_info["name"] = technique_names[technique_id]
        mitre_info["description"] = technique_descriptions.get(technique_id, f"Technique MITRE ATT&CK {technique_id}")
        mitre_info["tactic"] = get_tactic_for_technique(technique_id)
    
    # Essayer de récupérer depuis l'API MITRE (si disponible)
    try:
        # L'API MITRE ATT&CK Enterprise nécessite souvent une clé API
        # Pour l'instant, on retourne les infos basiques
        pass
    except Exception as e:
        print(f"Erreur lors de la récupération MITRE: {e}")
    
    return mitre_info

def get_tactic_for_technique(technique_id: str) -> str:
    """
    Retourne la tactique MITRE ATT&CK associée à une technique
    """
    # Mapping simplifié des tactiques
    tactic_mapping = {
        "T1190": "Initial Access",
        "T1078": "Defense Evasion, Persistence, Privilege Escalation",
        "T1565": "Impact",
        "T1557": "Collection",
        "T1005": "Collection",
        "T1530": "Collection",
        "T1040": "Collection",
        "T1105": "Command and Control",
        "T1499": "Impact",
        "T1203": "Execution",
        "T1471": "Impact",
        "T1542": "Persistence",
        "T1486": "Impact"
    }
    return tactic_mapping.get(technique_id, "Unknown")

def get_cwe_info(cwe_id: str) -> Optional[Dict]:
    """
    Récupère des informations sur un CWE
    """
    if not cwe_id or cwe_id == "N/A":
        return None
    
    cwe_id = cwe_id.strip().upper()
    
    return {
        "id": cwe_id,
        "name": "",
        "url": f"https://cwe.mitre.org/data/definitions/{cwe_id.replace('CWE-', '')}.html"
    }

def enrich_threat_with_metadata(threat: Dict) -> Dict:
    """
    Enrichit une menace avec des métadonnées supplémentaires
    """
    enriched = threat.copy()
    
    # Enrichir avec MITRE
    if threat.get("mitre_attack_id"):
        mitre_info = get_mitre_technique_info(threat.get("mitre_attack_id"))
        if mitre_info:
            enriched["mitre_info"] = mitre_info
    
    # Enrichir avec CWE
    if threat.get("cwe_id"):
        cwe_info = get_cwe_info(threat.get("cwe_id"))
        if cwe_info:
            enriched["cwe_info"] = cwe_info
    
    return enriched
