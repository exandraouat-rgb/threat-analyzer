import { useParams, useNavigate } from "react-router-dom";
import { useAnalysis } from "../context/AnalysisContext";
import { API_ENDPOINTS } from "../config";

export default function ThreatDetail() {
  const { projectName, threatName } = useParams<{ projectName: string; threatName: string }>();
  const navigate = useNavigate();
  const { getAnalysis } = useAnalysis();

  const analysis = projectName ? getAnalysis(decodeURIComponent(projectName)) : null;
  const threat = analysis?.analysis?.menaces?.find(
    (m) => m.nom === decodeURIComponent(threatName || "")
  );

  if (!analysis || !threat) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gray-800 rounded-lg shadow-xl p-12 border border-gray-700 text-center">
            <div className="text-6xl mb-4">❌</div>
            <h2 className="text-3xl font-bold text-white mb-4">Menace non trouvée</h2>
            <button
              onClick={() => navigate("/rapports")}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded-lg shadow-lg hover:shadow-xl transition-all"
            >
              Retour aux résultats
            </button>
          </div>
        </div>
      </div>
    );
  }

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case "critique":
        return "bg-red-600 text-white";
      case "élevée":
        return "bg-orange-500 text-white";
      case "moyenne":
        return "bg-yellow-500 text-white";
      case "faible":
        return "bg-green-500 text-white";
      default:
        return "bg-gray-600 text-white";
    }
  };

  const downloadPDF = async () => {
    try {
      const data = new FormData();
      data.append("project_name", analysis.project);
      data.append("dashboard", JSON.stringify(analysis.dashboard));
      data.append("analysis", JSON.stringify(analysis.analysis));

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
      a.download = `${analysis.project}_rapport.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Erreur lors du téléchargement");
    }
  };

  // Calculer la taille approximative du PDF (simulation)
  const pdfSize = "230K";

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Navigation retour */}
        <button
          onClick={() => navigate(`/rapports/${encodeURIComponent(analysis.project)}`)}
          className="text-blue-400 hover:text-blue-300 font-medium mb-6 flex items-center"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Retour aux résultats
        </button>

        {/* Titre de la menace */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700 mb-6">
          <div className="flex items-start justify-between mb-4">
            <h1 className="text-3xl font-bold text-white">{threat.nom}</h1>
            <div className="flex space-x-2">
              <span className={`px-4 py-2 rounded-full text-sm font-medium ${getSeverityColor(threat.gravite)}`}>
                {threat.gravite}
              </span>
            </div>
          </div>
          
          {/* Métadonnées et score de confiance */}
          <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
            {threat.cwe_id && threat.cwe_id !== "N/A" && (
              <div className="bg-gray-700/50 rounded-lg p-3">
                <div className="text-xs text-gray-400 mb-1">CWE ID</div>
                <a
                  href={threat.cwe_info?.url || `https://cwe.mitre.org/data/definitions/${threat.cwe_id.replace('CWE-', '')}.html`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 font-semibold text-sm"
                >
                  {threat.cwe_id}
                </a>
              </div>
            )}
            
            {threat.cvss_score && threat.cvss_score !== "N/A" && (
              <div className="bg-gray-700/50 rounded-lg p-3">
                <div className="text-xs text-gray-400 mb-1">CVSS Score</div>
                <div className={`font-bold text-sm ${
                  parseFloat(threat.cvss_score) >= 9.0 ? 'text-red-400' :
                  parseFloat(threat.cvss_score) >= 7.0 ? 'text-orange-400' :
                  parseFloat(threat.cvss_score) >= 4.0 ? 'text-yellow-400' :
                  'text-green-400'
                }`}>
                  {threat.cvss_score}
                </div>
              </div>
            )}
            
            {threat.mitre_attack_id && threat.mitre_attack_id !== "N/A" && (
              <div className="bg-gray-700/50 rounded-lg p-3">
                <div className="text-xs text-gray-400 mb-1">MITRE ATT&CK</div>
                <a
                  href={threat.mitre_info?.url || `https://attack.mitre.org/techniques/${threat.mitre_attack_id.replace('T', '')}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-purple-400 hover:text-purple-300 font-semibold text-sm"
                >
                  {threat.mitre_attack_id}
                </a>
              </div>
            )}
            
            {threat.owasp_category && threat.owasp_category !== "N/A" && (
              <div className="bg-gray-700/50 rounded-lg p-3">
                <div className="text-xs text-gray-400 mb-1">OWASP</div>
                <div className="text-green-400 font-semibold text-sm">{threat.owasp_category}</div>
              </div>
            )}
          </div>
          
          {/* Score de confiance IA */}
          {threat.score_confiance !== undefined && (
            <div className="mt-4 bg-gray-700/30 rounded-lg p-3">
              <div className="flex items-center justify-between">
                <div className="text-sm text-gray-400">Score de confiance IA</div>
                <div className="flex items-center space-x-2">
                  <div className="w-32 bg-gray-700 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        threat.score_confiance >= 0.9 ? 'bg-green-500' :
                        threat.score_confiance >= 0.7 ? 'bg-yellow-500' :
                        'bg-orange-500'
                      }`}
                      style={{ width: `${threat.score_confiance * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-white">
                    {Math.round(threat.score_confiance * 100)}%
                  </span>
                </div>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {threat.score_confiance >= 0.9 ? 'Très sûr' :
                 threat.score_confiance >= 0.7 ? 'Assez sûr' :
                 'Moins sûr - vérification recommandée'}
              </div>
            </div>
          )}
          
          {/* Comparaison avec standards */}
          {(threat.owasp_info || threat.cis_controls || threat.nist_csf) && (
            <div className="mt-4 bg-gray-700/30 rounded-lg p-4">
              <div className="text-sm font-semibold text-white mb-3">Mappings standards de sécurité</div>
              <div className="space-y-2">
                {threat.owasp_info && (
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-400">OWASP:</span>
                    <a
                      href={threat.owasp_info.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-green-400 hover:text-green-300 text-sm font-medium"
                    >
                      {threat.owasp_info.id} - {threat.owasp_info.name}
                    </a>
                  </div>
                )}
                {threat.cis_controls && threat.cis_controls.length > 0 && (
                  <div>
                    <span className="text-xs text-gray-400">CIS Controls:</span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {threat.cis_controls.map((cis: any, idx: number) => (
                        <span key={idx} className="px-2 py-1 bg-blue-600/20 border border-blue-500 rounded text-blue-400 text-xs">
                          {cis.id}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {threat.nist_csf && threat.nist_csf.length > 0 && (
                  <div>
                    <span className="text-xs text-gray-400">NIST CSF:</span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {threat.nist_csf.map((nist: any, idx: number) => (
                        <span key={idx} className="px-2 py-1 bg-purple-600/20 border border-purple-500 rounded text-purple-400 text-xs">
                          {nist.id}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Analyse par IA */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700 mb-6">
          <h2 className="text-2xl font-bold text-white mb-4">Analyse par IA</h2>
          
          <div className="space-y-4 text-gray-300">
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">
                1. Exigences et critères de menace associés
              </h3>
              <p className="text-gray-300">{threat.description}</p>
            </div>

            {threat.recommandations && threat.recommandations.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <svg className="w-5 h-5 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Recommandations de mitigation ({threat.recommandations.length})
                </h3>
                <div className="space-y-3">
                  {threat.recommandations.map((rec, index) => (
                    <div
                      key={index}
                      className="bg-gray-700/50 rounded-lg p-4 border-l-4 border-blue-500 hover:bg-gray-700 transition-colors"
                    >
                      <div className="flex items-start">
                        <div className="flex-shrink-0 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-bold mr-3 mt-0.5">
                          {index + 1}
                        </div>
                        <p className="text-gray-200 flex-1 leading-relaxed">{rec}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Actions de rapports */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          <div className="flex flex-col sm:flex-row gap-4">
            <button
              onClick={downloadPDF}
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transition-all"
            >
              Télécharger rapport (PDF)
            </button>
            <button
              onClick={() => navigate("/rapports")}
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
            >
              Exporter ({pdfSize})
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
