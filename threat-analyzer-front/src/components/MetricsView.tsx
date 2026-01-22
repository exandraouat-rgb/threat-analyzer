import { useParams } from "react-router-dom";
import { useAnalysis } from "../context/AnalysisContext";

export default function MetricsView() {
  const { projectName } = useParams<{ projectName: string }>();
  const { getAnalysis } = useAnalysis();

  const analysis = projectName ? getAnalysis(decodeURIComponent(projectName)) : null;
  const metrics = analysis?.dashboard?.metriques;

  if (!analysis || !metrics) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gray-800 rounded-lg shadow-xl p-12 border border-gray-700 text-center">
            <div className="text-6xl mb-4">📊</div>
            <h2 className="text-3xl font-bold text-white mb-4">Métriques non disponibles</h2>
            <p className="text-gray-400">
              Les métriques de validation ne sont disponibles que pour les analyses récentes.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const confidenceScore = metrics.score_confiance_moyen || 0.8;
  const coverage = metrics.couverture || {};

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Métriques de validation</h1>
        <p className="text-gray-400 mb-8">Projet: <span className="text-white font-semibold">{analysis.project}</span></p>

        {/* Score de confiance moyen */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700 mb-6">
          <h2 className="text-2xl font-bold text-white mb-4">Score de confiance IA</h2>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-300">Confiance moyenne</span>
                <span className="text-2xl font-bold text-white">{Math.round(confidenceScore * 100)}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-4">
                <div
                  className={`h-4 rounded-full transition-all ${
                    confidenceScore >= 0.9 ? 'bg-green-500' :
                    confidenceScore >= 0.7 ? 'bg-yellow-500' :
                    'bg-orange-500'
                  }`}
                  style={{ width: `${confidenceScore * 100}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-400 mt-2">
                {confidenceScore >= 0.9 ? 'Très haute confiance' :
                 confidenceScore >= 0.7 ? 'Confiance modérée' :
                 'Confiance faible - vérification recommandée'}
              </p>
            </div>
          </div>
        </div>

        {/* Couverture des standards */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700 mb-6">
          <h2 className="text-2xl font-bold text-white mb-4">Couverture des standards</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-700/50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-300">OWASP Top 10</span>
                <span className="text-xl font-bold text-green-400">{coverage.owasp_coverage || 0}%</span>
              </div>
              <div className="w-full bg-gray-600 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${coverage.owasp_coverage || 0}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-gray-700/50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-300">MITRE ATT&CK</span>
                <span className="text-xl font-bold text-purple-400">{coverage.mitre_coverage || 0}%</span>
              </div>
              <div className="w-full bg-gray-600 rounded-full h-2">
                <div
                  className="bg-purple-500 h-2 rounded-full"
                  style={{ width: `${coverage.mitre_coverage || 0}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-gray-700/50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-300">CWE</span>
                <span className="text-xl font-bold text-blue-400">{coverage.cwe_coverage || 0}%</span>
              </div>
              <div className="w-full bg-gray-600 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full"
                  style={{ width: `${coverage.cwe_coverage || 0}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-gray-700/50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-300">CVSS Score</span>
                <span className="text-xl font-bold text-orange-400">{coverage.cvss_coverage || 0}%</span>
              </div>
              <div className="w-full bg-gray-600 rounded-full h-2">
                <div
                  className="bg-orange-500 h-2 rounded-full"
                  style={{ width: `${coverage.cvss_coverage || 0}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Statistiques générales */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          <h2 className="text-2xl font-bold text-white mb-4">Statistiques</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-white mb-1">{coverage.total_menaces || 0}</div>
              <div className="text-sm text-gray-400">Menaces totales</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-400 mb-1">{coverage.owasp_coverage || 0}%</div>
              <div className="text-sm text-gray-400">Couverture OWASP</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400 mb-1">{coverage.mitre_coverage || 0}%</div>
              <div className="text-sm text-gray-400">Couverture MITRE</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-400 mb-1">{Math.round(confidenceScore * 100)}%</div>
              <div className="text-sm text-gray-400">Confiance IA</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
