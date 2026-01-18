import { useState } from "react";
import type { ChangeEvent } from "react";
import { API_ENDPOINTS } from "./config";
import "./App.css";

interface ThreatResult {
  project: string;
  score_risque: number;
  dashboard: object;
  analysis: {
    menaces: Array<{
      nom: string;
      gravite: string;
      description: string;
    }>;
  };
  error?: string;
}

const getSeverityColor = (severity: string): string => {
  switch (severity.toLowerCase()) {
    case "critique":
      return "threat-badge-critique";
    case "élevée":
      return "threat-badge-elevee";
    case "moyenne":
      return "threat-badge-moyenne";
    case "faible":
      return "threat-badge-faible";
    default:
      return "threat-badge-faible";
  }
};

const getScoreColor = (score: number): string => {
  if (score >= 80) return "score-critical";
  if (score >= 60) return "score-high";
  if (score >= 30) return "score-medium";
  return "score-low";
};

export default function ThreatAnalyzerApp() {
  const [form, setForm] = useState({
    project_name: "",
    app_type: "",
    architecture_description: "",
  });
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<ThreatResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    if (!form.project_name || !form.app_type || !form.architecture_description) {
      setError("Veuillez remplir tous les champs obligatoires");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = new FormData();
      data.append("project_name", form.project_name);
      data.append("app_type", form.app_type);
      data.append("architecture_description", form.architecture_description);
      if (file) data.append("file", file);

      const res = await fetch(API_ENDPOINTS.ANALYZE, {
        method: "POST",
        body: data,
      });

      if (!res.ok) {
        throw new Error(`Erreur serveur: ${res.status}`);
      }

      const json: ThreatResult = await res.json();
      
      if (json.error) {
        setError(json.error);
      } else {
        setResult(json);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur de connexion au serveur");
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async () => {
    if (!result) return;
    
    try {
      const data = new FormData();
      data.append("project_name", result.project);
      data.append("dashboard", JSON.stringify(result.dashboard));
      data.append("analysis", JSON.stringify(result.analysis));

      const res = await fetch(API_ENDPOINTS.GENERATE_PDF, {
        method: "POST",
        body: data,
      });

      if (!res.ok) {
        throw new Error("Erreur lors de la génération du PDF");
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${result.project}_rapport.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur lors du téléchargement");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 animate-slideIn">
          <h1 className="text-5xl font-bold text-gray-900 mb-2">🔒 Threat Analyzer</h1>
          <p className="text-gray-600 text-lg">Analyse complète des menaces de sécurité</p>
        </div>

        {/* Main Card */}
        <div className="card animate-slideIn">
          {/* Error Message */}
          {error && (
            <div className="error-message mb-6">
              <div className="flex items-start">
                <span className="text-xl mr-3">⚠️</span>
                <div>
                  <h3 className="font-bold">Erreur</h3>
                  <p>{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Form Section */}
          {!result && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Informations du Projet</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Nom du projet *</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="Ex: Mon Application Web"
                    name="project_name"
                    value={form.project_name}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Type d'application *</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="Ex: Application Web, API REST, Mobile App"
                    name="app_type"
                    value={form.app_type}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Description de l'architecture *</label>
                  <textarea
                    className="form-textarea"
                    rows={4}
                    placeholder="Décrivez votre architecture: microservices, monolithe, cloud, etc."
                    name="architecture_description"
                    value={form.architecture_description}
                    onChange={handleChange}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Fichier (optionnel)</label>
                  <input
                    type="file"
                    className="w-full px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 transition-colors"
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setFile(e.target.files?.[0] || null)}
                    accept=".json,.pdf"
                  />
                  {file && <p className="text-sm text-gray-600 mt-2">📄 {file.name}</p>}
                </div>

                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="btn-primary w-full mt-6 text-lg py-3"
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <span className="inline-block animate-spin mr-2">⏳</span>
                      Analyse en cours...
                    </span>
                  ) : (
                    "🔍 Analyser le Projet"
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Results Section */}
          {result && !result.error && (
            <div className="animate-slideIn">
              <button
                onClick={() => setResult(null)}
                className="text-blue-600 hover:text-blue-700 font-medium mb-4 text-sm"
              >
                ← Retour à l'analyse
              </button>

              <h2 className="text-3xl font-bold text-gray-800 mb-2">Résultats de l'Analyse</h2>
              <p className="text-gray-600 mb-6">Projet: <span className="font-semibold">{result.project}</span></p>

              {/* Score Card */}
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-8 mb-8 text-center border-2 border-blue-200">
                <p className="text-gray-700 text-lg mb-2">Score de Risque Global</p>
                <p className={`score-display ${getScoreColor(result.score_risque)}`}>
                  {result.score_risque}
                  <span className="text-2xl">/100</span>
                </p>
                <p className="text-gray-600 text-sm mt-2">
                  {result.score_risque >= 80 && "🔴 Critique - Action immédiate requise"}
                  {result.score_risque >= 60 && result.score_risque < 80 && "🟠 Élevé - Attention particulière requise"}
                  {result.score_risque >= 30 && result.score_risque < 60 && "🟡 Moyen - Surveillance recommandée"}
                  {result.score_risque < 30 && "🟢 Faible - Bonne posture de sécurité"}
                </p>
              </div>

              {/* Threats List */}
              <div>
                <h3 className="text-2xl font-bold text-gray-800 mb-4">Menaces Détectées ({result.analysis.menaces.length})</h3>
                
                {result.analysis.menaces.length > 0 ? (
                  <div className="grid grid-cols-1 gap-4">
                    {result.analysis.menaces.map((m, i: number) => (
                      <div key={i} className="border-l-4 border-gray-300 bg-gray-50 p-4 rounded hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-bold text-lg text-gray-800">{m.nom}</h4>
                            <span className={`threat-badge ${getSeverityColor(m.gravite)}`}>
                              {m.gravite}
                            </span>
                          </div>
                        </div>
                        <p className="text-gray-700 mt-3">{m.description}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="success-message">
                    ✅ Aucune menace détectée - Excellent!
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4 mt-8 pt-6 border-t">
                <button
                  onClick={downloadPDF}
                  className="btn-secondary flex-1 text-lg py-3"
                >
                  📥 Télécharger le Rapport PDF
                </button>
                <button
                  onClick={() => setResult(null)}
                  className="btn-primary flex-1 text-lg py-3"
                >
                  🔄 Nouvelle Analyse
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-600 text-sm">
          <p>🔐 Threat Analyzer - Analyse de sécurité alimentée par l'IA</p>
        </div>
      </div>
    </div>
  );
}
