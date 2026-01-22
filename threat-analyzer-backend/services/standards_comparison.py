"""
Service pour comparer les menaces avec les standards de sécurité
(OWASP, CIS Controls, NIST)
"""
from typing import Dict, List

# Mapping OWASP Top 10 2021
OWASP_2021_MAPPING = {
    "A01:2021": "Broken Access Control",
    "A02:2021": "Cryptographic Failures",
    "A03:2021": "Injection",
    "A04:2021": "Insecure Design",
    "A05:2021": "Security Misconfiguration",
    "A06:2021": "Vulnerable and Outdated Components",
    "A07:2021": "Identification and Authentication Failures",
    "A08:2021": "Software and Data Integrity Failures",
    "A09:2021": "Security Logging and Monitoring Failures",
    "A10:2021": "Server-Side Request Forgery (SSRF)"
}

# Mapping CIS Controls (simplifié)
CIS_CONTROLS_MAPPING = {
    "CIS-1": "Inventory and Control of Enterprise Assets",
    "CIS-2": "Inventory and Control of Software Assets",
    "CIS-3": "Data Protection",
    "CIS-4": "Secure Configuration of Enterprise Assets",
    "CIS-5": "Account Management",
    "CIS-6": "Access Control Management",
    "CIS-7": "Continuous Vulnerability Management",
    "CIS-8": "Audit Log Management",
    "CIS-9": "Email and Web Browser Protections",
    "CIS-10": "Malware Defenses"
}

# Mapping NIST CSF (simplifié)
NIST_CSF_MAPPING = {
    "ID.AM": "Asset Management",
    "ID.BE": "Business Environment",
    "PR.AC": "Identity Management and Access Control",
    "PR.DS": "Data Security",
    "PR.IP": "Information Protection Processes",
    "DE.CM": "Security Continuous Monitoring",
    "DE.DP": "Detection Processes",
    "RS.RP": "Response Planning",
    "RC.RP": "Recovery Planning"
}

def map_to_owasp(owasp_category: str) -> Dict:
    """
    Mappe une catégorie OWASP à sa description
    """
    if not owasp_category or owasp_category == "N/A":
        return None
    
    category = owasp_category.split(':')[0] if ':' in owasp_category else owasp_category
    
    if category in OWASP_2021_MAPPING:
        return {
            "id": category,
            "name": OWASP_2021_MAPPING[category],
            "url": f"https://owasp.org/Top10/{category}/"
        }
    
    return None

def map_to_cis_controls(threat_name: str, cwe_id: str) -> List[Dict]:
    """
    Mappe une menace à des CIS Controls pertinents
    """
    mappings = []
    
    threat_lower = threat_name.lower()
    cwe_lower = cwe_id.lower() if cwe_id else ""
    
    # Mapping basique basé sur le type de menace
    if "authentication" in threat_lower or "CWE-287" in cwe_lower or "CWE-306" in cwe_lower:
        mappings.append({
            "id": "CIS-5",
            "name": CIS_CONTROLS_MAPPING["CIS-5"],
            "relevance": "high"
        })
        mappings.append({
            "id": "CIS-6",
            "name": CIS_CONTROLS_MAPPING["CIS-6"],
            "relevance": "high"
        })
    
    if "injection" in threat_lower or "CWE-89" in cwe_lower or "CWE-79" in cwe_lower:
        mappings.append({
            "id": "CIS-4",
            "name": CIS_CONTROLS_MAPPING["CIS-4"],
            "relevance": "high"
        })
        mappings.append({
            "id": "CIS-7",
            "name": CIS_CONTROLS_MAPPING["CIS-7"],
            "relevance": "medium"
        })
    
    if "data" in threat_lower or "storage" in threat_lower or "CWE-312" in cwe_lower:
        mappings.append({
            "id": "CIS-3",
            "name": CIS_CONTROLS_MAPPING["CIS-3"],
            "relevance": "high"
        })
    
    if "logging" in threat_lower or "monitoring" in threat_lower or "CWE-778" in cwe_lower:
        mappings.append({
            "id": "CIS-8",
            "name": CIS_CONTROLS_MAPPING["CIS-8"],
            "relevance": "high"
        })
    
    return mappings

def map_to_nist_csf(threat_name: str, cwe_id: str) -> List[Dict]:
    """
    Mappe une menace à des fonctions NIST CSF pertinentes
    """
    mappings = []
    
    threat_lower = threat_name.lower()
    cwe_lower = cwe_id.lower() if cwe_id else ""
    
    if "access" in threat_lower or "authentication" in threat_lower:
        mappings.append({
            "id": "PR.AC",
            "name": NIST_CSF_MAPPING["PR.AC"],
            "relevance": "high"
        })
    
    if "data" in threat_lower or "storage" in threat_lower:
        mappings.append({
            "id": "PR.DS",
            "name": NIST_CSF_MAPPING["PR.DS"],
            "relevance": "high"
        })
    
    if "monitoring" in threat_lower or "logging" in threat_lower:
        mappings.append({
            "id": "DE.CM",
            "name": NIST_CSF_MAPPING["DE.CM"],
            "relevance": "high"
        })
    
    return mappings

def enrich_threat_with_standards(threat: Dict) -> Dict:
    """
    Enrichit une menace avec des mappings vers les standards
    """
    enriched = threat.copy()
    
    # Mapping OWASP
    if threat.get("owasp_category"):
        owasp_info = map_to_owasp(threat.get("owasp_category"))
        if owasp_info:
            enriched["owasp_info"] = owasp_info
    
    # Mapping CIS Controls
    cis_mappings = map_to_cis_controls(
        threat.get("nom", ""),
        threat.get("cwe_id", "")
    )
    if cis_mappings:
        enriched["cis_controls"] = cis_mappings
    
    # Mapping NIST CSF
    nist_mappings = map_to_nist_csf(
        threat.get("nom", ""),
        threat.get("cwe_id", "")
    )
    if nist_mappings:
        enriched["nist_csf"] = nist_mappings
    
    return enriched
