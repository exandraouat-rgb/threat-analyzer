export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">À propos</h1>

        <div className="bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
          <div className="space-y-6 text-gray-300">
            <div>
              <h2 className="text-2xl font-bold text-white mb-4">THREAT AI</h2>
              <p className="leading-relaxed">
                THREAT AI est une plateforme avancée de détection et de modélisation intelligente des menaces applicatives.
                Notre solution utilise l'intelligence artificielle pour analyser votre architecture et identifier
                les vulnérabilités potentielles.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-white mb-3">Fonctionnalités</h3>
              <ul className="list-disc list-inside space-y-2">
                <li>Analyse automatique des menaces basée sur l'IA</li>
                <li>Détection des vulnérabilités selon les standards de sécurité</li>
                <li>Génération de rapports détaillés en PDF</li>
                <li>Recommandations personnalisées pour chaque menace</li>
                <li>Scoring de risque global</li>
              </ul>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-white mb-3">Technologies</h3>
              <p className="leading-relaxed">
                THREAT AI utilise des technologies de pointe incluant Claude AI, RAG (Retrieval-Augmented Generation),
                et des algorithmes de scoring de risque avancés.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
