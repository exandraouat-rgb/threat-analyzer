"""
Service pour calculer des métriques de validation de base
"""
from typing import List, Dict

def calculate_precision_recall(ground_truth: List[str], predictions: List[str]) -> Dict:
    """
    Calcule la précision et le rappel basiques
    ground_truth: Liste des menaces réellement présentes (annotations expertes)
    predictions: Liste des menaces détectées par l'IA
    """
    if not predictions:
        return {
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "true_positives": 0,
            "false_positives": 0,
            "false_negatives": 0
        }
    
    # Normaliser les noms pour la comparaison
    ground_truth_normalized = [t.lower().strip() for t in ground_truth]
    predictions_normalized = [p.lower().strip() for p in predictions]
    
    # Calculer les vrais positifs, faux positifs, faux négatifs
    true_positives = sum(1 for p in predictions_normalized if p in ground_truth_normalized)
    false_positives = len(predictions_normalized) - true_positives
    false_negatives = len(ground_truth_normalized) - true_positives
    
    # Calculer précision et rappel
    precision = true_positives / len(predictions_normalized) if predictions_normalized else 0.0
    recall = true_positives / len(ground_truth_normalized) if ground_truth_normalized else 0.0
    
    # Calculer F1-score
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1_score, 3),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "total_ground_truth": len(ground_truth),
        "total_predictions": len(predictions)
    }

def calculate_average_confidence(menaces: List[Dict]) -> float:
    """
    Calcule le score de confiance moyen pour toutes les menaces
    """
    if not menaces:
        return 0.0
    
    confidences = [m.get("score_confiance", 0.8) for m in menaces if m.get("score_confiance")]
    
    if not confidences:
        return 0.8  # Valeur par défaut
    
    return round(sum(confidences) / len(confidences), 3)

def calculate_coverage_metrics(menaces: List[Dict]) -> Dict:
    """
    Calcule des métriques de couverture (OWASP, MITRE, etc.)
    """
    total = len(menaces)
    
    owasp_count = sum(1 for m in menaces if m.get("owasp_category") and m.get("owasp_category") != "N/A")
    mitre_count = sum(1 for m in menaces if m.get("mitre_attack_id") and m.get("mitre_attack_id") != "N/A")
    cwe_count = sum(1 for m in menaces if m.get("cwe_id") and m.get("cwe_id") != "N/A")
    cvss_count = sum(1 for m in menaces if m.get("cvss_score") and m.get("cvss_score") != "N/A")
    
    return {
        "total_menaces": total,
        "owasp_coverage": round(owasp_count / total * 100, 1) if total > 0 else 0,
        "mitre_coverage": round(mitre_count / total * 100, 1) if total > 0 else 0,
        "cwe_coverage": round(cwe_count / total * 100, 1) if total > 0 else 0,
        "cvss_coverage": round(cvss_count / total * 100, 1) if total > 0 else 0
    }
