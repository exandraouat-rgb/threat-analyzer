def calculate_risk_score(menaces: list) -> dict:
    """
    Calcule un score de risque global à partir des menaces détectées
    """

    poids = {
        "Faible": 1,
        "Moyenne": 2,
        "Élevée": 3,
        "Critique": 4
    }

    if not menaces:
        return {
            "score": 0,
            "niveau": "Faible",
            "couleur": "green"
        }

    total = 0
    max_possible = len(menaces) * 4

    for menace in menaces:
        gravite = menace.get("gravite", "Faible")
        total += poids.get(gravite, 1)

    score = int((total / max_possible) * 100)

    # Détermination du niveau
    if score < 30:
        niveau = "Faible"
        couleur = "green"
    elif score < 60:
        niveau = "Moyen"
        couleur = "yellow"
    elif score < 80:
        niveau = "Élevé"
        couleur = "orange"
    else:
        niveau = "Critique"
        couleur = "red"

    return {
        "score": score,
        "niveau": niveau,
        "couleur": couleur
    }
