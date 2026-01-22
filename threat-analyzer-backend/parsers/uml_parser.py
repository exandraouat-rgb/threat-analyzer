"""
Parseur basique pour les diagrammes UML
Extrait les classes, relations et interactions depuis des fichiers texte/XMI
"""
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

def parse_uml_text(content: str) -> Dict:
    """
    Parse un texte contenant une description de diagramme UML
    Retourne une structure avec classes, relations, et interactions
    """
    result = {
        "classes": [],
        "relations": [],
        "interactions": [],
        "actors": [],
        "use_cases": []
    }
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Extraire les classes (ex: "class User", "class Database")
        class_patterns = [
            r'class\s+(\w+)',
            r'(\w+)\s*:\s*class',
            r'(\w+)\s*\{.*class',
        ]
        
        for pattern in class_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                class_name = match.group(1).strip()
                if class_name and class_name not in [c.get('name') for c in result['classes']]:
                    result['classes'].append({
                        'name': class_name,
                        'type': 'class',
                        'attributes': [],
                        'methods': []
                    })
        
        # Extraire les relations (ex: "User -> Database", "User extends Admin")
        relation_patterns = [
            r'(\w+)\s*[-=]>\s*(\w+)',  # Format: "A -> B"
            r'(\w+)\s+extends\s+(\w+)',  # Format: "A extends B"
            r'(\w+)\s+implements\s+(\w+)',  # Format: "A implements B"
            r'(\w+)\s+uses\s+(\w+)',  # Format: "A uses B"
            r'(\w+)\s+depends\s+on\s+(\w+)',  # Format: "A depends on B"
        ]
        
        for pattern in relation_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                source = match.group(1).strip()
                target = match.group(2).strip()
                rel_type = 'association'
                
                if 'extends' in line.lower():
                    rel_type = 'inheritance'
                elif 'implements' in line.lower():
                    rel_type = 'implementation'
                elif 'uses' in line.lower() or 'depends' in line.lower():
                    rel_type = 'dependency'
                
                if source and target:
                    result['relations'].append({
                        'source': source,
                        'target': target,
                        'type': rel_type
                    })
        
        # Extraire les acteurs (ex: "actor User", "User : actor")
        actor_patterns = [
            r'actor\s+(\w+)',
            r'(\w+)\s*:\s*actor',
        ]
        
        for pattern in actor_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                actor_name = match.group(1).strip()
                if actor_name and actor_name not in result['actors']:
                    result['actors'].append(actor_name)
        
        # Extraire les use cases
        use_case_patterns = [
            r'use\s+case\s+(\w+)',
            r'(\w+)\s*:\s*use\s+case',
        ]
        
        for pattern in use_case_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                use_case = match.group(1).strip()
                if use_case and use_case not in result['use_cases']:
                    result['use_cases'].append(use_case)
    
    return result

