import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AnalysisProvider } from "./context/AnalysisContext";
import { AuthProvider } from "./context/AuthContext";
import Header from "./components/Header";
import Home from "./components/Home";
import NewAnalysis from "./components/NewAnalysis";
import AnalysisResults from "./components/AnalysisResults";
import ThreatDetail from "./components/ThreatDetail";
import MetricsView from "./components/MetricsView";
import AttackPathViewer from "./components/AttackPathViewer";
import About from "./components/About";
import Login from "./components/Login";
import Register from "./components/Register";
import ProtectedRoute from "./components/ProtectedRoute";
import "./App.css";

export default function ThreatAnalyzerApp() {
  return (
    <AuthProvider>
      <AnalysisProvider>
        <BrowserRouter>
          <div className="min-h-screen bg-gray-900">
            <Header />
            <Routes>
              <Route path="/connexion" element={<Login />} />
              <Route path="/inscription" element={<Register />} />
              <Route path="/" element={<Home />} />
              <Route
                path="/nouvelle-analyse"
                element={
                  <ProtectedRoute>
                    <NewAnalysis />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/rapports"
                element={
                  <ProtectedRoute>
                    <AnalysisResults />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/rapports/:projectName"
                element={
                  <ProtectedRoute>
                    <AnalysisResults />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/menace/:projectName/:threatName"
                element={
                  <ProtectedRoute>
                    <ThreatDetail />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/metriques/:projectName"
                element={
                  <ProtectedRoute>
                    <MetricsView />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/chemins-attaque/:projectName"
                element={
                  <ProtectedRoute>
                    <AttackPathViewer />
                  </ProtectedRoute>
                }
              />
              <Route path="/a-propos" element={<About />} />
            </Routes>
          </div>
        </BrowserRouter>
      </AnalysisProvider>
    </AuthProvider>
  );
}
