# Installation des dépendances Tailwind CSS

## Étape 1: Aller dans le dossier frontend
```bash
cd threat-analyzer-front
```

## Étape 2: Installer les nouvelles dépendances
```bash
npm install
```

Cette commande installera:
- `tailwindcss` - Framework CSS utilitaire
- `postcss` - Préprocesseur CSS
- `autoprefixer` - Ajoute les préfixes navigateurs
- `@tailwindcss/forms` - Plugin pour de beaux formulaires

## Étape 3: Vérifier que tout est correct
Vous devriez voir ces fichiers créés:
- `tailwind.config.js` - Configuration Tailwind
- `postcss.config.js` - Configuration PostCSS

## Étape 4: Démarrer le serveur
```bash
npm run dev
```

Le site devrait maintenant afficher avec un design magnifique! 🎨

## Troubleshooting

### Les styles ne s'appliquent pas
- Assurez-vous que le dossier `node_modules` existe
- Essayez `npm install` à nouveau
- Redémarrez le serveur de développement avec `npm run dev`

### Erreur "tailwindcss not found"
- Vérifiez que `package.json` contient les dépendances
- Supprimez `node_modules` et `package-lock.json`
- Lancez `npm install` à nouveau
