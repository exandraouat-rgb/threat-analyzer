import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import { useAuth } from "./AuthContext";

export interface Threat {
  nom: string;
  gravite: string;
  description: string;
  recommandations?: string[];
  cwe_id?: string;
  cvss_score?: string;
  mitre_attack_id?: string;
  owasp_category?: string;
  score_confiance?: number;
  cwe_info?: {
    id: string;
    name?: string;
    url: string;
  };
  mitre_info?: {
    id: string;
    name?: string;
    description?: string;
    tactic?: string;
    url: string;
  };
  cves?: Array<{
    id: string;
    description?: string;
    cvss_score?: number;
    severity?: string;
    url: string;
  }>;
  owasp_info?: {
    id: string;
    name: string;
    url: string;
  };
  cis_controls?: Array<{
    id: string;
    name: string;
    relevance: string;
  }>;
  nist_csf?: Array<{
    id: string;
    name: string;
    relevance: string;
  }>;
}

export interface Analysis {
  project: string;
  score_risque: number;
  dashboard: {
    resume?: {
      niveau_global?: string;
      niveau_risque?: string;
    };
    statistiques?: {
      total_menaces: number;
      par_gravite: {
        Critique: number;
        Élevée: number;
        Moyenne: number;
        Faible: number;
      };
    };
    menaces_cles?: Array<{
      nom: string;
      gravite: string;
      description: string;
    }>;
  };
  analysis: {
    niveau_global?: string;
    menaces: Threat[];
  };
  error?: string;
  createdAt?: string;
}

interface AnalysisContextType {
  analyses: Analysis[];
  addAnalysis: (analysis: Analysis) => void;
  getAnalysis: (projectName: string) => Analysis | undefined;
  deleteAnalysis: (projectName: string) => void;
  clearAnalyses: () => void;
}

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined);

export function AnalysisProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [analyses, setAnalyses] = useState<Analysis[]>([]);

  // Clé de stockage basée sur l'utilisateur
  const getStorageKey = () => {
    return user ? `threat_analyzer_analyses_${user.id}` : "threat_analyzer_analyses_guest";
  };

  // Charger les analyses depuis localStorage au démarrage ou lors du changement d'utilisateur
  useEffect(() => {
    const storageKey = getStorageKey();
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      try {
        setAnalyses(JSON.parse(stored));
      } catch (e) {
        console.error("Erreur lors du chargement des analyses:", e);
        setAnalyses([]);
      }
    } else {
      setAnalyses([]);
    }
  }, [user?.id]);

  // Sauvegarder dans localStorage à chaque changement
  useEffect(() => {
    const storageKey = getStorageKey();
    localStorage.setItem(storageKey, JSON.stringify(analyses));
  }, [analyses, user?.id]);

  const addAnalysis = (analysis: Analysis) => {
    const newAnalysis = {
      ...analysis,
      createdAt: new Date().toISOString(),
    };
    setAnalyses((prev) => [newAnalysis, ...prev]);
  };

  const getAnalysis = (projectName: string) => {
    return analyses.find((a) => a.project === projectName);
  };

  const deleteAnalysis = (projectName: string) => {
    setAnalyses((prev) => prev.filter((a) => a.project !== projectName));
  };

  const clearAnalyses = () => {
    const storageKey = getStorageKey();
    setAnalyses([]);
    localStorage.removeItem(storageKey);
  };

  return (
    <AnalysisContext.Provider value={{ analyses, addAnalysis, getAnalysis, deleteAnalysis, clearAnalyses }}>
      {children}
    </AnalysisContext.Provider>
  );
}

export function useAnalysis() {
  const context = useContext(AnalysisContext);
  if (context === undefined) {
    throw new Error("useAnalysis must be used within an AnalysisProvider");
  }
  return context;
}
