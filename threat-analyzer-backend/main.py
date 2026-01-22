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
from services.langchain_service import analyze_with_langchain
from services.nvd_service import enrich_threat_with_cve
from services.storage_service import save_analysis, init_database
from services.auth_service import register_user, login_user, get_user_by_id
from services.standards_comparison import enrich_threat_with_standards
from services.risk_score_service import calculate_risk_score
from services.dashboard_adapter import adapt_for_dashboard
from services.pdf_report_service import generate_pdf_report
from services.mitre_service import enrich_threat_with_metadata
from services.validation_metrics import calculate_average_confidence, calculate_coverage_metrics, calculate_precision_recall
from parsers.c4_parser import parse_c4_text, extract_architecture_from_c4
from parsers.uml_parser import parse_uml_text, extract_architecture_from_uml, parse_xmi_content

# -----------------------------------
# Initialisation
# -----------------------------------
app = FastAPI()

# Configuration CORS pour permettre la communication avec le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:5173"],
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
# Endpoints d'authentification
# -----------------------------------
@app.post("/api/auth/register")
async def register(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...)
):
    """
    Enregistre un nouvel utilisateur
    """
    try:
        user = register_user(email, password, name)
        if user:
            return {
                "success": True,
                "user": user,
                "message": "Inscription réussie"
            }
        else:
            return {
                "success": False,
                "message": "Cet email est déjà utilisé"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Erreur lors de l'inscription: {str(e)}"
        }

