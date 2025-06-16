# 🌐 WebCloner - Outil de Clonage de Sites Web

Un outil Python simple et efficace pour cloner des sites web complets avec toutes leurs ressources (CSS, JavaScript, images).

## ✨ Fonctionnalités

- 🎨 **Clonage complet** : Pages HTML, CSS, JavaScript et images
- 🔗 **Exploration automatique** : Suit tous les liens internes
- 📁 **Organisation structurée** : Crée une structure de dossiers propre
- 🎯 **Interface interactive** : Demande l'URL et le nom du dossier
- 🌈 **Interface colorée** : Messages de progression visuels et colorés
- ⚡ **Performance optimisée** : Téléchargement efficace des ressources

## 🚀 Installation

1. **Cloner le repository :**
   ```bash
   git clone https://github.com/nathanndevvv/WebCloner.git
   cd Website-Cloner
   ```

2. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Utilisation

### Méthode Interactive (Recommandée)
```bash
python app.py
```

Le script vous demandera :
- 🌐 L'URL du site à cloner
- 📁 Le nom du dossier de destination


## 📋 Prérequis

- **Python 3.7+**
- **BeautifulSoup4** - Pour l'analyse HTML
- **Requests** - Pour les requêtes HTTP
- **Colorama** - Pour l'affichage coloré

## ⚠️ Avertissements Importants

⚠️ **Utilisation Responsable :**
- Ce outil est destiné à un usage éducatif et personnel uniquement
- Respectez les droits d'auteur et les conditions d'utilisation des sites
- N'utilisez pas pour copier du contenu protégé ou commercial
- Vérifiez la légalité de l'utilisation dans votre juridiction

⚠️ **Limitations Techniques :**
- Certains sites modernes utilisent des technologies complexes (SPA, API, etc.)
- Les sites avec authentification ne fonctionneront pas correctement
- Les sites avec protection anti-bot peuvent bloquer les téléchargements

## 📁 Structure du Projet

```
Website-Cloner/
├── app.py              # Script principal
├── requirements.txt    # Dépendances Python
├── readme.md          # Ce fichier
├── license.md         # Licence du projet
└── .gitignore         # Fichiers ignorés par Git
```

## 🔧 Personnalisation

Le script peut être facilement modifié pour :
- Ajouter de nouveaux types de ressources
- Modifier la profondeur d'exploration
- Changer les délais entre les requêtes
- Personnaliser l'affichage des messages

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📄 Licence

Ce projet est sous licence **Mozilla Public License, version 2.0**.

Voir le fichier `license.md` pour plus de détails.

## ⚡ Exemple d'Utilisation

```bash
$ python app.py
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║    ██╗    ██╗███████╗██████╗  ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗  ║
║    ██║    ██║██╔════╝██╔══██╗██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗ ║
║    ██║ █╗ ██║█████╗  ██████╔╝██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝ ║
║    ██║███╗██║██╔══╝  ██╔══██╗██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗ ║
║    ╚███╔███╔╝███████╗██████╔╝╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║ ║
║     ╚══╝╚══╝ ╚══════╝╚═════╝  ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ║
║                                                                                  ║
║                    🌐 Site Web Cloner Tool 🌐                                   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝

🌐 Entrez l'URL du site à cloner: https://example.com
📁 Entrez le nom du dossier de destination: mon_site_clone
```

## 📞 Support

Si vous rencontrez des problèmes ou avez des questions :
- Ouvrez une issue sur GitHub
- Consultez la documentation
- Vérifiez les logs d'erreur

---

**Développé avec ❤️ pour l'apprentissage et l'éducation**
