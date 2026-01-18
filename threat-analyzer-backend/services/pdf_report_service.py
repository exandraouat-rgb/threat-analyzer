from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import red, orange, green
import datetime


def generate_pdf_report(project_name: str, dashboard: dict, analysis: dict, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    elements = []

    # -------------------------
    # Titre
    # -------------------------
    elements.append(Paragraph(
        f"<b>Rapport d’analyse de menaces</b><br/>{project_name}",
        styles["Title"]
    ))

    elements.append(Spacer(1, 12))

    # -------------------------
    # Date
    # -------------------------
    date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"<i>Date :</i> {date_str}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # -------------------------
    # Résumé exécutif
    # -------------------------
    resume = dashboard["resume"]

    elements.append(Paragraph("<b>Résumé exécutif</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        f"""
        <b>Niveau global :</b> {resume['niveau_global']}<br/>
        <b>Score de risque :</b> {resume['score']} / 100<br/>
        <b>Niveau de risque :</b> {resume['niveau_risque']}
        """,
        styles["Normal"]
    ))

    elements.append(Spacer(1, 12))

    # -------------------------
    # Menaces identifiées
    # -------------------------
    elements.append(Paragraph("<b>Menaces identifiées</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    for menace in analysis.get("menaces", []):
        elements.append(Paragraph(
            f"<b>{menace['nom']}</b> (Gravité : {menace['gravite']})",
            styles["Normal"]
        ))

        elements.append(Paragraph(
            menace.get("description", ""),
            styles["BodyText"]
        ))

        recos = menace.get("recommandations", [])
        if recos:
            elements.append(Paragraph("<i>Recommandations :</i>", styles["Italic"]))
            elements.append(
                ListFlowable(
                    [ListItem(Paragraph(r, styles["BodyText"])) for r in recos],
                    bulletType="bullet"
                )
            )

        elements.append(Spacer(1, 10))

    # -------------------------
    # Génération
    # -------------------------
    doc.build(elements)
