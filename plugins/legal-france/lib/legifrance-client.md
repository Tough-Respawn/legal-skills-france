# Légifrance : consultation API facultative et datée

## 1. Choisir le moyen d'accès

La recherche et la lecture des pages officielles restent prioritaires :
aucun compte ni Python n'est nécessaire pour ce parcours. Chercher sur
Légifrance, ouvrir le texte et consulter ses versions dans le temps.
Un extrait de recherche ne vaut pas lecture intégrale d'un article.

Utiliser l'API seulement si l'utilisateur l'a demandée pour cette recherche
ou a déjà exprimé cette préférence dans la session. Des identifiants présents
ne suffisent pas. Ne pas demander de configurer PISTE pour une question
juridique ordinaire ; un échec du web ne déclenche pas l'API sans ce choix.

Après ce choix, exécuter le client Python ci-dessous. Si Python, les outils
d'exécution, les identifiants ou l'accès API manquent, reprendre le parcours
web et signaler brièvement la limite. Si aucune source ne permet le contrôle,
indiquer que la référence reste non vérifiée.

## 2. Configuration facultative

Python **3.9 ou ultérieur**, bibliothèque standard uniquement. Le programme
est `skills/legal-france/scripts/legal_api.py`, adjacent au skill méta.
Résoudre son chemin depuis l'emplacement réellement chargé du plugin ;
utiliser un chemin absolu si le dossier courant est celui du dossier juridique.
Les exemples suivants sont relatifs à la racine `plugins/legal-france/`.
Conserver le dossier courant de l'utilisateur pour la lecture de `.env`,
ou fournir `--env-file` avec son chemin explicite. Cette option peut être
placée avant le service, entre le service et l'opération, ou après les
arguments de l'opération ; si elle est répétée, la dernière valeur prévaut.

Le client lit `LEGIFRANCE_CLIENT_ID` et `LEGIFRANCE_CLIENT_SECRET`, ou le couple
commun `PISTE_CLIENT_ID` / `PISTE_CLIENT_SECRET` si aucun couple spécifique
n'est renseigné. Les variables d'environnement priment sur les valeurs du
fichier `.env`. Ne pas mélanger deux applications pour compléter un couple.

Le compte et l'application PISTE doivent avoir accès à l'API **Légifrance
stable en production** : un accès Judilibre ne prouve pas cet abonnement.
Ne jamais lire les secrets avec un outil qui les afficherait dans la
conversation, ni les passer dans les arguments de commande. Le client lit le
fichier comme du texte, sans exécution ni interpolation.

## 3. Consulter un article à la date utile

Établir la date pertinente avec le dossier, selon
`skills/legal-france/references/qualification.md`. Retrouver l'identifiant
dans une source, jamais le deviner. `--date` est obligatoire ; le programme
ne choisit pas aujourd'hui à la place d'une date manquante.

```text
python skills/legal-france/scripts/legal_api.py --use-api legifrance article --id LEGIARTI000006307920 --date 2021-04-15
```

Un identifiant de version (`id`) n'est pas l'identifiant commun (`cid`).
Le programme appelle `POST /consult/getArticle` avec `id`, lit son `cid`,
puis `POST /consult/getArticleByCid` avec `cid`. Si le CID est déjà établi :

```text
python skills/legal-france/scripts/legal_api.py --use-api legifrance article --cid LEGIARTI000006307920 --date 2021-04-15
```

Parmi `listArticle`, il retient une seule version dont l'intervalle satisfait
`dateDebut <= date demandée < dateFin`, en excluant les versions mort-nées.
Il conserve les métadonnées originales et le texte. Une version historiquement
pertinente peut avoir aujourd'hui l'état `MODIFIE` ou `ABROGE` : ce seul état
n'interdit pas sa sélection à une date antérieure.

Zéro version, plusieurs versions, absence de texte ou de bornes cohérentes
produisent une erreur explicite. Les dates ISO et timestamps en millisecondes
sont acceptés ; les heures autres que minuit sont laissées à vérifier pour
éviter de décaler silencieusement un jour civil. Le client ne remplace jamais
ce résultat par une version actuelle ou « la plus proche ».

## 4. Consulter un texte LEGI daté

```text
python skills/legal-france/scripts/legal_api.py --use-api legifrance text --id LEGITEXT000006075116 --date 2021-04-15
```

Appel `POST /consult/legiPart` avec `textId` et `date`. Le client contrôle
l'identité, les bornes `dateDebutVersion` / `dateFinVersion` et la présence
du contenu. Cette commande n'est pas un connecteur KALI, JORF ou jurisprudence.
La recherche d'identifiants reste possible sur le web ; aucune recherche
libre API dans tous les fonds n'est implémentée ici.

Une sélection technique par date ne détermine pas le droit applicable au
dossier : examiner encore le champ, les transitions, la survie de la loi
ancienne et les exceptions. Citer le numéro, l'identifiant de version, sa
période, le lien public effectivement identifié et la date de consultation.

## 5. Sorties et repli

JSON sur la sortie standard : `ok`, `source`, `endpoint`, `retrieved_at`,
`data` en cas de succès ; `error`, `message`, `fallback: web` en cas d'échec.
Les identifiants OAuth et jetons ne sont ni affichés ni stockés sur disque.
Les réponses HTTP d'erreur ne sont pas reproduites. Un jeton est réutilisé
dans le seul processus courant ; une réponse API 401 permet un seul
renouvellement. Aucun suivi de redirection authentifiée, aucune boucle sur
403, 429 ou 5xx. `Retry-After` numérique est signalé sans relance automatique.

| Code de sortie | Interprétation |
|---|---|
| 0 | Résultat reçu et contrôles techniques de l'opération effectués |
| 2 | Arguments invalides |
| 3 | `--use-api` absent : aucune lecture de secret ni requête réseau |
| 4 | Configuration absente ou illisible |
| 5 | Authentification ou accès à l'API refusé |
| 6 | Réseau, HTTP, réponse inexploitable ou autre échec de consultation |
| 7 | Identité, contenu ou version temporelle non établis |

Ces codes sont communs au client Judilibre. Un code 0 ne certifie pas une
conclusion juridique. Si l'API échoue, consulter les pages officielles avec
les capacités web du harnais ; le programme ne lance pas lui-même de scraper.

## 6. Sources techniques

Documentation consultée le **2026-09-11**, sans appel métier authentifié :

- [DILA : présentation de l'API stable](https://www.legifrance.gouv.fr/contenu/pied-de-page/open-data-et-api).
- [Catalogue public PISTE](https://piste.gouv.fr/api-catalog-sandbox?sort=nd) :
  définition Légifrance 2.4.2 récupérée depuis l'onglet de documentation ;
  requêtes `ArticleRequest`, `ArticleCidRequest`, `LegiConsultRequest` et
  réponses `GetArticleResponse`, `GetListArticleResponse`, `ConsultTextResponse`.
- [Client SocialGouv : hôte de production et OAuth](https://github.com/SocialGouv/dila-api-client).

La consultation du schéma et les contrôles sur données synthétiques ne
valident pas le fonctionnement réel avec des identifiants valides. Cette
validation authentifiée reste à effectuer.
