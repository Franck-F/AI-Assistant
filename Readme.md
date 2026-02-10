# Bac2Futur - Assistant d'Orientation Intelligent

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.30+-FF4B4B.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg)

Bac2Futur est un assistant intelligent conçu pour accompagner les étudiants et les professionnels dans leur parcours d'orientation scolaire et professionnelle. S'appuyant sur l'architecture GPT-4o, il offre une interface moderne et intuitive pour simplifier la recherche de formations et la préparation des candidatures stratégiques.

---

## Architecture et Design

![Bac2Futur Interface Mockup](bac2futur_mockup.png)
*Interface logicielle optimisée : Glassmorphism, Dark Mode et assistance interactive.*

---

## Fonctionnalités Principales

- **Orientation Stratégique** : Analyse des parcours académiques en fonction des objectifs professionnels.
- **Support à la Candidature** : Aide méthodologique pour la rédaction de lettres de motivation et projets motivés Parcoursup.
- **Analyse de Formations** : Exploration des catalogues RNCP, conditions d'admission et débouchés.
- **Veille Professionnelle** : Informations structurées sur le marché de l'emploi, les stages et l'alternance.
- **Cadre Réglementaire** : Accès aux fiches pratiques sur la législation des contrats et des stages.

---

## Équipe Projet

- **Frank-Dilane FAMBOU**
- **Luana GUALDI**
- **Claude-Christian LETEMBET-AMBILY**
- **Djouhra OULD-YOUNES**
- **Fatoumata SARR**

---

## Installation et Déploiement

1. **Clonage du Dépôt** :

   ```bash
   git clone https://github.com/Franck-F/AI-Assistant.git
   cd AI-Assistant
   ```

2. **Configuration de l'Environnement** :

   ```bash
   pip install -r requirements.txt
   ```

3. **Paramétrage API** :
   Créez un fichier `.env` à la racine :

   ```env
   OPENAI_API_KEY=votre_cle_api
   ```

4. **Lancement de l'Application** :

   ```bash
   python -m streamlit run app.py
   ```

---

## Sources de Données

- **Référentiels Formations** : Catalogues RNCP et bases de données publiques de l'enseignement supérieur.
- **Ressources Métiers** : Guides d'orientation post-bac et référentiels européens.
- **Technologie** : Interface développée sous Streamlit pour une performance et une réactivité optimales.
