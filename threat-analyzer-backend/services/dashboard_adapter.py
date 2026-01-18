def adapt_for_dashboard(project_name: str, analysis: dict, score_risque: dict) -> dict:
    menaces = analysis.get("menaces", [])

    # Comptage par gravité
    gravite_count = {
        "Faible": 0,
        "Moyenne": 0,
        "Élevée": 0,
        "Critique": 0
    }

    for m in menaces:
        gravite = m.get("gravite", "Faible")
        if gravite in gravite_count:
            gravite_count[gravite] += 1

    # Données pour graphique circulaire
    repartition_gravite = [
        {"label": g, "value": v}
        for g, v in gravite_count.items()
        if v > 0
    ]

    # Menaces critiques / élevées (top)
    menaces_cles = [
        {
            "nom": m.get("nom"),
            "gravite": m.get("gravite"),
            "description": m.get("description")
        }
        for m in menaces
        if m.get("gravite") in ["Critique", "Élevée"]
    ]

    return {
        "resume": {
            "projet": project_name,
            "niveau_global": analysis.get("niveau_global"),
            "score": score_risque.get("score"),
            "niveau_risque": score_risque.get("niveau"),
            "couleur": score_risque.get("couleur")
        },
        "statistiques": {
            "total_menaces": len(menaces),
            "par_gravite": gravite_count
        },
        "repartition_gravite": repartition_gravite,
        "menaces_cles": menaces_cles
    }
