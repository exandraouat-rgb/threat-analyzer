"""
Parseur basique pour les diagrammes C4 Model
Extrait les composants, relations et flux de données depuis des fichiers texte/markdown
"""
import re
from typing import Dict, List, Optional

def parse_c4_text(content: str) -> Dict:
    """
    Parse un texte contenant une description de diagramme C4
    Retourne une structure avec composants, relations, et flux
    """
    result = {
        "components": [],
        "relations": [],
        "data_flows": [],
        "trust_boundaries": []
    }
    
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Détecter les sections
        if line.lower().startswith('#') or line.lower().startswith('##'):
            current_section = line.lower()
        
        # Extraire les composants (ex: "User Browser", "Web Application", "Database")
        component_patterns = [
            r'(\w+(?:\s+\w+)*)\s*(?:\(|:|\s+is\s+)',  # Format: "Component (description)"
            r'component\s+(\w+(?:\s+\w+)*)',  # Format: "component ComponentName"
            r'system\s+(\w+(?:\s+\w+)*)',  # Format: "system SystemName"
        ]
        
        for pattern in component_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                component_name = match.group(1).strip()
                if component_name and component_name not in [c.get('name') for c in result['components']]:
                    result['components'].append({
                        'name': component_name,
                        'type': 'component',
                        'description': ''
                    })
        
        # Extraire les relations (ex: "User -> Web Application", "Web Application -> Database")
        relation_patterns = [
            r'(\w+(?:\s+\w+)*)\s*[-=]>\s*(\w+(?:\s+\w+)*)',  # Format: "A -> B"
            r'(\w+(?:\s+\w+)*)\s+communicates\s+with\s+(\w+(?:\s+\w+)*)',  # Format: "A communicates with B"
            r'(\w+(?:\s+\w+)*)\s+calls\s+(\w+(?:\s+\w+)*)',  # Format: "A calls B"
        ]
        
        for pattern in relation_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                source = match.group(1).strip()
                target = match.group(2).strip()
                if source and target:
                    result['relations'].append({
                        'source': source,
                        'target': target,
                        'type': 'communication'
                    })
        
        # Extraire les flux de données
        data_flow_patterns = [
            r'data\s+flow\s+from\s+(\w+(?:\s+\w+)*)\s+to\s+(\w+(?:\s+\w+)*)',
            r'(\w+(?:\s+\w+)*)\s+sends\s+data\s+to\s+(\w+(?:\s+\w+)*)',
        ]
        
        for pattern in data_flow_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                source = match.group(1).strip()
                target = match.group(2).strip()
                if source and target:
                    result['data_flows'].append({
                        'source': source,
                        'target': target,
                        'data_type': 'unknown'
                    })
        
        # Extraire les zones de confiance
        if 'trust boundary' in line.lower() or 'security boundary' in line.lower():
            boundary_match = re.search(r'boundary[:\s]+(\w+(?:\s+\w+)*)', line, re.IGNORECASE)
            if boundary_match:
                result['trust_boundaries'].append({
                    'name': boundary_match.group(1),
                    'components': []
                })
    
    return result

def extract_architecture_from_c4(c4_data: Dict) -> str:
    """
    Convertit les données C4 parsées en description d'architecture textuelle
    pour l'analyse de menaces
    """
    description_parts = []
    
    if c4_data.get('components'):
        description_parts.append("Composants identifiés:")
        for comp in c4_data['components']:
            description_parts.append(f"- {comp['name']} ({comp.get('type', 'component')})")
    
    if c4_data.get('relations'):
        description_parts.append("\nRelations entre composants:")
        for rel in c4_data['relations']:
            description_parts.append(f"- {rel['source']} -> {rel['target']}")
    
    if c4_data.get('data_flows'):
        description_parts.append("\nFlux de données:")
        for flow in c4_data['data_flows']:
            description_parts.append(f"- {flow['source']} envoie des données à {flow['target']}")
    
    if c4_data.get('trust_boundaries'):
        description_parts.append("\nZones de confiance:")
        for boundary in c4_data['trust_boundaries']:
            description_parts.append(f"- {boundary['name']}")
    
    return "\n".join(description_parts)

def parse_c4_file(file_path: str) -> Optional[Dict]:
    """
    Parse un fichier C4 (markdown, texte, etc.)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return parse_c4_text(content)
    except Exception as e:
        print(f"Erreur lors du parsing du fichier C4: {e}")
        return None
