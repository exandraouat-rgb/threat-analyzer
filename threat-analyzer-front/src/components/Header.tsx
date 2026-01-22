import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useState } from "react";

export default function Header() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout, isAuthenticated } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  const isActive = (path: string) => location.pathname === path;

  const handleLogout = () => {
    logout();
    navigate("/connexion");
    setMobileMenuOpen(false);
    setUserMenuOpen(false);
  };

  const closeMenus = () => {
    setMobileMenuOpen(false);
    setUserMenuOpen(false);
  };

  return (
    <header className="bg-gray-900 border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2" onClick={closeMenus}>
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <span className="text-xl font-bold text-white hidden sm:inline">THREAT AI</span>
            <span className="text-lg font-bold text-white sm:hidden">THREAT</span>
          </Link>

          {/* Navigation Desktop */}
          {isAuthenticated ? (
            <>
              <nav className="hidden md:flex items-center space-x-1">
                <Link
                  to="/"
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    isActive("/") 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-300 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  Accueil
                </Link>
                <Link
                  to="/nouvelle-analyse"
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    isActive("/nouvelle-analyse") 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-300 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  Nouvelle analyse
                </Link>
                <Link
                  to="/rapports"
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    isActive("/rapports") 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-300 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  Rapports
                </Link>
                <Link
                  to="/a-propos"
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    isActive("/a-propos") 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-300 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  À propos
                </Link>
                
                {/* Menu utilisateur Desktop */}
                <div className="ml-4 relative">
                  <button
                    onClick={() => setUserMenuOpen(!userMenuOpen)}
                    className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center cursor-pointer hover:bg-gray-600 transition-colors"
                  >
                    <span className="text-gray-300 font-medium text-sm">
                      {user?.name.charAt(0).toUpperCase() || "U"}
                    </span>
                  </button>
                  
                  {/* Dropdown menu */}
                  {userMenuOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-xl border border-gray-700 z-50">
                      <div className="p-2">
                        <div className="px-3 py-2 text-sm text-gray-300 border-b border-gray-700">
                          <div className="font-medium text-white">{user?.name}</div>
                          <div className="text-xs text-gray-400">{user?.email}</div>
                        </div>
                        <button
                          onClick={handleLogout}
                          className="w-full text-left px-3 py-2 text-sm text-red-400 hover:bg-gray-700 rounded transition-colors"
                        >
                          Déconnexion
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </nav>

              {/* Menu Mobile */}
              <div className="md:hidden flex items-center space-x-2">
                {/* Avatar utilisateur mobile */}
                <div className="relative">
                  <button
                    onClick={() => setUserMenuOpen(!userMenuOpen)}
                    className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center cursor-pointer hover:bg-gray-600 transition-colors"
                  >
                    <span className="text-gray-300 font-medium text-sm">
                      {user?.name.charAt(0).toUpperCase() || "U"}
                    </span>
                  </button>
                  
                  {/* Dropdown menu mobile */}
                  {userMenuOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-xl border border-gray-700 z-50">
                      <div className="p-2">
                        <div className="px-3 py-2 text-sm text-gray-300 border-b border-gray-700">
                          <div className="font-medium text-white">{user?.name}</div>
                          <div className="text-xs text-gray-400">{user?.email}</div>
                        </div>
                        <button
                          onClick={handleLogout}
                          className="w-full text-left px-3 py-2 text-sm text-red-400 hover:bg-gray-700 rounded transition-colors"
                        >
                          Déconnexion
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                {/* Bouton hamburger */}
                <button
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="p-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
                  aria-label="Menu"
                >
                  {mobileMenuOpen ? (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  ) : (
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  )}
                </button>
              </div>
            </>
          ) : (
            <>
              <nav className="hidden sm:flex items-center space-x-4">
                <Link
                  to="/connexion"
                  className="px-4 py-2 text-gray-300 hover:text-white transition-colors"
                >
                  Connexion
                </Link>
                <Link
                  to="/inscription"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                >
                  Inscription
                </Link>
              </nav>

              {/* Menu Mobile non authentifié */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="sm:hidden p-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
                aria-label="Menu"
              >
                {mobileMenuOpen ? (
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                ) : (
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                )}
              </button>
            </>
          )}
        </div>

        {/* Menu mobile déroulant */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-800">
            {isAuthenticated ? (
              <nav className="px-2 pt-2 pb-3 space-y-1">
                <Link
                  to="/"
                  onClick={closeMenus}
                  className={`block px-3 py-2 rounded-lg transition-colors ${
                    isActive("/") 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-300 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  Accueil
                </Link>
                <Link
                  to="/nouvelle-analyse"
                  onClick={closeMenus}
                  className={`block px-3 py-2 rounded-lg transition-colors ${
                    isActive("/nouvelle-analyse") 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-300 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  Nouvelle analyse
                </Link>
                <Link
                  to="/rapports"
                  onClick={closeMenus}
                  className={`block px-3 py-2 rounded-lg transition-colors ${
                    isActive("/rapports") 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-300 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  Rapports
                </Link>
                <Link
                  to="/a-propos"
                  onClick={closeMenus}
                  className={`block px-3 py-2 rounded-lg transition-colors ${
                    isActive("/a-propos") 
                      ? "bg-blue-600 text-white" 
                      : "text-gray-300 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  À propos
                </Link>
              </nav>
            ) : (
              <nav className="px-2 pt-2 pb-3 space-y-1">
                <Link
                  to="/connexion"
                  onClick={closeMenus}
                  className="block px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
                >
                  Connexion
                </Link>
                <Link
                  to="/inscription"
                  onClick={closeMenus}
                  className="block px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-center"
                >
                  Inscription
                </Link>
              </nav>
            )}
          </div>
        )}
      </div>

      {/* Overlay pour fermer les menus au clic extérieur */}
      {(mobileMenuOpen || userMenuOpen) && (
        <div
          className="fixed inset-0 z-40 md:hidden"
          onClick={closeMenus}
        />
      )}
    </header>
  );
}