@app.post("/api/auth/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Authentifie un utilisateur
    """
    try:
        user = login_user(email, password)
        if user:
            return {
                "success": True,
                "user": user,
                "message": "Connexion réussie"
            }
        else:
            return {
                "success": False,
                "message": "Email ou mot de passe incorrect"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Erreur lors de la connexion: {str(e)}"
        }

@app.get("/api/auth/user/{user_id}")
async def get_user(user_id: str):
    """
    Récupère les informations d'un utilisateur par son ID
    """
    try:
        user = get_user_by_id(user_id)
        if user:
            return {
                "success": True,
                "user": user
            }
        else:
            return {
                "success": False,
                "message": "Utilisateur non trouvé"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Erreur: {str(e)}"
        }

# -----------------------------------
# Endpoint principal : Analyse
# -----------------------------------
@app.post("/analyze")
async def analyze_project(
    project_name: str = Form(...),
    app_type: str = Form(...),
    architecture_description: str = Form(...),
    file: Optional[UploadFile] = File(None),
    user_id: Optional[str] = Form(None)
):
    try:
        file_content = ""

        # -------------------------------
        # Lecture du fichier uploadé
        # -------------------------------
        c4_architecture = None
        if file:
            if file.filename.endswith(".json"):
                content = await file.read()
                file_content = json.dumps(json.loads(content), indent=2)
                # Essayer de parser comme C4 si c'est un fichier de diagramme
                try:
                    json_data = json.loads(content)
                    if isinstance(json_data, dict) and ('components' in json_data or 'systems' in json_data):
                        c4_architecture = extract_architecture_from_c4(json_data)
                except:
                    pass

            elif file.filename.endswith(".pdf"):
                pdf_bytes = await file.read()
                reader = PdfReader(io.BytesIO(pdf_bytes))
                for page in reader.pages:
                    file_content += page.extract_text() or ""
                # Essayer de parser le texte comme C4
                if file_content:
                    c4_data = parse_c4_text(file_content)
                    if c4_data.get('components'):
                        c4_architecture = extract_architecture_from_c4(c4_data)

            elif file.filename.endswith((".md", ".txt", ".c4")):
                content = await file.read()
                file_content = content.decode('utf-8')
                # Essayer de parser comme C4
                c4_data = parse_c4_text(file_content)
                if c4_data.get('components'):
                    c4_architecture = extract_architecture_from_c4(c4_data)
                else:
                    # Essayer de parser comme UML
                    uml_data = parse_uml_text(file_content)
                    if uml_data.get('classes') or uml_data.get('actors'):
                        c4_architecture = extract_architecture_from_uml(uml_data)
            
            elif file.filename.endswith((".xmi", ".xml")):
                # Parser comme UML XMI
                content = await file.read()
                file_content = content.decode('utf-8')
                
                # Essayer d'abord le parsing XMI (format standard)
                uml_data = parse_xmi_content(file_content)
                
                # Si le parsing XMI n'a rien donné, essayer le parsing texte
                if not uml_data or (not uml_data.get('classes') and not uml_data.get('actors') and not uml_data.get('use_cases') and not uml_data.get('relations')):
                    uml_data = parse_uml_text(file_content)
                
                if uml_data and (uml_data.get('classes') or uml_data.get('actors') or uml_data.get('use_cases') or uml_data.get('relations')):
                    c4_architecture = extract_architecture_from_uml(uml_data)

            else:
                file_content = "Format non supporté"
        
        # Si on a une architecture C4, l'ajouter à la description
        if c4_architecture:
            architecture_description = f"{architecture_description}\n\nArchitecture extraite du diagramme:\n{c4_architecture}"

        # -------------------------------
        # RAG : recherche des menaces
        # -------------------------------
        # Construire une requête plus spécifique selon le type d'application
        app_type_lower = app_type.lower()
        if "mobile" in app_type_lower or "ios" in app_type_lower or "android" in app_type_lower:
            rag_query = f"""
Application mobile iOS/Android : {app_type}
Architecture mobile : {architecture_description}
Menaces spécifiques aux applications mobiles, stockage local, certificate pinning, OAuth mobile
"""
        elif "web" in app_type_lower or "site" in app_type_lower:
            rag_query = f"""
Application web : {app_type}
Architecture web : {architecture_description}
Menaces spécifiques aux applications web, SQL injection, XSS, authentification web
"""
        elif "api" in app_type_lower or "rest" in app_type_lower or "graphql" in app_type_lower:
            rag_query = f"""
API REST/GraphQL : {app_type}
Architecture API : {architecture_description}
Menaces spécifiques aux APIs, accès non autorisé API, rate limiting, authentification API
"""
        else:
            rag_query = f"""
Application : {app_type}
Architecture : {architecture_description}
"""

        # Augmenter le nombre de résultats pour avoir plus de contexte, puis Claude filtrera
        relevant_threats = search_threats(vector_db, rag_query, k=10)
        
        # Filtrage préliminaire selon le type d'application
        filtered_threats = []
        app_type_lower = app_type.lower()
        
        for threat in relevant_threats:
            threat_lower = threat.lower()
            # Pour applications mobiles : garder seulement les menaces mobiles, ignorer les menaces web explicites
            if "mobile" in app_type_lower or "ios" in app_type_lower or "android" in app_type_lower:
                # Ignorer les menaces qui mentionnent explicitement "web" ou "serveur web" sauf si elles mentionnent aussi "mobile"
                if ("application web" in threat_lower or "serveur web" in threat_lower) and "mobile" not in threat_lower:
                    continue
                # Garder les menaces qui mentionnent mobile, iOS, Android, ou qui sont génériques (API, backend)
                if any(keyword in threat_lower for keyword in ["mobile", "ios", "android", "api", "backend", "oauth", "s3", "firebase"]):
                    filtered_threats.append(threat)
                elif "application web" not in threat_lower:
                    # Garder les menaces génériques qui ne sont pas spécifiquement web
                    filtered_threats.append(threat)
            # Pour applications web : garder seulement les menaces web, ignorer les menaces mobiles explicites
            elif "web" in app_type_lower or "site" in app_type_lower:
                # Ignorer les menaces qui mentionnent explicitement "mobile", "ios", "android" sauf si elles mentionnent aussi "web"
                if ("mobile" in threat_lower or "ios" in threat_lower or "android" in threat_lower) and "web" not in threat_lower:
                    continue
                filtered_threats.append(threat)
            # Pour APIs : garder les menaces API et backend, ignorer les menaces UI
            elif "api" in app_type_lower or "rest" in app_type_lower or "graphql" in app_type_lower:
                # Ignorer les menaces spécifiques aux interfaces utilisateur
                if ("application web" in threat_lower or "application mobile" in threat_lower) and "api" not in threat_lower:
                    continue
                filtered_threats.append(threat)
            else:
                # Pour les autres types, garder tout
                filtered_threats.append(threat)
        
        # Si le filtrage a supprimé trop de résultats, garder au moins les 5 premiers
        if len(filtered_threats) < 3:
            filtered_threats = relevant_threats[:5]
        
        rag_context = "\n\n".join(filtered_threats)

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
        # Analyse IA (avec LangChain si disponible, sinon Claude direct)
        # -------------------------------
        try:
            # Essayer avec LangChain d'abord (meilleure orchestration)
            analysis = analyze_with_langchain(
                rag_context=rag_context,
                user_input=user_input
            )
            # Si erreur, fallback sur Claude direct
            if "error" in analysis:
                analysis = analyze_with_claude(
                    rag_context=rag_context,
                    user_input=user_input
                )
        except Exception as e:
            # Fallback sur Claude direct en cas d'erreur
            print(f"Erreur LangChain, fallback sur Claude: {e}")
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
        # Enrichissement des menaces avec métadonnées
        # -------------------------------
        enriched_menaces = []
        for menace in analysis.get("menaces", []):
            enriched_menace = enrich_threat_with_metadata(menace)
            
            # Enrichir avec CVE depuis NVD
            try:
                cves = enrich_threat_with_cve(
                    threat_name=enriched_menace.get("nom", ""),
                    cwe_id=enriched_menace.get("cwe_id", "")
                )
                if cves:
                    enriched_menace["cves"] = cves
            except Exception as e:
                print(f"Erreur enrichissement CVE: {e}")
                # Continuer sans CVE si erreur
            
            # Enrichir avec comparaison standards
            enriched_menace = enrich_threat_with_standards(enriched_menace)
            
            enriched_menaces.append(enriched_menace)
        
        analysis["menaces"] = enriched_menaces

        # -------------------------------
        # Score + Dashboard
        # -------------------------------
        risk_score = calculate_risk_score(analysis.get("menaces", []))

        dashboard_data = adapt_for_dashboard(
            project_name=project_name,
            analysis=analysis,
            score_risque=risk_score
        )
        
        # Calculer métriques de validation
        avg_confidence = calculate_average_confidence(enriched_menaces)
        coverage_metrics = calculate_coverage_metrics(enriched_menaces)
        
        # Ajouter les métriques au dashboard
        dashboard_data["metriques"] = {
            "score_confiance_moyen": avg_confidence,
            "couverture": coverage_metrics
        }

        # Sauvegarder dans la base de données
        try:
            init_database()
            analysis_id = save_analysis(
                project_name=project_name,
                user_id=user_id,
                app_type=app_type,
                architecture_description=architecture_description,
                dashboard=dashboard_data,
                analysis=analysis
            )
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            # Continuer même si la sauvegarde échoue

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

# -----------------------------------
# Endpoint métriques de validation
# -----------------------------------
@app.get("/metrics/{project_name}")
def get_validation_metrics(project_name: str):
    """
    Retourne les métriques de validation pour un projet
    Note: Nécessite que le projet ait été analysé
    """
    # Pour l'instant, retourne un exemple
    # Dans une vraie implémentation, on récupérerait depuis une base de données
    return {
        "project": project_name,
        "message": "Les métriques sont calculées lors de l'analyse et incluses dans le dashboard",
        "note": "Utilisez l'endpoint /analyze pour obtenir les métriques avec l'analyse"
    }

@app.post("/validate")
def validate_analysis(
    ground_truth: str = Form(...),  # JSON avec liste des menaces réelles
    predictions: str = Form(...)    # JSON avec liste des menaces détectées
):
    """
    Calcule les métriques de validation (précision, rappel, F1-score)
    entre les menaces réelles (ground truth) et les prédictions
    """
    try:
        gt_list = json.loads(ground_truth)
        pred_list = json.loads(predictions)
        
        metrics = calculate_precision_recall(gt_list, pred_list)
        
        return {
            "status": "success",
            "metrics": metrics
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
