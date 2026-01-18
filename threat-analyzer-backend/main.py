from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import io
import os

from pypdf import PdfReader

from rag.build_kb import build_vector_db
from rag.query_kb import search_threats
from services.llm_service import analyze_with_claude
from services.risk_score_service import calculate_risk_score
from services.dashboard_adapter import adapt_for_dashboard
from services.pdf_report_service import generate_pdf_report

# -----------------------------------
# Initialisation
# -----------------------------------
app = FastAPI()

# Configuration CORS pour permettre la communication avec le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Construction de la base vectorielle UNE SEULE FOIS
vector_db = build_vector_db("Données.csv")

# -----------------------------------
# Endpoint health check
# -----------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend is running"}

# -----------------------------------
# Endpoint principal : Analyse
# -----------------------------------
@app.post("/analyze")
async def analyze_project(
    project_name: str = Form(...),
    app_type: str = Form(...),
    architecture_description: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        file_content = ""

        # -------------------------------
        # Lecture du fichier uploadé
        # -------------------------------
        if file:
            if file.filename.endswith(".json"):
                content = await file.read()
                file_content = json.dumps(json.loads(content), indent=2)

            elif file.filename.endswith(".pdf"):
                pdf_bytes = await file.read()
                reader = PdfReader(io.BytesIO(pdf_bytes))
                for page in reader.pages:
                    file_content += page.extract_text() or ""

            else:
                file_content = "Format non supporté"

        # -------------------------------
        # RAG : recherche des menaces
        # -------------------------------
        rag_query = f"""
Application : {app_type}
Architecture : {architecture_description}
"""

        relevant_threats = search_threats(vector_db, rag_query)
        rag_context = "\n\n".join(relevant_threats)

        # -------------------------------
        # Entrée utilisateur
        # -------------------------------
        user_input = f"""
Nom du projet : {project_name}
Type d'application : {app_type}
Architecture : {architecture_description}

Fichier fourni :
{file_content}
"""

        # -------------------------------
        # Analyse IA
        # -------------------------------
        analysis = analyze_with_claude(
            rag_context=rag_context,
            user_input=user_input
        )

        # Sécurité si l'IA retourne une erreur
        if "error" in analysis:
            return {
                "project": project_name,
                "error": analysis.get("error"),
                "score_risque": 0,
                "dashboard": {},
                "analysis": {"menaces": []}
            }

        # -------------------------------
        # Score + Dashboard
        # -------------------------------
        risk_score = calculate_risk_score(analysis.get("menaces", []))

        dashboard_data = adapt_for_dashboard(
            project_name=project_name,
            analysis=analysis,
            score_risque=risk_score
        )

        return {
            "project": project_name,
            "score_risque": risk_score.get("score", 0),
            "dashboard": dashboard_data,
            "analysis": analysis
        }
    
    except Exception as e:
        print(f"Erreur dans /analyze: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "project": project_name,
            "error": f"Erreur serveur: {str(e)}",
            "score_risque": 0,
            "dashboard": {},
            "analysis": {"menaces": []}
        }

# -----------------------------------
# Endpoint PDF
# -----------------------------------
@app.post("/generate-pdf")
def generate_pdf(
    project_name: str = Form(...),
    dashboard: str = Form(...),
    analysis: str = Form(...)
):
    """
    Génère et retourne le rapport PDF
    """

    os.makedirs("reports", exist_ok=True)

    dashboard_data = json.loads(dashboard)
    analysis_data = json.loads(analysis)

    file_path = f"reports/{project_name.replace(' ', '_')}_rapport.pdf"

    generate_pdf_report(
        project_name=project_name,
        dashboard=dashboard_data,
        analysis=analysis_data,
        output_path=file_path
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=os.path.basename(file_path)
    )
