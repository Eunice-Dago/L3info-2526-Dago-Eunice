Dans le cadre de ce projet, j’ai développé une application web dédiée à la vente de bijoux, avec pour objectif principal d’offrir une interface moderne, dynamique et intuitive. La réalisation s’est déroulée en plusieurs étapes techniques qui ont permis de structurer correctement le site, et de rendre l’ensemble entièrement dynamique.

1) Implémentation des sessions 
Une étape essentielle du projet a été la mise en place des sessions.
Les sessions permettent de maintenir des informations côté utilisateur même si celui-ci n’est pas connecté.


2 Dynamisation du site avec les données du backend
Après avoir mis en place les bases, j’ai rendu le site entièrement dynamique :
Produits dynamiques
Les bijoux affichés sur le site ne sont pas écrits en dur dans le HTML.
Ils proviennent directement de la base de données.
J’ai créé des modèles pour représenter :
les catégories
les produits (nom, description, prix, stock, images)
les commantaires
Ensuite, dans les vues, j’ai récupéré ces informations et je les ai envoyées au template.
Cela permet d’ajouter facilement de nouveaux bijoux sans modifier le code HTML.
