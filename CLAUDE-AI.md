# Utiliser legal-france dans Claude.ai, sans rien installer

Ce guide est pour vous si vous utilisez Claude dans votre navigateur
(claude.ai) ou dans l'application Claude, et que vous n'avez jamais ouvert
un terminal. Tout se fait en quelques clics. La formule gratuite suffit.

## 1. Télécharger le fichier

Téléchargez [legal-france-claude-ai.zip](https://github.com/Tough-Respawn/legal-skills-france/releases/latest/download/legal-france-claude-ai.zip).

**Ne le décompressez pas.** Claude.ai attend le fichier `.zip` tel quel.

## 2. Autoriser Claude à utiliser des compétences

Dans Claude.ai, ouvrez **Paramètres**, puis **Capacités** (*Settings >
Capabilities*). Activez l'option **Exécution de code et création de
fichiers** (*Code execution and file creation*). Sans elle, les compétences
ne fonctionnent pas.

Activez aussi la **recherche web** si elle vous est proposée : elle permet
à Claude de vérifier les articles de loi sur Légifrance.

## 3. Importer la compétence

1. Ouvrez **Personnaliser**, puis **Compétences** (*Customize > Skills*).
2. Cliquez sur **+**, puis **Créer une compétence** (*Create skill*).
3. Choisissez **Importer une compétence** (*Upload a skill*).
4. Sélectionnez le fichier `legal-france-claude-ai.zip` téléchargé.

La compétence **legal-france** apparaît dans la liste. Vérifiez qu'elle est
activée.

Les noms des menus peuvent varier légèrement selon la version de Claude.ai.
En cas de doute, suivez [l'aide officielle](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## 4. Poser votre question

Ouvrez une nouvelle conversation et écrivez simplement, avec vos mots :

- « Mon propriétaire refuse de me rendre ma caution, que faire ? »
- « J'ai été licencié, à quelles indemnités ai-je droit ? »
- « Je veux contester une amende. »
- « Rédige-moi une mise en demeure. »

Claude utilise la compétence de lui-même quand la question porte sur le
droit français. Pour être sûr qu'elle est utilisée, commencez par :
« Avec legal-france, … ».

## 5. Autoriser les sites officiels une fois pour toutes

Pour vérifier les textes, Claude consulte des sites officiels et vous demande
votre accord : « Claude souhaite récupérer une page web ». Si vous cliquez
sur **Autoriser une fois**, la question reviendra à chaque page, ce qui ralentit
beaucoup la réponse.

Cliquez plutôt sur **Toujours autoriser pour ce site web**. Les sites
consultés sont toujours les mêmes, uniquement des sites publics officiels :

- legifrance.gouv.fr (textes de loi et jurisprudence)
- service-public.fr (démarches et droits des particuliers)
- eur-lex.europa.eu (droit européen)
- conseil-constitutionnel.fr
- cnil.fr (données personnelles)

Après quelques questions, Claude ne vous demande plus rien.

## Ce qu'il faut savoir

- **Ce n'est pas un avocat.** Les réponses sont des informations juridiques,
  pas un avis sur votre situation. Pour un litige important ou un délai
  qui approche, consultez un avocat, une maison de justice et du droit ou un
  point-justice (souvent gratuit).
- **Vérifiez les références.** Claude cite les articles et décisions qu'il
  utilise ; suivez les liens vers legifrance.gouv.fr avant de vous en servir.
- **Vos données.** Ce que vous écrivez est traité par Claude.ai selon ses
  propres conditions. Évitez d'y mettre des informations dont vous n'avez pas
  besoin (numéro de sécurité sociale, coordonnées bancaires…).
- **Mise à jour.** La compétence ne se met pas à jour toute seule. Pour
  connaître votre version, demandez à Claude : « Quelle version de
  legal-france est installée ? », puis comparez avec la
  [dernière version publiée](https://github.com/Tough-Respawn/legal-skills-france/releases/latest).
  Pour mettre à jour, supprimez l'ancienne compétence dans *Compétences*,
  téléchargez de nouveau le fichier (le lien de l'étape 1 donne toujours la
  dernière version) et importez-le.
- Les connexions directes aux bases Légifrance et Judilibre (API PISTE)
  sont réservées à l'installation technique décrite dans le
  [README](README.md). Dans Claude.ai, la vérification passe par la
  recherche web.
