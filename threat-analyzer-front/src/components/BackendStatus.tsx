import { useState, useEffect } from "react";
import { API_ENDPOINTS } from "../config";

interface BackendStatusProps {
  onStatusChange?: (isOnline: boolean) => void;
}

export default function BackendStatus({ onStatusChange }: BackendStatusProps) {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    let abortController: AbortController | null = null;
    
      const checkBackend = async () => {
        setIsChecking(true);
        abortController = new AbortController();
        const timeoutId = setTimeout(() => abortController?.abort(), 5000);
        
        try {
          const response = await fetch(API_ENDPOINTS.HEALTH, {
            method: "GET",
            signal: abortController.signal,
            mode: 'cors',
          });
          clearTimeout(timeoutId);
          const isOk = response.ok;
          setIsOnline(isOk);
          if (onStatusChange) {
            onStatusChange(isOk);
          }
        } catch (error) {
          clearTimeout(timeoutId);
          setIsOnline(false);
          if (onStatusChange) {
            onStatusChange(false);
          }
        } finally {
          setIsChecking(false);
        }
      };

    checkBackend();
    // Vérifier toutes les 10 secondes
    const interval = setInterval(checkBackend, 10000);
    return () => {
      clearInterval(interval);
      if (abortController) {
        abortController.abort();
      }
    };
  }, [onStatusChange]);

  if (isChecking) {
    return (
      <div className="flex items-center space-x-2 text-gray-400 text-sm">
        <span className="inline-block w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
        <span>Vérification du serveur...</span>
      </div>
    );
  }

  if (isOnline) {
    return (
      <div className="flex items-center space-x-2 text-green-400 text-sm">
        <span className="inline-block w-2 h-2 bg-green-400 rounded-full"></span>
        <span>Serveur connecté</span>
      </div>
    );
  }

  return (
    <div className="bg-yellow-900/50 border border-yellow-500 text-yellow-200 px-4 py-3 rounded-lg">
      <div className="flex items-start">
        <span className="text-xl mr-3">⚠️</span>
        <div className="flex-1">
          <h3 className="font-bold mb-2">Serveur backend non accessible</h3>
          <p className="text-sm mb-3">
            Le backend n'est pas démarré ou n'est pas accessible sur le port 8000.
          </p>
          <div className="text-sm space-y-1">
            <p className="font-semibold">Pour démarrer le backend :</p>
            <ol className="list-decimal list-inside space-y-1 ml-2">
              <li>Ouvrez un terminal dans le dossier <code className="bg-yellow-800/50 px-1 rounded">threat-analyzer-backend</code></li>
              <li>Exécutez : <code className="bg-yellow-800/50 px-1 rounded">python -m uvicorn main:app --reload --port 8000</code></li>
              <li>Ou utilisez le script PowerShell : <code className="bg-yellow-800/50 px-1 rounded">..\start-backend.ps1</code> (depuis la racine du projet)</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}
