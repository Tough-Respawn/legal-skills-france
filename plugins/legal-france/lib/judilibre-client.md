# Judilibre : client portable facultatif

## 1. Web prioritaire, API sur demande

Pour la jurisprudence, rechercher et lire d'abord les sources officielles
sur le web. Ne pas vérifier les identifiants ni proposer une inscription
PISTE à chaque question. Utiliser Judilibre uniquement si l'utilisateur
l'a demandé pour la recherche ou a déjà choisi ce mode dans la session.
La présence de clés seule ne change pas ce choix.

Le client est `skills/legal-france/scripts/legal_api.py`, partagé avec
Légifrance et fondé sur la bibliothèque standard Python 3.9 ou ultérieure.
Il remplace les appels Bash/curl et l'extraction des secrets par sed.
Aucun outil propre à un modèle n'est nécessaire : utiliser la capacité
locale d'exécution disponible dans le harnais, si elle existe.

## 2. Configuration

Lire les modalités communes dans `lib/legifrance-client.md`, section 2.
Pour Judilibre, le couple spécifique est `JUDILIBRE_CLIENT_ID` et
`JUDILIBRE_CLIENT_SECRET`. Sans couple spécifique, le couple historique
`PISTE_CLIENT_ID` / `PISTE_CLIENT_SECRET` reste accepté. L'application doit
être abonnée à Judilibre en production. Les identifiants sont lus par le
programme depuis l'environnement ou textuellement depuis `.env`, jamais
récupérés dans la conversation ni transmis comme arguments de commande.

Résoudre le chemin du script depuis le plugin réellement chargé, sans
supposer que le dossier courant est la racine du dépôt. Les exemples sont
relatifs à `plugins/legal-france/`. Garder le dossier courant de l'utilisateur
pour `.env`, ou préciser `--env-file` avant le service, entre le service et
l'opération, ou après les arguments de l'opération.

## 3. Rechercher puis lire la décision

```text
python skills/legal-france/scripts/legal_api.py --use-api judilibre search --query "harcèlement moral employeur" --chamber soc --page 0 --page-size 10
```

Le programme obtient un jeton OAuth, puis appelle `GET /search` avec les
paramètres encodés. Il ne télécharge pas automatiquement toutes les pages.
Paramètres disponibles : `--jurisdiction`, `--chamber`, `--date-start`,
`--date-end`, `--page`, `--page-size`, `--sort` et `--order`. La première page
est 0 ; le maximum par page est 50. Le défaut est la Cour de cassation (`cc`),
avec tri `scorepub` descendant. Le champ de date d'une décision retournée
est `decision_date`, à distinguer de `update_date`.

Le schéma déclare `jurisdiction` et `chamber` comme tableaux sans
`collectionFormat` explicite. Le format par défaut de
[Swagger 2.0](https://spec.openapis.org/oas/v2.0.html#parameter-object) est CSV :
pour un élément, `jurisdiction=cc` et `chamber=soc` sont les représentations
attendues. Les exemples du client sélectionnent une valeur par filtre ;
cette conformité au schéma ne constitue pas un test du serveur de production.

Pour un pourvoi précis, rechercher son numéro puis utiliser exclusivement
un identifiant retourné par la source :

```text
python skills/legal-france/scripts/legal_api.py --use-api judilibre search --query "19-13.340"
python skills/legal-france/scripts/legal_api.py --use-api judilibre decision --id IDENTIFIANT_RETOURNE_PAR_LA_RECHERCHE
```

`GET /decision` restitue notamment le texte et ses zones. Un résultat de
recherche n'est pas une lecture de l'arrêt : ouvrir la décision avant de
présenter son raisonnement comme vérifié. Ne jamais inventer le contenu,
un identifiant, un visa ou les faits d'une décision.

## 4. Citations et périmètre

Construire la référence depuis les métadonnées effectivement reçues :
chambre, `decision_date`, numéro, ECLI si présent, puis `(Judilibre: <id>)`.
L'identifiant Judilibre complète la citation usuelle ; il ne la remplace pas.
Ne pas doubler le préfixe `ECLI:` s'il est déjà dans la valeur.

| Code de chambre | Forme française |
|---|---|
| `civ1` | Cass. civ. 1re |
| `civ2` | Cass. civ. 2e |
| `civ3` | Cass. civ. 3e |
| `soc` | Cass. soc. |
| `com` | Cass. com. |
| `crim` | Cass. crim. |
| `mixte` | Cass. ch. mixte |
| `pl` | Cass. ass. plén. |

Judilibre concerne l'ordre judiciaire ; la couverture dépend de la
juridiction et de la période. Pour le Conseil d'État, le Conseil
constitutionnel ou les juridictions européennes, consulter les sites
respectifs (CE/Légifrance, Conseil constitutionnel, CURIA/EUR-Lex/HUDOC).
Ne pas envoyer ces recherches à Judilibre ni conclure à l'absence d'une
décision à partir d'un seul résultat vide.

## 5. Échecs et repli

Les sorties et codes sont décrits dans `lib/legifrance-client.md`, section 5.
Sans `--use-api`, aucune lecture de secrets et aucun appel réseau. Si le
mode API a été choisi mais que la configuration manque, expliquer brièvement
la configuration facultative et poursuivre sur le web. Ne pas répéter
l'invitation à configurer le service dans une session restée en mode web.

Sur erreur réseau, 403, 429 ou 5xx : repli vers la recherche et la lecture
web, avec une note factuelle sur l'échec. Sur 401 d'un appel métier : un seul
renouvellement du jeton, puis repli si nécessaire. Ne pas prétendre qu'une
citation issue du web est par nature moins précise qu'une citation API.
Si aucune source n'est lisible, conserver le statut non vérifié.

## 6. Sources techniques

[Spécification publiée par la Cour de cassation](https://github.com/Cour-de-cassation/judilibre-search/blob/master/public/JUDILIBRE-public-swagger.json),
version 1.2.5 consultée le **2026-09-11** : `/search`, `/decision`, pagination,
tri et champ `decision_date`. [Présentation officielle](https://github.com/Cour-de-cassation/judilibre-search).
L'hôte de production et le flux OAuth PISTE reprennent l'intégration existante.
Le fonctionnement du client Python avec des identifiants valides reste à
vérifier ; les résultats historiques du client curl ne le valident pas.
