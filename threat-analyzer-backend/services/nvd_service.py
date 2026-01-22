"""
Service pour intégrer l'API NVD (National Vulnerability Database)
Récupère des informations sur les vulnérabilités CVE
"""
import requests
from typing import Optional, Dict, List
import time

NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def search_cve_by_keyword(keyword: str, limit: int = 5) -> List[Dict]:
    """
    Recherche des CVE par mot-clé
    """
    try:
        # L'API NVD nécessite un rate limiting
        time.sleep(0.6)  # Respecter le rate limit (50 requêtes par 30 secondes)
        
        url = f"{NVD_API_BASE}?keywordSearch={keyword}&resultsPerPage={limit}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            cves = []
            
            if 'vulnerabilities' in data:
                for vuln in data['vulnerabilities']:
                    cve_data = vuln.get('cve', {})
                    cve_id = cve_data.get('id', '')
                    
                    # Extraire la description
                    descriptions = cve_data.get('descriptions', [])
                    description = ''
                    for desc in descriptions:
                        if desc.get('lang') == 'en':
                            description = desc.get('value', '')
                            break
                    
                    # Extraire le score CVSS
                    metrics = cve_data.get('metrics', {})
                    cvss_score = None
                    severity = None
                    
                    if 'cvssMetricV31' in metrics:
                        cvss_data = metrics['cvssMetricV31'][0]
                        cvss_score = cvss_data.get('cvssData', {}).get('baseScore')
                        severity = cvss_data.get('cvssData', {}).get('baseSeverity')
                    elif 'cvssMetricV30' in metrics:
                        cvss_data = metrics['cvssMetricV30'][0]
                        cvss_score = cvss_data.get('cvssData', {}).get('baseScore')
                        severity = cvss_data.get('cvssData', {}).get('baseSeverity')
                    elif 'cvssMetricV2' in metrics:
                        cvss_data = metrics['cvssMetricV2'][0]
                        cvss_score = cvss_data.get('cvssData', {}).get('baseScore')
                        severity = cvss_data.get('baseSeverity', '')
                    
                    cves.append({
                        'id': cve_id,
                        'description': description,
                        'cvss_score': cvss_score,
                        'severity': severity,
                        'url': f"https://nvd.nist.gov/vuln/detail/{cve_id}"
                    })
            
            return cves
        else:
            print(f"Erreur API NVD: {response.status_code}")
            return []
    except Exception as e:
        print(f"Erreur lors de la recherche CVE: {e}")
        return []

def get_cve_by_id(cve_id: str) -> Optional[Dict]:
    """
    Récupère les détails d'un CVE spécifique
    """
    try:
        time.sleep(0.6)  # Rate limiting
        
        url = f"{NVD_API_BASE}?cveId={cve_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'vulnerabilities' in data and len(data['vulnerabilities']) > 0:
                vuln = data['vulnerabilities'][0]
                cve_data = vuln.get('cve', {})
                
                descriptions = cve_data.get('descriptions', [])
                description = ''
                for desc in descriptions:
                    if desc.get('lang') == 'en':
                        description = desc.get('value', '')
                        break
                
                metrics = cve_data.get('metrics', {})
                cvss_score = None
                severity = None
                
                if 'cvssMetricV31' in metrics:
                    cvss_data = metrics['cvssMetricV31'][0]
                    cvss_score = cvss_data.get('cvssData', {}).get('baseScore')
                    severity = cvss_data.get('cvssData', {}).get('baseSeverity')
                
                return {
                    'id': cve_id,
                    'description': description,
                    'cvss_score': cvss_score,
                    'severity': severity,
                    'url': f"https://nvd.nist.gov/vuln/detail/{cve_id}"
                }
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération CVE: {e}")
        return None

def enrich_threat_with_cve(threat_name: str, cwe_id: str = None) -> List[Dict]:
    """
    Enrichit une menace avec des CVE associés
    """
    cves = []
    
    # Rechercher par nom de menace
    if threat_name:
        threat_cves = search_cve_by_keyword(threat_name, limit=3)
        cves.extend(threat_cves)
    
    # Rechercher par CWE si disponible
    if cwe_id and cwe_id != "N/A":
        cwe_number = cwe_id.replace('CWE-', '')
        cwe_cves = search_cve_by_keyword(f"CWE-{cwe_number}", limit=2)
        cves.extend(cwe_cves)
    
    # Dédupliquer
    seen_ids = set()
    unique_cves = []
    for cve in cves:
        if cve['id'] not in seen_ids:
            seen_ids.add(cve['id'])
            unique_cves.append(cve)
    
    return unique_cves[:5]  # Limiter à 5 CVE