def parse_xmi_content(content: str) -> Optional[Dict]:
    """
    Parse le contenu XMI (XML Metadata Interchange) pour UML depuis une chaîne
    Supporte plusieurs formats : UML 2.x standard, Eclipse UML2, formats génériques
    """
    try:
        root = ET.fromstring(content)
        
        result = {
            "classes": [],
            "relations": [],
            "interactions": [],
            "actors": [],
            "use_cases": []
        }
        
        # Extraire les namespaces depuis la racine
        namespaces = {}
        for key, value in root.attrib.items():
            if key.startswith('xmlns'):
                if key == 'xmlns':
                    namespaces['default'] = value
                elif key.startswith('xmlns:'):
                    prefix = key.split(':', 1)[1]
                    namespaces[prefix] = value
        
        # Fonction helper pour trouver des éléments avec différents namespaces
        def find_with_namespaces(tag_name):
            elements = []
            # Format standard UML 2.x
            uml_ns = namespaces.get("uml", "http://www.omg.org/spec/UML/20131001")
            elements.extend(root.findall(f'.//{{{uml_ns}}}{tag_name}'))
            # Format Eclipse UML2
            uml2_ns = "http://www.eclipse.org/uml2/5.0.0/UML"
            elements.extend(root.findall(f'.//{{{uml2_ns}}}{tag_name}'))
            # Format générique (sans namespace)
            elements.extend(root.findall(f'.//{tag_name}'))
            # Format avec namespace par défaut
            if 'default' in namespaces:
                default_ns = namespaces["default"]
                elements.extend(root.findall(f'.//{{{default_ns}}}{tag_name}'))
            # Éliminer les doublons
            seen = set()
            unique_elements = []
            for elem in elements:
                elem_id = id(elem)
                if elem_id not in seen:
                    seen.add(elem_id)
                    unique_elements.append(elem)
            return unique_elements
        
        # Extraire les classes
        classes_found = set()
        for cls in find_with_namespaces('Class'):
            class_name = cls.get('name', '')
            if class_name and class_name not in classes_found:
                classes_found.add(class_name)
                result['classes'].append({
                    'name': class_name,
                    'type': 'class',
                    'attributes': [],
                    'methods': []
                })
        
        # Extraire les acteurs
        actors_found = set()
        for actor in find_with_namespaces('Actor'):
            actor_name = actor.get('name', '')
            if actor_name and actor_name not in actors_found:
                actors_found.add(actor_name)
                result['actors'].append(actor_name)
        
        # Extraire les use cases
        use_cases_found = set()
        for uc in find_with_namespaces('UseCase'):
            uc_name = uc.get('name', '')
            if uc_name and uc_name not in use_cases_found:
                use_cases_found.add(uc_name)
                result['use_cases'].append(uc_name)
        
        # Extraire les relations (associations)
        relations_found = set()
        for association in find_with_namespaces('Association'):
            # Chercher les propriétés (ends) de l'association
            properties = []
            for prop in association.findall('.//Property'):
                properties.append(prop)
            for prop in association.findall('.//{http://www.omg.org/spec/UML/20131001}Property'):
                properties.append(prop)
            for prop in association.findall('.//{http://www.eclipse.org/uml2/5.0.0/UML}Property'):
                properties.append(prop)
            
            if len(properties) >= 2:
                source_name = properties[0].get('name', '')
                target_name = properties[1].get('name', '')
                
                # Si pas de nom, chercher via xmi:idref ou type
                if not source_name:
                    type_ref = properties[0].get('type', '')
                    if type_ref:
                        # Chercher l'élément référencé
                        ref_elem = root.find(f'.//*[@xmi:id="{type_ref}"]')
                        if ref_elem is not None:
                            source_name = ref_elem.get('name', '')
                
                if not target_name:
                    type_ref = properties[1].get('type', '')
                    if type_ref:
                        ref_elem = root.find(f'.//*[@xmi:id="{type_ref}"]')
                        if ref_elem is not None:
                            target_name = ref_elem.get('name', '')
                
                if source_name and target_name:
                    rel_key = f"{source_name}->{target_name}"
                    if rel_key not in relations_found:
                        relations_found.add(rel_key)
                        result['relations'].append({
                            'source': source_name,
                            'target': target_name,
                            'type': 'association'
                        })
        
        # Extraire les relations d'héritage (Generalization)
        for gen in find_with_namespaces('Generalization'):
            # Chercher les références source et target
            source_ref = gen.get('source', '') or gen.get('{http://www.omg.org/spec/UML/20131001}source', '')
            target_ref = gen.get('target', '') or gen.get('{http://www.omg.org/spec/UML/20131001}target', '')
            
            if source_ref:
                source_elem = root.find(f'.//*[@xmi:id="{source_ref}"]')
                if source_elem is not None:
                    source_name = source_elem.get('name', '')
            else:
                source_elem = gen.find('.//source')
                if source_elem is not None:
                    source_name = source_elem.get('name', '')
                else:
                    source_name = ''
            
            if target_ref:
                target_elem = root.find(f'.//*[@xmi:id="{target_ref}"]')
                if target_elem is not None:
                    target_name = target_elem.get('name', '')
            else:
                target_elem = gen.find('.//target')
                if target_elem is not None:
                    target_name = target_elem.get('name', '')
                else:
                    target_name = ''
            
            if source_name and target_name:
                rel_key = f"{source_name}->{target_name}"
                if rel_key not in relations_found:
                    relations_found.add(rel_key)
                    result['relations'].append({
                        'source': source_name,
                        'target': target_name,
                        'type': 'inheritance'
                    })
        
        return result if (result['classes'] or result['actors'] or result['use_cases'] or result['relations']) else None
        
    except ET.ParseError as e:
        print(f"Erreur de parsing XML: {e}")
        return None
    except Exception as e:
        print(f"Erreur lors du parsing XMI: {e}")
        import traceback
        traceback.print_exc()
        return None

def parse_xmi_file(file_path: str) -> Optional[Dict]:
    """
    Parse un fichier XMI (XML Metadata Interchange) pour UML
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return parse_xmi_content(content)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier XMI: {e}")
        return None

def extract_architecture_from_uml(uml_data: Dict) -> str:
    """
    Convertit les données UML parsées en description d'architecture textuelle
    """
    description_parts = []
    
    if uml_data.get('classes'):
        description_parts.append("Classes identifiées:")
        for cls in uml_data['classes']:
            description_parts.append(f"- {cls['name']} (classe)")
    
    if uml_data.get('actors'):
        description_parts.append("\nActeurs identifiés:")
        for actor in uml_data['actors']:
            description_parts.append(f"- {actor}")
    
    if uml_data.get('use_cases'):
        description_parts.append("\nUse cases identifiés:")
        for uc in uml_data['use_cases']:
            description_parts.append(f"- {uc}")
    
    if uml_data.get('relations'):
        description_parts.append("\nRelations entre éléments:")
        for rel in uml_data['relations']:
            description_parts.append(f"- {rel['source']} {rel['type']} {rel['target']}")
    
    return "\n".join(description_parts)

def parse_uml_file(file_path: str) -> Optional[Dict]:
    """
    Parse un fichier UML (texte, XMI, etc.)
    """
    try:
        if file_path.endswith('.xmi') or file_path.endswith('.xml'):
            return parse_xmi_file(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return parse_uml_text(content)
    except Exception as e:
        print(f"Erreur lors du parsing UML: {e}")
        return None

def parse_uml_from_content(content: str, is_xml: bool = False) -> Optional[Dict]:
    """
    Parse le contenu UML depuis une chaîne (texte ou XMI)
    """
    try:
        if is_xml:
            return parse_xmi_content(content)
        else:
            return parse_uml_text(content)
    except Exception as e:
        print(f"Erreur lors du parsing UML: {e}")
        return None
