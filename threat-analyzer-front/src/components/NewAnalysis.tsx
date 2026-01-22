import { useState } from "react";
import type { ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import { API_ENDPOINTS } from "../config";
import { useAnalysis } from "../context/AnalysisContext";
import { useAuth } from "../context/AuthContext";
import BackendStatus from "./BackendStatus";

export default function NewAnalysis() {
  const navigate = useNavigate();
  const { addAnalysis } = useAnalysis();
  const { user } = useAuth();

  const [form, setForm] = useState({
    project_name: "",
    app_type: "Web",
    architecture_description: "",
  });
  const [file, setFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);
  const [importFile, setImportFile] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
    if (selectedFile) {
      setFilePreview(selectedFile.name);
    } else {
      setFilePreview(null);
    }
  };

  const handleSubmit = async () => {
    if (!form.project_name || !form.app_type || !form.architecture_description) {
      setError("Veuillez remplir tous les champs obligatoires");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = new FormData();
      data.append("project_name", form.project_name);
      data.append("app_type", form.app_type);
      data.append("architecture_description", form.architecture_description);
      if (file) data.append("file", file);
      // Ajouter l'ID utilisateur si l'utilisateur est connecté
      if (user?.id) {
        data.append("user_id", user.id);
      }

      const res = await fetch(API_ENDPOINTS.ANALYZE, {
        method: "POST",
        body: data,
      });

      if (!res.ok) {
        const errorText = await res.text();
        let errorMessage = `Erreur serveur (${res.status})`;
        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.error || errorJson.message || errorMessage;
        } catch {
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      const json = await res.json();
      
      if (json.error) {
        setError(json.error);
      } else {
        addAnalysis(json);
        navigate(`/rapports/${encodeURIComponent(json.project)}`);
      }
    } catch (err) {
      if (err instanceof TypeError && (err.message.includes('fetch') || err.message.includes('Failed to fetch'))) {
        setError(
          "❌ Impossible de se connecter au serveur backend.\n\n" +
          "Vérifiez que:\n" +
          "1. Le backend est démarré (port 8000)\n" +
          "2. Exécutez: cd threat-analyzer-backend; python -m uvicorn main:app --reload --port 8000\n" +
          "3. Ou utilisez le script PowerShell: ..\\start-backend.ps1"
        );
      } else {
        setError(err instanceof Error ? err.message : "Erreur de connexion au serveur");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Nouvelle analyse</h1>

        {/* Statut du backend */}
        <div className="mb-6">
          <BackendStatus />
        </div>

        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          {error && (
            <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-6">
              <div className="flex items-start">
                <span className="text-xl mr-3">⚠️</span>
                <div className="flex-1">
                  <h3 className="font-bold mb-2">Erreur</h3>
                  <p className="whitespace-pre-line text-sm">{error}</p>
                </div>
              </div>
            </div>
          )}

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Nom du projet *
              </label>
              <input
                type="text"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nom du projet"
                name="project_name"
                value={form.project_name}
                onChange={handleChange}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Type d'application *
              </label>
              <select
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                name="app_type"
                value={form.app_type}
                onChange={handleChange}
              >
                <option value="Web">Web</option>
                <option value="API REST">API REST</option>
                <option value="Mobile App">Mobile App</option>
                <option value="Desktop">Desktop</option>
                <option value="Microservices">Microservices</option>
                <option value="Autre">Autre</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Description de l'architecture *
              </label>
              <textarea
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                rows={6}
                placeholder="Décrivez votre architecture: microservices, monolithe, cloud, etc."
                name="architecture_description"
                value={form.architecture_description}
                onChange={handleChange}
              />
            </div>

            <div>
              <label className="flex items-center space-x-2 mb-3">
                <input
                  type="checkbox"
                  checked={importFile}
                  onChange={(e) => setImportFile(e.target.checked)}
                  className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                />
                <span className="text-sm font-medium text-gray-300">
                  Importer un fichier de description (PDF, JSON, YAML)
                </span>
              </label>

              {importFile && (
                <div className="space-y-3">
                  <input
                    type="file"
                    className="w-full px-4 py-2 bg-gray-700 border-2 border-dashed border-gray-600 rounded-lg text-white cursor-pointer hover:border-blue-500 transition-colors"
                    onChange={handleFileChange}
                    accept=".pdf,.json,.yaml,.yml"
                  />
                  {filePreview && (
                    <div className="flex items-center justify-between bg-gray-700 p-3 rounded-lg">
                      <span className="text-gray-300">📄 {filePreview}</span>
                      <button
                        onClick={() => {
                          setFile(null);
                          setFilePreview(null);
                        }}
                        className="text-red-400 hover:text-red-300"
                      >
                        ✕
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>

            <button
              onClick={handleSubmit}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold text-lg py-4 rounded-lg shadow-lg hover:shadow-xl transition-all disabled:bg-gray-600 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <span className="inline-block animate-spin mr-2">⏳</span>
                  Analyse en cours...
                </span>
              ) : (
                "Analyser avec l'IA"
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
