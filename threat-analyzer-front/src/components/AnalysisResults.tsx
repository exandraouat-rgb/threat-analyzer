import { useParams, useNavigate, Link } from "react-router-dom";
import { useAnalysis } from "../context/AnalysisContext";

export default function AnalysisResults() {
  const { projectName } = useParams<{ projectName: string }>();
  const navigate = useNavigate();
  const { getAnalysis, analyses, deleteAnalysis, clearAnalyses } = useAnalysis();

  // Si un projet spécifique est demandé, l'afficher
  // Sinon, afficher le dernier projet ou un état vide
  const analysis = projectName ? getAnalysis(decodeURIComponent(projectName)) : analyses[0];

  // Calculer les statistiques
  const totalThreats = analysis?.analysis?.menaces?.length || 0;
  const stats = analysis?.dashboard?.statistiques?.par_gravite || {
    Critique: 0,
    Élevée: 0,
    Moyenne: 0,
    Faible: 0,
  };

  const niveauGlobal = analysis?.dashboard?.resume?.niveau_global || analysis?.analysis?.niveau_global || "FAIBLE";
  const menacesCles = analysis?.dashboard?.menaces_cles || [];

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

  const getSeverityIcon = (severity: string) => {
    switch (severity.toLowerCase()) {
      case "critique":
        return "🔴";
      case "élevée":
        return "🟠";
      case "moyenne":
        return "🟡";
      case "faible":
        return "🟢";
      default:
        return "⚪";
    }
  };

  const handleDeleteAnalysis = (projectToDelete: string) => {
    if (window.confirm(`Êtes-vous sûr de vouloir supprimer l'analyse "${projectToDelete}" ? Cette action est irréversible.`)) {
      deleteAnalysis(projectToDelete);
      
      // Si on supprime l'analyse actuellement affichée, rediriger
      if (analysis?.project === projectToDelete) {
        const remainingAnalyses = analyses.filter((a) => a.project !== projectToDelete);
        if (remainingAnalyses.length > 0) {
          navigate(`/rapports/${encodeURIComponent(remainingAnalyses[0].project)}`);
        } else {
          navigate("/rapports");
        }
      }
    }
  };

  // Déterminer si on affiche un état vide
  const isEmpty = !analysis && analyses.length === 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">Résultats de l'analyse</h1>

        {isEmpty && (
          <div className="bg-gray-800 rounded-lg shadow-xl p-12 border border-gray-700 text-center mb-8">
            <div className="text-6xl mb-4">📊</div>
            <h2 className="text-2xl font-bold text-white mb-4">Aucune analyse disponible</h2>
            <p className="text-gray-400 mb-8">
              Vous n'avez pas encore effectué d'analyse. Lancez votre première analyse pour voir les résultats ici.
            </p>
            <Link
              to="/nouvelle-analyse"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded-lg shadow-lg hover:shadow-xl transition-all"
            >
              Lancer une analyse
            </Link>
          </div>
        )}

        {analysis && (
          <div className="mb-4 flex items-center justify-between">
            <div className="text-gray-400">
              Projet: <span className="text-white font-semibold">{analysis.project}</span>
            </div>
            <button
              onClick={() => handleDeleteAnalysis(analysis.project)}
              className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors text-sm font-medium"
              title="Supprimer cette analyse"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span>Supprimer</span>
            </button>
          </div>
        )}

        {/* Synthèse des Menaces */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-gray-400 mb-2">Menaces détectées</div>
                <div className="flex items-center space-x-3">
                  <div className={`w-16 h-16 ${totalThreats > 0 ? 'bg-red-600' : 'bg-gray-600'} rounded-full flex items-center justify-center text-2xl font-bold text-white`}>
                    {totalThreats}
                  </div>
                  <div>
                    <div className="text-lg font-semibold text-white">
                      {totalThreats > 0 ? (stats.Critique > 0 ? 'Critique' : 'Détectées') : 'Aucune'}
                    </div>
                    <div className="text-sm text-gray-400">Niveau de risque</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="text-sm text-gray-400 mb-2">Niveau global</div>
            <div className={`text-2xl font-bold ${totalThreats > 0 ? 'text-blue-400' : 'text-gray-500'}`}>
              {totalThreats > 0 ? niveauGlobal.toUpperCase() : 'FAIBLE'}
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="text-sm text-gray-400 mb-2">Recommandations disponibles</div>
            <div className="flex items-center space-x-3">
              <div className={`w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl font-bold text-white`}>
                {analysis?.dashboard?.statistiques?.total_recommandations || 
                 analysis?.analysis?.menaces?.reduce((acc: number, m: any) => acc + (m.recommandations?.length || 0), 0) || 0}
              </div>
              <div>
                <div className="text-lg font-semibold text-white">Recommandations</div>
                <div className="text-sm text-gray-400">Actions suggérées</div>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="text-sm text-gray-400 mb-2">Confiance IA moyenne</div>
            <div className="flex items-center space-x-3">
              <div className={`w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold text-white ${
                (analysis?.dashboard?.metriques?.score_confiance_moyen || 0) >= 0.9 ? 'bg-green-600' :
                (analysis?.dashboard?.metriques?.score_confiance_moyen || 0) >= 0.7 ? 'bg-yellow-600' :
                'bg-orange-600'
              }`}>
                {Math.round((analysis?.dashboard?.metriques?.score_confiance_moyen || 0.8) * 100)}%
              </div>
              <div>
                <div className="text-lg font-semibold text-white">Confiance</div>
                <div className="text-sm text-gray-400">Score moyen</div>
              </div>
            </div>
          </div>
        </div>

        {/* Répartition des Menaces par Sévérité */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-red-600/20 border border-red-600 rounded-lg p-4">
            <div className="text-2xl font-bold text-red-400 mb-1">{stats.Critique}</div>
            <div className="text-sm text-gray-300">Menaces critiques</div>
          </div>
          <div className="bg-orange-500/20 border border-orange-500 rounded-lg p-4">
            <div className="text-2xl font-bold text-orange-400 mb-1">{stats.Élevée}</div>
            <div className="text-sm text-gray-300">Menaces élevées</div>
          </div>
          <div className="bg-yellow-500/20 border border-yellow-500 rounded-lg p-4">
            <div className="text-2xl font-bold text-yellow-400 mb-1">{stats.Moyenne}</div>
            <div className="text-sm text-gray-300">Menaces moyennes</div>
          </div>
          <div className="bg-green-500/20 border border-green-500 rounded-lg p-4">
            <div className="text-2xl font-bold text-green-400 mb-1">{stats.Faible}</div>
            <div className="text-sm text-gray-300">Menaces faibles</div>
          </div>
        </div>

        {/* Principales menaces détectées */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          <h2 className="text-2xl font-bold text-white mb-6">Principales menaces détectées</h2>

          {isEmpty ? (
            <div className="text-center py-8">
              <div className="text-4xl mb-4">📋</div>
              <p className="text-gray-400 mb-4">Aucune menace détectée pour le moment</p>
              <p className="text-sm text-gray-500">Lancez une analyse pour identifier les menaces potentielles</p>
            </div>
          ) : menacesCles.length > 0 ? (
            <div className="space-y-4">
              {menacesCles.map((menace, index) => (
                <div
                  key={index}
                  className="bg-gray-700 rounded-lg p-4 border-l-4 border-blue-500 hover:bg-gray-600 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="text-2xl">{getSeverityIcon(menace.gravite)}</span>
                        <h3 className="text-lg font-bold text-white">{menace.nom}</h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getSeverityColor(menace.gravite)}`}>
                          {menace.gravite}
                        </span>
                      </div>
                      <p className="text-gray-300 text-sm mb-3">{menace.description}</p>
                      
                      {/* Afficher les recommandations si disponibles */}
                      {menace.recommandations && menace.recommandations.length > 0 && (
                        <div className="mt-3 mb-3">
                          <div className="text-xs font-semibold text-blue-400 mb-2">Recommandations principales :</div>
                          <ul className="list-disc list-inside space-y-1 text-xs text-gray-400">
                            {menace.recommandations.slice(0, 2).map((rec: string, recIndex: number) => (
                              <li key={recIndex} className="line-clamp-1">{rec}</li>
                            ))}
                            {menace.recommandations.length > 2 && (
                              <li className="text-blue-400 italic">+ {menace.recommandations.length - 2} autres recommandations...</li>
                            )}
                          </ul>
                        </div>
                      )}
                      
                      <button
                        onClick={() => navigate(`/menace/${encodeURIComponent(analysis?.project || "")}/${encodeURIComponent(menace.nom)}`)}
                        className="text-blue-400 hover:text-blue-300 text-sm font-medium"
                      >
                        Voir le rapport détaillé →
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="text-4xl mb-4">✅</div>
              <p className="text-gray-400">Aucune menace critique détectée</p>
            </div>
          )}
        </div>

        {/* Liste de toutes les analyses */}
        {analyses.length > 1 && (
          <div className="mt-8 bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-white">Autres analyses</h2>
            </div>
            <div className="space-y-2">
              {analyses
                .filter((a) => a.project !== analysis?.project)
                .map((a, index) => (
                  <div
                    key={index}
                    className="bg-gray-700 hover:bg-gray-600 rounded-lg p-4 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <Link
                        to={`/rapports/${encodeURIComponent(a.project)}`}
                        className="flex-1"
                      >
                        <div>
                          <div className="text-white font-medium">{a.project}</div>
                          <div className="text-sm text-gray-400">
                            {a.analysis?.menaces?.length || 0} menaces détectées • Score: {a.score_risque || 0}/100
                          </div>
                        </div>
                      </Link>
                      <div className="flex items-center space-x-2">
                        <div className="text-blue-400">→</div>
                        <button
                          onClick={(e) => {
                            e.preventDefault();
                            handleDeleteAnalysis(a.project);
                          }}
                          className="p-2 text-red-400 hover:text-red-300 hover:bg-red-900/20 rounded transition-colors"
                          title="Supprimer cette analyse"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Si on est sur /rapports sans projet spécifique et qu'il y a plusieurs analyses */}
        {!projectName && analyses.length > 0 && (
          <div className="mt-8 bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-white">Toutes vos analyses</h2>
              {analyses.length > 0 && (
                <button
                  onClick={() => {
                    if (window.confirm(`Êtes-vous sûr de vouloir supprimer toutes les analyses (${analyses.length}) ? Cette action est irréversible.`)) {
                      clearAnalyses();
                      navigate("/rapports");
                    }
                  }}
                  className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors text-sm font-medium"
                  title="Supprimer toutes les analyses"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  <span>Tout supprimer</span>
                </button>
              )}
            </div>
            <div className="space-y-2">
              {analyses.map((a, index) => (
                <div
                  key={index}
                  className="bg-gray-700 hover:bg-gray-600 rounded-lg p-4 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <Link
                      to={`/rapports/${encodeURIComponent(a.project)}`}
                      className="flex-1"
                    >
                      <div>
                        <div className="text-white font-medium">{a.project}</div>
                        <div className="text-sm text-gray-400">
                          {a.analysis?.menaces?.length || 0} menaces détectées • Score: {a.score_risque || 0}/100
                        </div>
                      </div>
                    </Link>
                    <div className="flex items-center space-x-2">
                      <div className="text-blue-400">→</div>
                      <button
                        onClick={(e) => {
                          e.preventDefault();
                          handleDeleteAnalysis(a.project);
                        }}
                        className="p-2 text-red-400 hover:text-red-300 hover:bg-red-900/20 rounded transition-colors"
                        title="Supprimer cette analyse"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
