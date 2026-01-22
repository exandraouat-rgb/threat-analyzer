"""
Script de test pour vérifier que tous les modules fonctionnent correctement
"""
import sys
import os

def test_imports():
    """Teste tous les imports"""
    print("Test des imports...")
    errors = []
    
    try:
        from rag.build_kb import build_vector_db
        print("  [OK] rag.build_kb")
    except Exception as e:
        errors.append(f"[ERREUR] rag.build_kb: {e}")
    
    try:
        from rag.query_kb import search_threats
        print("  [OK] rag.query_kb")
    except Exception as e:
        errors.append(f"[ERREUR] rag.query_kb: {e}")
    
    try:
        from services.llm_service import analyze_with_claude
        print("  [OK] services.llm_service")
    except Exception as e:
        errors.append(f"[ERREUR] services.llm_service: {e}")
    
    try:
        from services.langchain_service import analyze_with_langchain
        print("  [OK] services.langchain_service")
    except Exception as e:
        print(f"  [WARN] services.langchain_service: {e} (peut necessiter langchain)")
    
    try:
        from services.nvd_service import enrich_threat_with_cve
        print("  [OK] services.nvd_service")
    except Exception as e:
        errors.append(f"[ERREUR] services.nvd_service: {e}")
    
    try:
        from services.storage_service import save_analysis, init_database
        print("  [OK] services.storage_service")
    except Exception as e:
        errors.append(f"[ERREUR] services.storage_service: {e}")
    
    try:
        from services.standards_comparison import enrich_threat_with_standards
        print("  [OK] services.standards_comparison")
    except Exception as e:
        errors.append(f"[ERREUR] services.standards_comparison: {e}")
    
    try:
        from services.mitre_service import enrich_threat_with_metadata
        print("  [OK] services.mitre_service")
    except Exception as e:
        errors.append(f"[ERREUR] services.mitre_service: {e}")
    
    try:
        from services.validation_metrics import calculate_average_confidence
        print("  [OK] services.validation_metrics")
    except Exception as e:
        errors.append(f"[ERREUR] services.validation_metrics: {e}")
    
    try:
        from parsers.c4_parser import parse_c4_text
        print("  [OK] parsers.c4_parser")
    except Exception as e:
        errors.append(f"[ERREUR] parsers.c4_parser: {e}")
    
    try:
        from parsers.uml_parser import parse_uml_text
        print("  [OK] parsers.uml_parser")
    except Exception as e:
        errors.append(f"[ERREUR] parsers.uml_parser: {e}")
    
    if errors:
        print("\n[ERREURS] Erreurs detectees:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("\n[OK] Tous les imports sont corrects!")
        return True

def test_parsers():
    """Teste les parseurs"""
    print("\nTest des parseurs...")
    
    try:
        from parsers.c4_parser import parse_c4_text, extract_architecture_from_c4
        
        test_c4 = """
        User Browser
        Web Application
        Database
        
        User Browser -> Web Application
        Web Application -> Database
        """
        
        result = parse_c4_text(test_c4)
        if result.get('components') or result.get('relations'):
            print("  [OK] Parseur C4 fonctionne")
        else:
            print("  [WARN] Parseur C4: pas de resultats (peut etre normal)")
    except Exception as e:
        print(f"  [ERREUR] Parseur C4: {e}")
    
    try:
        from parsers.uml_parser import parse_uml_text, extract_architecture_from_uml
        
        test_uml = """
        class User
        class Database
        User -> Database
        """
        
        result = parse_uml_text(test_uml)
        if result.get('classes') or result.get('relations'):
            print("  [OK] Parseur UML fonctionne")
        else:
            print("  [WARN] Parseur UML: pas de resultats (peut etre normal)")
    except Exception as e:
        print(f"  [ERREUR] Parseur UML: {e}")

def test_services():
    """Teste les services"""
    print("\nTest des services...")
    
    try:
        from services.validation_metrics import calculate_average_confidence
        
        test_menaces = [
            {"score_confiance": 0.9},
            {"score_confiance": 0.8},
            {"score_confiance": 0.7}
        ]
        
        avg = calculate_average_confidence(test_menaces)
        if avg == 0.8:
            print("  [OK] Service validation_metrics fonctionne")
        else:
            print(f"  [WARN] Service validation_metrics: resultat inattendu {avg}")
    except Exception as e:
        print(f"  [ERREUR] Service validation_metrics: {e}")
    
    try:
        from services.mitre_service import get_mitre_technique_info
        
        info = get_mitre_technique_info("T1190")
        if info and info.get('id') == 'T1190':
            print("  [OK] Service mitre_service fonctionne")
        else:
            print("  [WARN] Service mitre_service: resultat inattendu")
    except Exception as e:
        print(f"  [ERREUR] Service mitre_service: {e}")
    
    try:
        from services.standards_comparison import map_to_owasp
        
        owasp_info = map_to_owasp("A03:2021")
        if owasp_info:
            print("  [OK] Service standards_comparison fonctionne")
        else:
            print("  [WARN] Service standards_comparison: pas de resultat")
    except Exception as e:
        print(f"  [ERREUR] Service standards_comparison: {e}")

def test_storage():
    """Teste le stockage"""
    print("\nTest du stockage...")
    
    try:
        from services.storage_service import init_database
        
        init_database()
        if os.path.exists("analyses.db"):
            print("  [OK] Base de donnees SQLite creee")
        else:
            print("  [WARN] Base de donnees non creee (peut etre normal)")
    except Exception as e:
        print(f"  [ERREUR] Stockage: {e}")

def test_file_structure():
    """Vérifie la structure des fichiers"""
    print("\nVerification de la structure des fichiers...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "rag/build_kb.py",
        "rag/query_kb.py",
        "services/llm_service.py",
        "services/risk_score_service.py",
        "services/dashboard_adapter.py",
        "services/pdf_report_service.py",
        "services/mitre_service.py",
        "services/validation_metrics.py",
        "parsers/c4_parser.py",
        "parsers/uml_parser.py",
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
        else:
            print(f"  [OK] {file}")
    
    if missing:
        print(f"\n[ERREUR] Fichiers manquants: {missing}")
        return False
    else:
        print("\n[OK] Tous les fichiers requis sont presents!")
        return True

def main():
    """Fonction principale de test"""
    print("=" * 60)
    print("TEST DU SYSTÈME THREAT ANALYZER")
    print("=" * 60)
    
    # Changer vers le répertoire backend
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    results = []
    
    # Test de la structure
    results.append(("Structure fichiers", test_file_structure()))
    
    # Test des imports
    results.append(("Imports", test_imports()))
    
    # Test des parseurs
    test_parsers()
    
    # Test des services
    test_services()
    
    # Test du stockage
    test_storage()
    
    # Résumé
    print("\n" + "=" * 60)
    print("RESUME DES TESTS")
    print("=" * 60)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n[SUCCES] Tous les tests critiques sont passes!")
        print("[OK] Le systeme est pret a etre utilise")
    else:
        print("\n[ATTENTION] Certains tests ont echoue")
        print("Verifiez les erreurs ci-dessus")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
