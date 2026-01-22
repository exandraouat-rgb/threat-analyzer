import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Contenu principal centré */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
            Détection et modélisation intelligente des menaces applicatives
          </h1>
          
          {/* Bouclier stylisé */}
          <div className="flex justify-center mb-12">
            <div className="relative">
              <div className="w-64 h-64 bg-gradient-to-br from-blue-600 to-blue-800 rounded-full flex items-center justify-center shadow-2xl">
                <div className="w-48 h-48 bg-gray-900 rounded-full flex items-center justify-center border-4 border-blue-500">
                  <svg className="w-32 h-32 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
              </div>
              {/* Effet de circuits en arrière-plan */}
              <div className="absolute inset-0 opacity-20">
                <svg className="w-full h-full" viewBox="0 0 400 400">
                  <path d="M50,50 Q200,100 350,50" stroke="currentColor" strokeWidth="2" fill="none" className="text-blue-400" />
                  <path d="M50,150 Q200,200 350,150" stroke="currentColor" strokeWidth="2" fill="none" className="text-blue-400" />
                  <path d="M50,250 Q200,300 350,250" stroke="currentColor" strokeWidth="2" fill="none" className="text-blue-400" />
                  <path d="M50,350 Q200,400 350,350" stroke="currentColor" strokeWidth="2" fill="none" className="text-blue-400" />
                </svg>
              </div>
            </div>
          </div>

          {/* Bouton principal */}
          <button
            onClick={() => navigate("/nouvelle-analyse")}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xl px-12 py-4 rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            Lancer une analyse
          </button>
        </div>

        {/* Fonctionnalités principales */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Carte 1 : Analyse intelligente */}
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-8 border border-gray-700 hover:border-blue-500 transition-all transform hover:scale-105 shadow-lg">
            <div className="w-16 h-16 bg-blue-600/20 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Analyse intelligente</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Détection automatique des vulnérabilités grâce à l'intelligence artificielle Claude
            </p>
          </div>

          {/* Carte 2 : Recommandations personnalisées */}
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-8 border border-gray-700 hover:border-green-500 transition-all transform hover:scale-105 shadow-lg">
            <div className="w-16 h-16 bg-green-600/20 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Recommandations</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Solutions concrètes et actionnables pour chaque menace identifiée
            </p>
          </div>

          {/* Carte 3 : Rapports détaillés */}
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-8 border border-gray-700 hover:border-purple-500 transition-all transform hover:scale-105 shadow-lg">
            <div className="w-16 h-16 bg-purple-600/20 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Rapports PDF</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Exportez vos analyses en PDF pour un partage et un archivage facile
            </p>
          </div>
        </div>

        {/* Section Comment ça marche */}
        <div className="mt-20 max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-white text-center mb-12">Comment ça marche ?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold text-white">
                1
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Décrivez votre projet</h3>
              <p className="text-gray-400 text-sm">
                Indiquez le type d'application et son architecture
              </p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold text-white">
                2
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Analyse automatique</h3>
              <p className="text-gray-400 text-sm">
                Notre IA analyse les menaces potentielles
              </p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold text-white">
                3
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Obtenez vos résultats</h3>
              <p className="text-gray-400 text-sm">
                Consultez les menaces détectées et les recommandations
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
