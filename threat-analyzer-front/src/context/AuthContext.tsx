import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import { API_ENDPOINTS } from "../config";

export interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (email: string, password: string, name: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // Charger l'utilisateur depuis localStorage au démarrage
  useEffect(() => {
    const storedUser = localStorage.getItem("threat_analyzer_user");
    if (storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        setUser(userData);
        // Optionnel : vérifier que l'utilisateur existe toujours dans la BD
        // fetch(`${API_ENDPOINTS.GET_USER}/${userData.id}`)
        //   .then(res => res.json())
        //   .then(data => {
        //     if (data.success) {
        //       setUser(data.user);
        //     } else {
        //       localStorage.removeItem("threat_analyzer_user");
        //     }
        //   });
      } catch (e) {
        console.error("Erreur lors du chargement de l'utilisateur:", e);
        localStorage.removeItem("threat_analyzer_user");
      }
    }
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const formData = new FormData();
      formData.append("email", email);
      formData.append("password", password);

      const response = await fetch(API_ENDPOINTS.LOGIN, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.success && data.user) {
        setUser(data.user);
        localStorage.setItem("threat_analyzer_user", JSON.stringify(data.user));
        return true;
      }

      return false;
    } catch (error) {
      console.error("Erreur lors de la connexion:", error);
      return false;
    }
  };

  const register = async (email: string, password: string, name: string): Promise<boolean> => {
    try {
      const formData = new FormData();
      formData.append("email", email);
      formData.append("password", password);
      formData.append("name", name);

      const response = await fetch(API_ENDPOINTS.REGISTER, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.success && data.user) {
        setUser(data.user);
        localStorage.setItem("threat_analyzer_user", JSON.stringify(data.user));
        return true;
      }

      return false;
    } catch (error) {
      console.error("Erreur lors de l'inscription:", error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("threat_analyzer_user");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
