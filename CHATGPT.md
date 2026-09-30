# Utiliser legal-france dans ChatGPT, sans rien installer

Ce guide est pour vous si vous utilisez ChatGPT dans votre navigateur
(chatgpt.com) et que vous n'avez jamais ouvert un terminal. Tout se fait en
quelques clics.

## 1. Télécharger le fichier

Téléchargez [legal-france-chatgpt.zip](https://github.com/Tough-Respawn/legal-skills-france/releases/latest/download/legal-france-chatgpt.zip).

**Ne le décompressez pas.** ChatGPT attend le fichier `.zip` tel quel.

## 2. Importer le plugin

1. Dans ChatGPT, ouvrez **Plugins** dans la barre latérale
   (ou allez sur [chatgpt.com/plugins](https://chatgpt.com/plugins)).
2. En haut à droite, cliquez sur **Ajouter**, puis sur
   **Importer une archive de plugin**.
3. Sélectionnez le fichier `legal-france-chatgpt.zip` téléchargé.

ChatGPT analyse le fichier avant de l'activer. Le plugin apparaît ensuite
sous **Installés**, dans la barre latérale des plugins.

Si vous ne voyez pas l'option d'import, votre formule ou votre espace de
travail ne la propose pas encore : les plugins sont déployés
progressivement selon les comptes.

## 3. Poser votre question

Ouvrez une nouvelle conversation et écrivez simplement, avec vos mots :

- « Mon propriétaire refuse de me rendre ma caution, que faire ? »
- « J'ai été licencié, à quelles indemnités ai-je droit ? »
- « Je veux contester une amende. »
- « Rédige-moi une mise en demeure. »

ChatGPT utilise le plugin de lui-même quand la question porte sur le droit
français. Pour être sûr qu'il est utilisé, tapez **@** puis choisissez
**legal-france** au début de votre message.

Activez la **recherche web** si elle vous est proposée : elle permet de
vérifier les articles de loi sur les sites officiels (legifrance.gouv.fr,
service-public.fr).

## Ce qu'il faut savoir

- **Ce n'est pas un avocat.** Les réponses sont des informations juridiques,
  pas un avis sur votre situation. Pour un litige important ou un délai
  qui approche, consultez un avocat, une maison de justice et du droit ou un
  point-justice (souvent gratuit).
- **Vérifiez les références.** Les articles et décisions cités doivent être
  confirmés sur legifrance.gouv.fr avant de vous en servir.
- **Vos données.** Ce que vous écrivez est traité par ChatGPT selon ses
  propres conditions. Évitez d'y mettre des informations dont vous n'avez pas
  besoin (numéro de sécurité sociale, coordonnées bancaires…).
- **Mise à jour.** Le plugin ne se met pas à jour tout seul. Pour connaître
  votre version, demandez : « Quelle version de legal-france est
  installée ? », puis comparez avec la
  [dernière version publiée](https://github.com/Tough-Respawn/legal-skills-france/releases/latest).
  Pour mettre à jour, téléchargez de nouveau le fichier (le lien de
  l'étape 1 donne toujours la dernière version), ouvrez la page du plugin
  dans **Plugins**, puis menu **…** > **Modifier**, et déposez le nouveau
  fichier. Désinstaller le plugin ne le supprime pas : un nouvel import de
  la même version est alors refusé (« Le plugin n'a pas pu être ajouté »).
- Les connexions directes aux bases Légifrance et Judilibre (API PISTE)
  sont réservées à l'installation technique décrite dans le
  [README](README.md).
