# Outil de Nettoyage de Données pour les Projets QGIS Zone SUD (Inwi)

Cet outil vous aide à traiter et valider les fichiers CSV contenant des chemins de liens des photos de livrables QGIS. 

Il vérifie l’existence des fichiers liés et génère un rapport de validation.

## Prérequis

Avant de commencer, assurez-vous d’avoir installé les logiciels suivants :

- [Python](https://www.python.org/downloads/) (version la plus récente recommandée)
- [PostgreSQL](https://www.postgresql.org/download/) (version la plus récente recommandée)

## Installation

### Configuration de PostgreSQL

1. Installez PostgreSQL à partir du lien au dessus  
2. Pour un guide détaillé, consultez ce [Tutoriel d’installation de PostgreSQL](https://www.youtube.com/watch?v=4qH-7w5LZsA&list=PLQQ4jCKoK5On2OSmPjOVwQ5nyuz78B2Zp&index=56)

### Création d’un utilisateur PostgreSQL (recommandé)

Pour des raisons de sécurité, il est recommandé de créer un utilisateur dédié au lieu d’utiliser le superutilisateur :

1. Ouvrez la ligne de commande PostgreSQL (psql) en tant qu’utilisateur postgres  et entrez les commandes suivantes :
2. Créez un nouvel utilisateur : `CREATE USER votre_utilisateur WITH PASSWORD 'votre_mot_de_passe';`  
3. Créez une base de données : `CREATE DATABASE votre_base;`  
4. Attribuez les privilèges : `GRANT ALL PRIVILEGES ON DATABASE votre_base TO votre_utilisateur;`  

OU utilisez l’interface graphique PGADMIN : [create_new_user](https://www.youtube.com/watch?v=oNJpktM65eY) (guidd détaillé) 

### Installation des dépendances Python

Lancez le script d’installation pour configurer Python avec toutes les bibliothèques nécessaires :

1. Accédez au répertoire du projet  
2. Double-cliquez sur `installer.vbs`  
3. Attendez la fin de l’installation  

Le script installera les bibliothèques Python suivantes :
- psycopg2-binary (adaptateur PostgreSQL)
- python-docx (pour manipuler des documents Word)
- tkinter (interface graphique)
- Bibliothèques standard : csv, os

## Création d’un raccourci sur le bureau

Voici comment créer un raccourci vers votre script Python sous Windows :

1. **Créer un raccourci vers Python :**
   - Clic droit sur le bureau
   - Sélectionnez "Nouveau" > "Raccourci"
   - Dans le champ de localisation, tapez : `pythonw "C:\chemin\complet\vers\votre\script.py"`
   - Cliquez sur "Suivant", donnez un nom, puis cliquez sur "Terminer"
   - Clic droit sur le nouveau raccourci > "Propriétés"
   - Dans le champ "Démarrer dans", entrez le lien vers le dossier contenant le script

### Options supplémentaires :

- **Changer l’icône :**
  - Clic droit sur le raccourci > "Propriétés"
  - Cliquez sur "Changer l’icône"
  - Choisissez une icône appropriée (.ico)

## Utilisation

Avant tout, commencez par extraire les données depuis la couche QGIS. Voici un tutoriel à suivre :  
[exporter des données d'une couche en CSV dans QGIS](https://www.youtube.com/watch?v=VV378t7IkMo)

1. Double-cliquez sur le raccourci du bureau pour lancer l’application  
2. Sélectionnez votre fichier CSV contenant les chemins de fichiers  
3. L’outil va :
   - Nettoyer les données du fichier CSV
   - Vérifier l’existence de chaque fichier lié
   - Générer un rapport de validation  
4. Les données nettoyées seront enregistrées dans votre base de données PostgreSQL

## Dépannage

En cas de problème lors de l’installation ou de l’utilisation :

- Vérifiez que Python et PostgreSQL sont correctement installés  
- Vérifiez les permissions de l’utilisateur PostgreSQL  
- Assurez-vous que toutes les bibliothèques Python nécessaires sont installées  
- Vérifiez que les chemins dans votre fichier CSV sont correctement formatés

## Support

Pour toute aide supplémentaire ou pour signaler un problème, contactez : kamil02mac@gmail.com

