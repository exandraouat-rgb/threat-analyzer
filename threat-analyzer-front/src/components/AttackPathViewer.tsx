import { useParams } from "react-router-dom";
import { useAnalysis } from "../context/AnalysisContext";

export default function AttackPathViewer() {
  const { projectName } = useParams<{ projectName: string }>();
  const { getAnalysis } = useAnalysis();

  const analysis = projectName ? getAnalysis(decodeURIComponent(projectName)) : null;
  const menaces = analysis?.analysis?.menaces || [];

  if (!analysis || menaces.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gray-800 rounded-lg shadow-xl p-12 border border-gray-700 text-center">
            <div className="text-6xl mb-4">🔗</div>
            <h2 className="text-3xl font-bold text-white mb-4">Aucun chemin d'attaque disponible</h2>
            <p className="text-gray-400">
              Les chemins d'attaque seront affichés ici une fois l'analyse complétée.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Grouper les menaces par gravité pour visualisation
  const menacesBySeverity = {
    Critique: menaces.filter((m: any) => m.gravite === "Critique"),
    Élevée: menaces.filter((m: any) => m.gravite === "Élevée"),
    Moyenne: menaces.filter((m: any) => m.gravite === "Moyenne"),
    Faible: menaces.filter((m: any) => m.gravite === "Faible"),
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "Critique":
        return "border-red-500 bg-red-500/10";
      case "Élevée":
        return "border-orange-500 bg-orange-500/10";
      case "Moyenne":
        return "border-yellow-500 bg-yellow-500/10";
      case "Faible":
        return "border-green-500 bg-green-500/10";
      default:
        return "border-gray-500 bg-gray-500/10";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">Chemins d'attaque</h1>
        <p className="text-gray-400 mb-8">Projet: <span className="text-white font-semibold">{analysis.project}</span></p>

        {/* Vue d'ensemble */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-6 border border-gray-700 mb-6">
          <h2 className="text-xl font-bold text-white mb-4">Vue d'ensemble des menaces</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(menacesBySeverity).map(([severity, threats]: [string, any]) => (
              <div key={severity} className="text-center">
                <div className={`text-3xl font-bold mb-1 ${
                  severity === "Critique" ? "text-red-400" :
                  severity === "Élevée" ? "text-orange-400" :
                  severity === "Moyenne" ? "text-yellow-400" :
                  "text-green-400"
                }`}>
                  {threats.length}
                </div>
                <div className="text-sm text-gray-400">{severity}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Chemins d'attaque par gravité */}
        {Object.entries(menacesBySeverity).map(([severity, threats]: [string, any]) => {
          if (threats.length === 0) return null;

          return (
            <div key={severity} className="mb-8">
              <h2 className="text-2xl font-bold text-white mb-4">
                Menaces {severity.toLowerCase()}
              </h2>
              <div className="space-y-4">
                {threats.map((menace: any, index: number) => (
                  <div
                    key={index}
                    className={`bg-gray-800 rounded-lg p-6 border-l-4 ${getSeverityColor(menace.gravite)}`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="text-xl font-bold text-white mb-2">{menace.nom}</h3>
                        {menace.mitre_attack_id && menace.mitre_attack_id !== "N/A" && (
                          <div className="flex items-center space-x-2 mb-2">
                            <span className="text-xs text-gray-400">MITRE ATT&CK:</span>
                            <a
                              href={menace.mitre_info?.url || `https://attack.mitre.org/techniques/${menace.mitre_attack_id.replace('T', '')}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-purple-400 hover:text-purple-300 text-sm font-semibold"
                            >
                              {menace.mitre_attack_id}
                            </a>
                          </div>
                        )}
                      </div>
                      {menace.score_confiance !== undefined && (
                        <div className="text-right">
                          <div className="text-xs text-gray-400 mb-1">Confiance</div>
                          <div className={`text-sm font-bold ${
                            menace.score_confiance >= 0.9 ? 'text-green-400' :
                            menace.score_confiance >= 0.7 ? 'text-yellow-400' :
                            'text-orange-400'
                          }`}>
                            {Math.round(menace.score_confiance * 100)}%
                          </div>
                        </div>
                      )}
                    </div>

                    <p className="text-gray-300 mb-4">{menace.description}</p>

                    {/* Recommandations */}
                    {menace.recommandations && menace.recommandations.length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-sm font-semibold text-white mb-2">Recommandations:</h4>
                        <ul className="list-disc list-inside space-y-1 text-sm text-gray-300">
                          {menace.recommandations.slice(0, 3).map((rec: string, recIndex: number) => (
                            <li key={recIndex}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* CVE associés */}
                    {menace.cves && menace.cves.length > 0 && (
                      <div className="mt-4">
                        <h4 className="text-sm font-semibold text-white mb-2">CVE associés:</h4>
                        <div className="flex flex-wrap gap-2">
                          {menace.cves.map((cve: any, cveIndex: number) => (
                            <a
                              key={cveIndex}
                              href={cve.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="px-3 py-1 bg-blue-600/20 border border-blue-500 rounded text-blue-400 hover:bg-blue-600/30 text-xs font-medium"
                            >
                              {cve.id} {cve.cvss_score && `(CVSS: ${cve.cvss_score})`}
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
