# legal-anonymiser

Pseudonymisation locale de contrats, sans réseau. L'outil lit un contrat (DOCX, PDF, numérisation),
écrit une version masquée en texte, une table de correspondance et un rapport d'inspection technique,
le tout sur votre poste. Seul le fichier masqué, relu et validé par vous, est destiné à un modèle.

## Ce que l'outil promet, et ce qu'il ne promet pas

Les identifiants directs et indirects sont masqués : noms et prénoms (composés, initiales, noms
d'usage), raisons sociales et noms commerciaux, adresses postales, e-mails, téléphones, IBAN et BIC,
SIREN, SIRET, TVA, RCS, numéro de sécurité sociale, pièces d'identité, dates et lieux de naissance,
immatriculations, URL propres aux parties, en-têtes et pieds de page, blocs de signature, numéros de
contrat, de dossier ou de client, capital social, lieux-dits et bâtiments, et la commune (masquée par
défaut, à garder sur décision explicite).

Restent visibles parce que l'analyse juridique en dépend : dates (hors dates de naissance), durées,
montants, pourcentages, forme sociale (SAS, SARL), intitulé du poste, convention collective, effectif,
qualité de consommateur ou de professionnel. C'est un **risque résiduel**, compté dans le rapport et dans
le fichier masqué sous « Risque résiduel » ; vous pouvez le réduire en masquant ces éléments vous-même
(`masquer: texte` dans le fichier d'ajustements).

Le masquage est automatique et **peut manquer un élément**. Une seconde passe relit le texte masqué et
signale ce qui ressemble encore à un identifiant, puis vous relisez le texte avant publication. Rien ici
ne promet une anonymisation complète : on parle de pseudonymisation, la table de correspondance existe
sur votre disque et ne quitte jamais le coffre.

## Avant un envoi à Claude.ai ou ChatGPT

Dans Claude.ai ou ChatGPT, les skills ne peuvent pas lancer cet outil : il s'exécute **en amont, sur
votre machine**. Traitez le contrat ici, relisez le fichier masqué, publiez-le, puis transmettez
uniquement `contrat-<id>.masque.md` à votre assistant. Ne transmettez jamais l'original, le coffre ni le
rapport local. Le rapport que renvoie l'assistant se réidentifie ensuite localement (`reidentifier`).

## Installation

Python 3.9 ou plus récent. L'outil tourne hors ligne ; seuls l'installation et le téléchargement du
modèle demandent le réseau, une fois.

```bash
python -m venv .venv
.venv\Scripts\activate                      # Windows ; sous Linux et macOS : source .venv/bin/activate
pip install ./tools/legal-anonymiser        # pypdf, Pillow et spaCy sont installés avec
pip install https://github.com/explosion/spacy-models/releases/download/fr_core_news_lg-3.8.0/fr_core_news_lg-3.8.0-py3-none-any.whl
legal-anonymiser --help
```

Le modèle de reconnaissance des noms (`fr_core_news_lg`, environ 550 Mo) est chargé localement à chaque
passage et n'est jamais téléchargé à l'exécution. Sans lui, le passage continue sans reconnaissance des
noms, la console affiche « Modèle de reconnaissance des noms absent : détection réduite, relisez avec
attention. » et le rapport porte le constat `ner_absente` : à éviter sur un vrai contrat.

Les numérisations (PDF image, JPG, PNG) demandent **Tesseract** avec la langue française :

- Windows : installateur de l'UB Mannheim (binaire attendu dans `C:\Program Files\Tesseract-OCR\`,
  sinon variable `TESSERACT_CMD` vers `tesseract.exe`). Si `fra.traineddata` n'a pas pu être écrit dans
  `C:\Program Files\Tesseract-OCR\tessdata` (droits), placez-le dans un dossier à vous et définissez
  `TESSDATA_PREFIX` vers ce dossier, par exemple `C:\Users\<nom>\AppData\Local\tessdata`.
- Debian et Ubuntu : `apt install tesseract-ocr tesseract-ocr-fra`.
- macOS : `brew install tesseract tesseract-lang`.

Sans Tesseract ou sans la langue `fra`, une numérisation est refusée avec le message d'installation
(code 6) ; les DOCX et PDF avec couche texte ne demandent rien d'autre que Python.

## Utilisation

`legal-anonymiser <commande>` (ou `python -m legal_anonymiser <commande>`). Le coffre est
`~/.legal-france/coffre/` (variable `LEGAL_FRANCE_COFFRE` pour le déplacer). La garde réseau
(`nonet.install()`) est la première instruction de `main`, avant tout import de pypdf, Pillow ou spaCy.

Parcours complet :

1. `legal-anonymiser traiter` dans un terminal ouvert **dans le dossier où le fichier masqué doit être
   publié** (le projet d'analyse). Sans chemin, un sélecteur de fichier s'ouvre : le chemin de l'original
   n'apparaît alors ni dans la commande ni dans la console. Gardez l'original hors de ce dossier.
2. S'il reste des points à arbitrer (code 3), ouvrez `coffre/<id>/ajustements.txt`, tranchez chaque
   ligne `?`, puis `legal-anonymiser relancer <id>`. Répétez jusqu'à « 0 alerte(s), 0 ambiguïté(s) ».
3. L'outil ouvre alors `masque.md` et `rapport.md` depuis le coffre et pose la question dans une fenêtre :
   relisez le texte masqué, puis cliquez **Publier** (ou Ajuster, ou Abandonner). `legal-anonymiser
   valider <id>` repose la question plus tard. Aucun script, variable ni option ne répond à votre place.
4. Le fichier `contrat-<id>.masque.md` est écrit dans le dossier courant et son empreinte inscrite au
   registre. `legal-anonymiser verifier contrat-<id>.masque.md` répond `publie` tant qu'il n'a pas été
   modifié, `modifie` sinon, `inconnu` pour un fichier étranger.
5. Après l'analyse par le modèle, `legal-anonymiser reidentifier <id> rapport.md` écrit le rapport avec
   les valeurs réelles dans `coffre/<id>/rapport-final.md` et l'ouvre : il ne quitte pas le coffre. La
   **première ligne du rapport doit être la copie exacte de celle du fichier publié** (marqueur
   `<!-- legal-france:masque v1 id=… statut=valide_humain date=… corps=… -->`) : elle désigne la table de
   correspondance figée à cette publication. Sans elle, ou pour une version jamais publiée, rien n'est
   réidentifié (code 7).

| Commande | Effet | Codes |
|---|---|---|
| `traiter [CHEMIN]` | sans chemin : sélecteur de fichier natif (DOCX, PDF, JPG, PNG) ; masquage complet ; sans rien en attente, passe à la validation | 0 publié, 3 arbitrage en attente, 4 non publié, 5 fichier introuvable, illisible ou format inconnu, 6 dépendance manquante |
| `relancer ID` | relit `ajustements.txt`, relance le masquage, puis comme `traiter` | idem (4 si l'identifiant est invalide ou inconnu) |
| `valider ID` | relecture et publication seules, si le dernier passage n'a rien laissé en attente | 0, 3, 4 |
| `verifier FICHIER` | affiche `publie`, `modifie` ou `inconnu` | 0 si `publie`, 1 sinon |
| `reidentifier ID RAPPORT` | rapport final avec les valeurs réelles, écrit dans le coffre et ouvert localement | 0, 7 (réidentification impossible : identifiant inconnu, aucune publication ne correspond à la première ligne du rapport, rapport illisible ; sans trace écrite) |
| `install-hook [--settings CHEMIN]` | ajoute le verrou Claude Code aux réglages (défaut `~/.claude/settings.json`), voir « Verrou Claude Code » | 0 (installé, ou déjà à jour), 6 (Claude Code absent ou antérieur à 2.1.295), 7 (réglages non JSON, rien écrit) |
| `uninstall-hook [--settings CHEMIN]` | retire exactement cette entrée | 0 (retiré, ou rien à retirer), 7 |

Code 1 : `verifier` négatif. Code 2 : arguments invalides. Code 7 : erreur interne, ou fichier du coffre corrompu (`registre.json`, `etat.json`,
`ajustements.txt` mal formé : la console ne donne que le numéro de ligne et le chemin neutre, jamais un
fragment de la ligne). La trace complète d'une erreur imprévue va dans `coffre/<id>/erreur.txt`
(ou `coffre/erreurs/<horodatage>.txt` quand aucun contrat n'est en cours) ; la console ne reçoit que le
message générique et le chemin neutre de la trace. Code 4 aussi sur Ctrl+C (« Interrompu »). Un original
illisible (droits, verrou) donne le code 5 ; une extension inconnue est refusée avant tout enregistrement
au coffre.

## Fichier d'ajustements

`coffre/<id>/ajustements.txt`, UTF-8, une décision par ligne, réécrit à chaque passage en conservant vos
décisions. Exemple après un premier passage :

```
# legal-france ajustements v1, contrat c7f3a2
# Alertes : remplacer ? par masquer ou garder.
# Une alerte valeur_connue ne peut pas être gardée : utilisez masquer.
A1 ? « Résidence Les Hauts » | paragraphe 11 | 1 | majuscule
A2 ? « kerbrat » | paragraphe 19 | 1 | valeur_connue
# Mentions ambiguës : remplacer ? par un des placeholders proposés, ou nouveau.
M1 ? « M. Kerbrat » | paragraphe 19 | 1 | [LOCATAIRE_1] [LOCATAIRE_2]
# Communes, masquées par défaut : garder si la commune est utile à l'analyse.
C1 masquer « Orange »
# Ajouts libres :
masquer: Résidence Les Hauts
demasquer: [SOCIETE_2]
```

- `A<n>` : alerte de la seconde passe (motif en fin de ligne : `majuscule`, `chiffres`, `arobase`, `url`,
  `date_naissance`, `initiales`, `valeur_connue`). `masquer` masque ce texte partout ; `garder` exempte cette seule
  occurrence (clé `localisation | rang`), jamais une alerte `valeur_connue`, qui repasse à `?`.
- `M<n>` : mention qui peut désigner plusieurs entités (homonymes, époux, « Orange » commune ou société).
  Répondre par un des placeholders proposés, ou `nouveau` pour une entité distincte. Un placeholder
  inexistant reste en attente.
- `C<n>` : commune, `masquer` par défaut, `garder` si elle est utile à l'analyse (zone tendue, encadrement
  des loyers) ; une commune gardée collée à une civilité reste signalée.
- Lignes libres : `masquer: texte exact` masque un texte partout (réduit le risque résiduel : un montant,
  une date), `demasquer: [PLACEHOLDER]` rend une entité visible. `demasquer` contourne la règle
  `valeur_connue` : c'est votre décision, elle est visible dans le fichier.
- Une ligne qui commence par `#` est un commentaire. Une ligne mal formée bloque le passage (code 7, seul
  le numéro de ligne est affiché). Les décisions dont le texte a disparu sont listées sous « Décisions
  périmées ».
- Modifier `ajustements.txt` ou `masque.md` après le dernier passage invalide la validation : `valider`
  refuse (code 3) tant que `relancer` n'a pas été relancé, y compris quand la modification a lieu
  pendant la fenêtre de confirmation (rien n'est publié).

## Limites

- **Détection** : un nom en minuscules inconnu du modèle, un mot capitalisé seul en tête de phrase
  (« Fabre signera ») ou un code postal seul ne sont pas signalés par la seconde passe. Des initiales
  seules (« ED / JK / MK » en pied de page, « J.K. ») sont signalées (`initiales`), jamais masquées
  d'office : un sigle hors vocabulaire (« CDD », « RIB ») l'est aussi, à `garder`. Un contrat tout en
  capitales produit beaucoup d'alertes `majuscule`. Un nom ou un terme défini coupé par un saut de
  ligne dans un PDF ou une numérisation peut n'être masqué qu'en partie (le reste est alors signalé
  par la seconde passe). Une alerte portant sur un fragment de mot
  (« FR » dans « FR38 ») ne se masque pas par `masquer` sur sa ligne : écrire le mot entier en ligne
  libre (`masquer: FR38`). La relecture humaine reste la dernière couche.
- **Écarts assumés par rapport à la conception** (v1) : 1. sous Windows, les droits du coffre ne sont
  pas vérifiés (pas de lecture d'ACL en bibliothèque standard, `icacls` serait un sous-processus) :
  l'isolation repose sur le profil utilisateur ; 2. pas de table « zone tendue » : chaque commune est
  masquée par défaut et proposée à l'arbitrage ; 3. texte hors page détecté pour le PDF seulement ;
  4. « écart entre texte visible et texte extrait » couvert par les constats de texte caché (blanc,
  minuscule, masqué, rendu invisible, sous image), sans comparaison par rendu graphique.
- **Réseau** : le filet dans le processus (`nonet`) coupe les sockets Python ; il ne couvre ni le code
  natif des dépendances ni le binaire OCR. Ce n'est pas une garantie, c'est une réduction du risque,
  vérifiée en test par une trace système (`strace`) et non par construction. Voir l'isolement
  optionnel ci-dessous.
- **Validation** : un programme qui simule clavier ou souris sur votre session, ou un pseudo-terminal
  piloté par un autre programme, n'est pas détecté ; l'outil ne peut pas distinguer un clic humain d'un
  clic injecté. Un `tkinter` masqué par `PYTHONPATH` fait retomber sur le terminal interactif, jamais
  sur une publication automatique.
- **Formats** : PDF chiffré refusé ; annotations autres que `/Text` et `/FreeText` non extraites ;
  JavaScript cherché dans le catalogue et les liens, pas dans les actions de pages ni de champs ;
  rectangles couvrants et transparence ignorés. Détail dans « Formats lus ».
- **Plateformes** : Windows et Linux exercés ; macOS non documenté en v1 (installation Tesseract via
  Homebrew indiquée, isolement réseau système non identifié).

## Isolement réseau au niveau du système (optionnel)

Pour une garantie qui couvre aussi les processus enfants (OCR) et le code natif :

- **Linux** : `unshare -rn legal-anonymiser traiter <fichier>` lance l'outil dans un espace réseau vide
  (seule l'interface de bouclage existe, inactive). Vérifié le 2026-10-19 dans un conteneur
  `python:3.12-slim` : même code de sortie et même `masque.md` qu'en passage normal.
- **Windows** : règle de pare-feu sortante bloquant l'interpréteur Python du venv et `tesseract.exe`
  (droits administrateur), par exemple
  `netsh advfirewall firewall add rule name="legal-anonymiser" dir=out action=block program="<venv>\Scripts\python.exe"`
  et la même règle pour `C:\Program Files\Tesseract-OCR\tesseract.exe`. Non exécuté sur ce poste
  (droits administrateur non demandés) : à vérifier par qui l'applique.
- **macOS** : non documenté en v1.

## Verrou Claude Code

Protection supplémentaire, propre à Claude Code : un hook `PreToolUse` (`legal_anonymiser/verrou.py`,
bibliothèque standard, `python -P -m legal_anonymiser.verrou --coffre <racine>`) reçoit chaque appel
d'outil en JSON sur l'entrée standard. Pour refuser, il écrit sur la sortie standard la décision JSON
`{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
"permissionDecisionReason": "<message>"}}` et sort avec le code 0 ; pour laisser passer, il ne
répond rien (code 0). Il ne lit jamais le contenu d'un fichier : il compare des chemins résolus
(liens, jonctions, noms courts 8.3 via `GetLongPathNameW`, casse indifférente sous Windows et macOS).

Ce qu'il refuse, pour le coffre et pour chaque original inscrit au registre :

- `Read`, `Edit`, `Write`, `NotebookEdit` sur un original ou sur tout chemin sous le coffre
  (`file_path` ou `notebook_path`, relatif au `cwd` de la session s'il n'est pas absolu) ;
- `Grep` et `Glob` dont la racine (`path`, sinon le dossier courant ; pour `Glob`, aussi la partie
  littérale du motif jusqu'au dernier séparateur avant le premier `*`, `?`, `[` ou `{`) est le
  coffre ou est dedans (« coffre protégé »), ou est un parent du coffre ou d'un original : une
  recherche lancée depuis le dossier personnel ou la racine du disque, ou un motif comme
  `~/Doc*/**/*.docx`, est refusée avec la raison (« un original protégé ou le coffre se trouve dans
  ce dossier ou en dessous : lancez la recherche dans un sous-dossier qui ne les contient pas ») ;
- `Bash` et `PowerShell` dont la commande contient, casse et séparateurs `\` ou `/` indifférents,
  le chemin du coffre (absolu, `/c/Users/…` de Git Bash, `~/.legal-france`, `%USERPROFILE%`,
  `$HOME`, `$env:USERPROFILE`, ou simplement `.legal-france` ; pour un coffre déplacé sous le dossier
  personnel, ses formes `~/…`, `$HOME/…`, `%USERPROFILE%\…`, `$env:USERPROFILE\…` ; et toujours
  `$LEGAL_FRANCE_COFFRE`, `%LEGAL_FRANCE_COFFRE%`, `$env:LEGAL_FRANCE_COFFRE`), le chemin d'un
  original ou son nom de fichier ; les chemins absolus Windows présents dans la commande sont
  résolus avant comparaison (jonction, nom court). Chaque jeton de la commande (mots séparés par
  blancs, guillemets et `;|&<>()=,`, plus le contenu entier de chaque chaîne entre guillemets ; un
  jeton à joker réduit à sa partie littérale, comme pour `Glob`) est aussi résolu depuis le dossier de
  la session (`cwd` de l'événement) : refusé s'il est sous le coffre (`cat coffre/registre.json` ou
  `Get-Content coffre/*/correspondance.json` depuis le parent du coffre, `cd coffre; type
  registre.json`) ou s'il est un original. Une commande lancée depuis un dossier du coffre est refusée
  entière. Une commande de 5 000 jetons est jugée en moins d'une seconde (mesuré le 2026-10-20 sous
  Windows), loin du délai de 10 s.

Avant toute comparaison, chaque chemin donné à un outil est mis sous la forme que Claude Code
(2.1.303) ouvrira lui-même après le hook : espaces et BOM retirés aux extrémités, `~` et `~/` seuls
développés (`~\…` ou `~nom/…` restent relatifs au dossier de la session, comme dans Claude Code), sous
Windows `/c/…` (Git Bash) converti en `C:\…`, sinon chemin relatif au dossier de la session. Les
préfixes `\\?\` et `\\.\` sont retirés (`\\?\UNC\serveur` devient `\\serveur`) : ils désignent le
même fichier.
L'entrée standard est lue en octets et décodée en UTF-8, quelle que soit la page de code du poste
(Claude Code ne fixe pas `PYTHONIOENCODING` pour les hooks) : un chemin accentué est comparé tel quel.

Le verrou se protège aussi lui-même. Refusés avec « verrou protégé, modification refusée » :

- `Edit`, `Write`, `NotebookEdit` sur un fichier du paquet `legal_anonymiser` installé (pour une
  installation éditable, le dossier du dépôt), sur tout fichier des dossiers de l'interpréteur qui
  lance le verrou (`sys.prefix`, `sys.base_prefix`, `sys.exec_prefix`, site-packages de
  l'utilisateur : venv, bibliothèque standard, `.pth`, chercheur de l'installation éditable, tout ce
  que Python charge au démarrage), et sur tout `settings*.json` d'un dossier `.claude`
  (`~/.claude/settings.json`, `~/.claude/settings.local.json`, `.claude/settings.json` d'un projet) ;
  `Read` reste permis ;
- `Bash` et `PowerShell` dont la commande contient `uninstall-hook`, `legal_anonymiser.verrou`,
  `legal_anonymiser/`, `.claude/settings`, `sitecustomize`, `usercustomize`, `site-packages` ou le
  chemin absolu du paquet, ou dont un jeton, résolu depuis le dossier de la session, désigne un fichier
  du paquet ou un `settings*.json` d'un dossier `.claude` (`echo {} > settings.json` lancé dans
  `.claude`). `python -m legal_anonymiser traiter`, `legal-anonymiser verifier` et le Python du venv
  lancé par son chemin restent permis.

Conséquences : `uninstall-hook` se lance par l'utilisateur, dans son propre terminal, jamais par le
modèle ; les réglages de Claude Code ne se modifient plus depuis une session (le faire à la main, ou
retirer le verrou le temps du changement) ; développer l'outil lui-même avec Claude Code demande de
retirer le verrou d'abord. Sur un poste de développement, préférer une installation limitée au
dossier des contrats (`legal-anonymiser install-hook --settings <dossier des contrats>/.claude/settings.json`),
ou retirer le verrou pendant le travail sur l'outil : les sessions ouvertes hors de ce dossier ne sont
alors pas protégées.

Les messages ne contiennent jamais un chemin ni un nom de fichier. Sur un refus, le modèle voit
seulement `PreToolUse:Read hook error: legal-france : original protégé, accès refusé...`
(Claude Code 2.1.303, constaté le 2026-10-20). Pourquoi le JSON plutôt que le code 2 : sur un refus
par code 2, Claude Code préfixe le message de la ligne de commande du hook, donc du chemin absolu de
l'interpréteur et du coffre.

Toute exception interne (JSON invalide sur l'entrée, registre corrompu, argument manquant) vaut
refus par la même décision JSON, avec la raison générique « verrou en erreur, accès refusé par
précaution ». Dernier recours, si la décision elle-même ne peut pas être écrite (sortie standard
inutilisable) : code 2 et le même message sur l'erreur standard ; dans ce cas seulement, le modèle
voit la ligne de commande du hook. Le hook est
déclaré avec `"onFailure": "block"` (délai 10 s) : un hook qui ne démarre pas, plante, dépasse son
délai ou répond un JSON illisible bloque aussi l'appel au lieu de le laisser passer, ce qui exige
Claude Code 2.1.295 ou plus. Les hooks des fichiers de réglages s'appliquent aussi aux appels
d'outils des sous-agents. Format du hook, décision `deny`, code 2 et `onFailure` confirmés sur
https://code.claude.com/docs/en/hooks, lue le 2026-10-20.

### Installation du verrou

```bash
legal-anonymiser install-hook                 # écrit dans ~/.claude/settings.json
legal-anonymiser install-hook --settings CHEMIN
legal-anonymiser uninstall-hook               # retire exactement cette entrée
```

- Lancer `install-hook` avec l'interpréteur de l'environnement où l'outil est installé : l'entrée
  enregistre son chemin absolu (`sys.executable`) et la racine résolue du coffre (variable
  `LEGAL_FRANCE_COFFRE` comprise). Après un déplacement du coffre ou du venv, ou un changement de
  version de Python, relancer `install-hook` : l'entrée est remplacée (arguments compris), jamais
  doublée.
- L'entrée ajoutée sous `hooks.PreToolUse` : matcher
  `Read|Edit|Write|NotebookEdit|Grep|Glob|Bash|PowerShell`, hook `{"type": "command", "command":
  <python>, "args": ["-P", "-m", "legal_anonymiser.verrou", "--coffre", <racine>], "onFailure":
  "block", "timeout": 10}` (forme exec, sans shell). Elle est reconnue par `legal_anonymiser.verrou`
  dans `args`.
- `-P` (Python 3.11 ou plus) empêche le dossier de la session d'entrer dans le chemin d'import : un
  `json.py`, un `argparse.py` ou un dossier `legal_anonymiser/` présent dans le projet ne remplace pas
  le verrou (vérifié en test : sans `-P`, un tel fichier fait sortir le hook en code 0, donc laisser
  passer). En Python 3.9 et 3.10, `-P` n'existe pas et n'est pas écrit : un module du projet nommé
  comme un module de la bibliothèque standard, ou comme le paquet, peut détourner le verrou. Utiliser
  Python 3.11 ou plus pour l'environnement de l'outil.
- `install-hook` écrit toujours un JSON valide.
- Refus d'installer, sans rien écrire : `claude --version` introuvable ou antérieur à 2.1.295 (code 6) ;
  réglages qui ne sont pas un objet JSON valide, commentaires compris (code 7).
- Avant chaque écriture, l'ancien fichier est copié en `settings.json.legal-france.bak` à côté ;
  l'écriture est atomique (fichier temporaire puis remplacement). Le fichier est rechargé et réécrit
  en JSON indenté de 2 : les autres clés et les autres hooks sont conservés, la mise en forme
  d'origine ne l'est pas. Relancer sans rien à changer n'écrit rien. Un BOM UTF-8 en tête est
  accepté. Si `settings.json` est un lien symbolique, c'est sa cible qui est réécrite (et sauvegardée
  à côté d'elle), le lien reste en place.
- `uninstall-hook` retire seulement l'objet hook du verrou ; un hook à vous placé dans la même entrée
  est conservé, l'entrée n'est supprimée que si elle devient vide.
- Redémarrer les sessions Claude Code ouvertes après l'installation.

**Limites** (conception, section 8) :

- un script lancé par `Bash` ou `PowerShell` (Python, `node`, PowerShell) qui lit l'original sans
  citer son chemin ni son nom, un motif générique (`cat *.docx`, `Get-ChildItem -Recurse`), un chemin
  reconstitué par des variables ou une concaténation (`d=.legal-fr; cat ~/${d}ance/...`) ne sont pas
  reconnus ;
- les outils MCP, les autres harnais et toute session sans le hook ne sont pas couverts ;
- un fichier de réglages (`--settings` ou `settings.json`) qui n'est pas du JSON valide est ignoré
  par Claude Code sans avertissement : le verrou disparaît avec lui. Constaté avec `--settings` le
  2026-10-20 (appel `Read` passé, rien sur la sortie d'erreur) ; pour `~/.claude/settings.json`, non
  vérifié, à supposer identique. Après toute modification manuelle des réglages, vérifier qu'ils
  restent du JSON valide ;
- `Read` refuse déjà de lui-même un `.docx` (fichier binaire) et suggère au modèle un script : c'est
  précisément le contournement que le verrou ne voit pas ;
- l'auto-protection repose sur des chemins et des mots dans les commandes : un script qui écrit dans
  les réglages ou dans le paquet sans les nommer n'est pas vu (même limite que ci-dessus) ; pour
  `Bash` et `PowerShell`, les dossiers de l'interpréteur ne sont reconnus que par `site-packages`,
  `sitecustomize` ou `usercustomize`, pas par leur chemin absolu (sinon lancer le Python du venv par
  son chemin serait refusé) ;
- le dépassement du délai de 10 s n'a pas été provoqué en session réelle : le blocage dans ce cas
  vient de la documentation de Claude Code, pas d'une observation ;
- un contrat jamais passé dans l'outil n'est pas inscrit au registre, donc pas protégé : la garde
  d'entrée du skill (`verifier`) s'en charge.

Les protections principales restent : le modèle ne connaît pas le chemin de l'original, rien de non
publié n'existe hors du coffre, l'utilisateur ne transmet que le fichier publié.

## État de la validation (2026-10-20)

Vérifié par exécution : suite de tests locale complète (OCR et modèle réels) ; corpus synthétique de 26
contrats fictifs (bail, travail, consommation, entre professionnels, en DOCX, PDF texte et numérisation,
plus un fichier piégé par constat technique) traité par la ligne de commande avec arbitrage scripté
(mesure du 2026-10-20) : 0 fuite des noms, initiales, adresses, numéros, e-mails, IBAN, SIREN et dates
de naissance lisibles après arbitrage, 175 noms sur 176 détectés avant arbitrage, 30 constats techniques
sur 30 présents dans le rapport, 1,0 alerte pour 100 mots, 0 fusion de deux parties sous un placeholder,
0 partie éclatée sur plusieurs placeholders ; 20 placeholders de nom qui débordent sur du texte courant
(« Logement sans l'accord » pris pour une société par le modèle, 17 fois ; un titre de contrat pris pour
une personne, 2 fois ; « TVA intracommunautaire », 1 fois : masqués à tort, pas une fuite). Trace
système `strace` dans un conteneur Linux : aucune connexion, `unshare -rn` identique.

Parcours réel sur un poste Windows, vérifié le 2026-10-19 à 23:28 : `traiter` (code 3), arbitrage,
`relancer`, fenêtre de validation, clic humain « Publier » (code 0), `verifier` = `publie`, aucun nom de
partie dans le fichier publié.

Verrou Claude Code en session réelle, vérifié le 2026-10-20 entre 08:01 et 08:07 UTC (Claude Code
2.1.303, `claude -p --settings` avec l'entrée écrite par `install-hook`, coffre et originaux factices
temporaires) : refus constatés dans le transcript pour `Read` d'un original PDF, `cat` et `Get-Content`
du registre, `Grep` depuis le dossier personnel, `Read` par un sous-agent, registre corrompu (message
générique) et interpréteur introuvable (`onFailure: "block"`). Après passage à la décision JSON et à
`-P` (08:14 UTC), puis du dernier recours à la décision JSON (08:19 UTC), tous les cas rejoués
sauf l'interpréteur introuvable : `Read` de l'original, `Grep` depuis le dossier personnel, `cat` et
`Get-Content` du registre, `Read` par un sous-agent et registre corrompu sont refusés, et le texte vu
par le modèle ne contient ni chemin ni ligne de commande. Après la normalisation des chemins et
l'auto-protection (08:44 à 08:48 UTC, coffre temporaire sous le dossier personnel) : `Grep` sur
`~/.legal-france-test/coffre`, `Read` d'un original accentué, deux `Glob` absolus à joker (`pro*`,
`{projet,x}`), `Edit` et `Write` de l'original, `Write` dans le coffre par `~`, `Write` de
`.claude/settings.local.json`, `Edit` de `verrou.py`, `NotebookEdit` d'un notebook du paquet et
`uninstall-hook` par `Bash` sont refusés par le verrou, sans chemin dans le texte vu par le modèle.
Un `NotebookEdit` sur un original non lu est arrêté avant le hook par Claude Code (« File has not
been read yet ») ; lien symbolique non créable sur ce poste (droit absent) ; délai dépassé non
provoqué. `install-hook` n'a pas été lancé sur un vrai `~/.claude/settings.json`.

Non vérifié à ce jour : le parcours complet depuis une session Claude Code avec le skill, le clic
humain sur le dialogue natif, la règle de pare-feu Windows, macOS. Les résultats détaillés restent locaux (`evals/`), hors du dépôt
public.

## Fonctionnement détaillé (état actuel)

**Chaîne d'un passage** (`pipeline.run`) : extraction, inspection (pièges Unicode, NFC, texte adressé à
une IA), règles, structure (`[IMAGE]` des signatures relabellisé), NER si le modèle est installé (sinon
le passage continue sans elle, constat `ner_absente`), entités avec les décisions relues, constats de
métadonnées, masquage, risque résiduel, seconde passe. Écrit dans `coffre/<id>/` : `masque.md`
(version en préparation, marqueur `valide_humain` daté du jour, avec `corps=` : 16 premiers caractères
de l'empreinte SHA-256 de tout ce qui suit le marqueur), `rapport.md` (valeurs réelles, jamais
publié), `ajustements.txt`, `correspondance.json` (table de travail, placeholder vers valeur, ambiguïtés
`[AMBIGU_n]` comprises, réécrite à chaque passage ; la publication en fige une copie) et `etat.json`
(`destination` : dossier courant du premier `traiter`, où sera publié le
fichier ; `pending` ; `ouverts` : alertes et ambiguïtés encore ouvertes ; `sha_masque` : empreinte du
corps de `masque.md` après le marqueur ; `sha_ajustements` ; `date` ; `original_name_hidden`). `etat.json`
est écrit en début de passage avec `pending` et `ouverts` à `null`, puis complété à la fin : un passage
interrompu ne laisse jamais un état validable. Les décisions survivent à la réécriture du fichier
d'ajustements : une alerte gardée reste écrite `A<n> garder`, une ambiguïté tranchée `M<n> [PLACEHOLDER]`
(numérotée après les ambiguïtés ouvertes, sa clé ne change pas), une commune gardée `C<n> garder`. Une
alerte `valeur_connue` n'est jamais exemptée : `garder` y est ignoré et la ligne repasse à `?`, seule
`masquer` la règle. Un placeholder qui n'existe pas (`M1 [TYPO_9]`) reste en attente. Comptent comme en
attente les lignes `?` et ces placeholders inconnus.

**Validation** : refusée (code 3, « des points restent ouverts ») tant que `pending` ou `ouverts` n'est
pas 0, si `etat.json` ne porte pas ces champs, ou si `masque.md` contient encore `[AMBIGU_` ; refusée
aussi (code 3, « fichiers du coffre modifiés depuis le dernier passage ») quand le corps de `masque.md`
ou `ajustements.txt` ne correspond plus aux empreintes du dernier passage, ou que le marqueur de
`masque.md` n'a pas le `corps=` de son corps (fichier écrit par la v4.5.0) : il faut `relancer`. Sinon
`masque.md` est redaté du jour, son empreinte SHA-256 calculée, puis `masque.md` et `rapport.md` sont
ouverts et la question posée (« Contrat <id> : relisez les fichiers ouverts. Publier ce contrat
masqué ? »). `publier` : le fichier est relu ; s'il a changé pendant la relecture, rien n'est publié
(« fichier modifié pendant la relecture, relancez », code 4) ; les contrôles d'avant la fenêtre sont
ensuite refaits (empreintes de `masque.md` et `ajustements.txt`, `pending` et `ouverts` d'`etat.json`) :
un ajustement ou un état modifié pendant la fenêtre donne « Contrat <id> : fichiers modifiés pendant la
relecture, rien n'a été publié ; relancez : legal-anonymiser relancer <id> » (code 3, audit v4.5.0,
constat F3) ; sinon il est publié dans la destination
enregistrée (« Publié : contrat-<id>.masque.md », suivi du rappel « La validation porte sur le texte
relu ; le risque résiduel listé reste visible pour le modèle. »), un dossier inaccessible en écriture
donne le code 4. `ajuster` : chemin neutre de `ajustements.txt`, code 3. `abandonner` ou fermeture de la
fenêtre : code 4. `impossible` (ni fenêtre ni terminal, cas d'un outil piloté par un modèle) :
« validation impossible ici : lancez vous-même `legal-anonymiser valider <id>` dans un terminal », code 4.
Sans chemin : `tkinter` absent ou sans affichage donne « Sélecteur de fichier indisponible : lancez
`legal-anonymiser traiter <chemin>` vous-même » (code 4), un sélecteur annulé « Aucun fichier choisi »
(code 4).

**Ce que la console affiche** (`sortie.py`, dictionnaire `MESSAGES`) : des comptes (entités, alertes,
ambiguïtés, points en attente), l'identifiant neutre du contrat et des chemins neutres (`./…` sous le
dossier courant, `coffre/<id>/…` sous le coffre, sinon `[chemin masqué]`). Jamais un texte du document,
le nom du fichier original, un chemin absolu, un fragment d'une ligne d'`ajustements.txt` ni le message
d'une exception imprévue ; seuls les messages fixes de nos propres modules (dépendance manquante,
fichier du coffre corrompu) sont relayés tels quels. Tout le passage tourne sous `sortie.quiet` :
sorties, avertissements et journaux Python de pypdf et spaCy sont absorbés (une écriture en code natif
sur les descripteurs 1 et 2, thinc ou libtiff via Pillow, passerait ; aucune constatée). Le chemin choisi n'est jamais
affiché ; si l'original est dans le dossier
courant, un avertissement sans chemin le signale. `--help` affiche `legal-anonymiser`, jamais le chemin
du script ; une erreur d'arguments (commande inconnue, argument en trop ou manquant) n'affiche que
« Arguments invalides : voir `legal-anonymiser --help`. » (code 2), jamais l'argument fautif, qui peut
être un chemin. Quand plus rien n'est à arbitrer mais que des alertes ou ambiguïtés restent ouvertes
(`pending` 0, `ouverts` > 0), le message dit « <n> alerte(s) ou ambiguïté(s) restent ouvertes : voir
coffre/<id>/ajustements.txt » (code 3), jamais « 0 point(s) à arbitrer ».

**Réidentification** (`reidentification.py`) : la première ligne du rapport doit être le marqueur du
fichier publié (même `id`, champ `corps=`) ; elle désigne `coffre/<id>/publications/<corps>.json`, la
table figée à cette publication. Seules les clés de cette table sont substituées (texte exact, la plus
longue d'abord), tout le reste (`[INCONNU_1]`, `[IMAGE]`) reste tel quel ; le résultat,
`coffre/<id>/rapport-final.md`, ne quitte pas le coffre. Ligne absente ou modifiée, autre contrat,
version jamais publiée, marqueur de la v4.5.0 sans `corps=` : refus, « aucune publication ne correspond à
ce rapport » (code 7), rien n'est écrit. La table de travail n'est jamais lue : retraiter l'original
modifié sans publier ne change pas les valeurs d'un rapport écrit sur une publication antérieure (audit
v4.5.0, constat F2).

## Formats lus (état actuel)

- **DOCX** : bibliothèque standard. Un bloc par paragraphe ; révisions, commentaires et
  texte caché dans des sections séparées.
- **PDF avec couche texte** : `pypdf`. Un bloc par page. Le texte en mode de rendu
  invisible, blanc, de moins de 2 pt, hors de la zone visible ou recouvert ensuite par une
  image part dans une section `cache` et produit un constat. Sont aussi signalés :
  JavaScript, action d'ouverture, fichier joint, mises à jour incrémentales, signature qui
  ne couvre pas tout le fichier. Un PDF chiffré, tronqué ou corrompu est refusé.
  Les valeurs des champs texte et liste vont dans le corps, les notes `/Text` et
  `/FreeText` en commentaire.
- **Numérisations** : le texte invisible ou recouvert, posé sur une image opaque qui couvre
  au moins 90 % de la page, est lu comme une couche OCR (corps, constat `texte_ocr`) et tient
  lieu de texte. Une page avec image mais sans texte, ou une page couverte par une image
  avec au plus 200 caractères visibles, passe par l'OCR local (Tesseract, langue `fra`),
  comme les images JPG et PNG données directement.
- **Limites PDF** : rectangles couvrants et transparence de l'état graphique ignorés ;
  espaces de couleur Separation et Indexed lus comme du gris ; JavaScript cherché dans les
  actions du catalogue et des liens, chaînes `/Next` comprises, pas dans les actions des
  pages ni des champs ; autres annotations (surlignage, etc.) non extraites.
- **Inspection** (`inspection.py`) : caractères de largeur nulle et contrôles bidi retirés et
  signalés, homoglyphes signalés, texte recomposé en NFC (un nom décomposé d'un PDF, e suivi de
  l'accent, arrive composé aux détecteurs).

## Détection (état actuel)

- **Règles** (`detection/regles.py`) : identifiants à forme fixe (IBAN, SIREN, SIRET, NIR,
  TVA, RCS, e-mail, téléphone, adresse, date et lieu de naissance, immatriculation, pièce
  d'identité, n° de contrat). La clé de contrôle type la mention, elle n'exempte jamais. Entre deux
  groupes d'un numéro ou d'une date de naissance, un saut de ligne vaut une espace (PDF replié, OCR :
  « FR76 1450\n8000 … », « le 17\nseptembre 1983 »).
  Un numéro après « contrat », « dossier », « client »… contient au moins un chiffre
  (« CONTRAT DE LOCATION », « LE CLIENT PAIE » : rien) ; le nom après « lieu-dit »,
  « résidence », « bâtiment » s'arrête avant une forme sociale ou une préposition en capitales
  (« GRAND EST BÂTIMENT SAS », « BÂTIMENT POUR TROIS MOIS » : rien).
  Naissance (« NÉE LE 2 JUIN 1990 À SAINT-ÉTIENNE »), capital (« 10 000 EUROS ») et RCS
  (« RCS DE LYON … ») sont lus aussi en capitales ; le lieu de naissance est un seul nom, composé
  par trait d'union ou apostrophe, après « Saint » ou un article au plus, suivi au plus de « sur »,
  « sous », « lès » ou « en » et d'un mot (« BOULOGNE SUR MER ») ; « À LYON DE NATIONALITÉ
  FRANÇAISE » donne « LYON ».
- **Structure** (`detection/structure.py`) : le bloc de comparution (« Entre les
  soussignés » jusqu'à « Il a été convenu », « Préambule » ou « Article 1 ») est découpé en
  parties numérotées ; chaque partie reçoit le rôle défini par « ci-après » ou
  « ci-dessous » (rôle connu, féminin ou pluriel compris, ou mot du vocabulaire) ou annoncé
  par « LE SALARIÉ : », ses représentants (« représenté(e) par », plusieurs possibles) et ses
  noms de naissance ou d'usage (« née MARTIN », « épouse LEROY »). Partout (candidats de
  noms dans `detection/noms.py`) : civilité suivie d'un nom (civilité incluse, particules et
  capitales comprises), société désignée par sa forme (la forme sociale reste visible), adresse
  après « demeurant », « domicilié », « dont le siège est », « sis », « résidant »,
  « habitant » (arrêt sur « et » devant une civilité ou une forme sociale). Quand une forme
  sociale a un nom plausible de chaque côté (« LA SOCIÉTÉ SAS DUVALCOURT CONSEIL »,
  « DUVALCOURT CONSEIL SAS IMMATRICULÉE »), chaque côté est jugé seul : un nom placé avant sa
  forme perd ses mots d'ouverture (« CONTRAT », « CONVENTION », « Gérant », articles,
  prépositions), ne commence pas par un article ou une préposition devant un mot capitalisé,
  garde ses mots courants
  (« Société Générale SA », « L'Oréal SA ») mais n'est pas fait que de mots d'annonce
  (« LA SOCIÉTÉ SAS X ») ; « et », « & » lient les mots d'un nom (« Dupont et Fils SARL »).
  « SA » devant un mot en capitales est le possessif (« MET SA VOITURE », « EXERCER SA MISSION, »),
  sauf si un marqueur de société suit dans les 80 caractères (« au capital », « immatriculée »,
  RCS, SIREN, SIRET, « dont le siège », « représentée par », « ci-après », « société anonyme » ;
  une virgule seule n'en est pas un), si « la », « entre », « société » précède comme mot
  entier, ou si une préposition suit (« X SA ENTRE LES SOUSSIGNÉS »). Les
  titres (« M. le Maire », « Maître d'Œuvre ») ne sont pas pris pour des noms. Après une ligne
  qui commence par « Fait à », « Lu et approuvé » ou « Signature », un « Fait à » suivi d'un
  lieu après une fin de phrase (« La Rochelle » admis, jamais un lieu fait seulement de mots
  connus comme « la demande du Bailleur »), ou une ligne de
  légendes (« Le Locataire  Le Bailleur ») : noms des blocs de signature, colonnes comprises,
  commune de « Fait à », et `[IMAGE]` devient `[SIGNATURE]`. Un terme défini qui n'est ni un
  rôle connu ni au vocabulaire (« ci-après Duvalcourt Conseil ») est masqué comme un nom.
- **Reconnaissance des noms** (`detection/ner.py`) : modèle spaCy `fr_core_news_lg`, local,
  chargé une fois par processus sans ses composants inutiles (seuls `tok2vec` et `ner` restent).
  PER devient PERSONNE, ORG SOCIETE, LOC COMMUNE (un seul mot) ou LIEU. Une entité faite de mots
  du vocabulaire (rôles, institutions) est ignorée ; coupée par une ponctuation de phrase, elle
  garde sa plus longue partie (un saut de ligne n'en est pas une : un prénom en fin de ligne et
  le nom à la ligne suivante restent un seul nom) ; articles, mots d'annonce et forme sociale sont
  retirés de ses bords. Un bloc plus long que
  `nlp.max_length` est découpé aux fins de paragraphe ou de phrase. Un bloc surtout en capitales
  est lu sur une copie à l'initiale majuscule, et seules ses entités de 2 à 4 mots sont gardées,
  sans mot-outil à l'intérieur autre qu'une liaison de nom (« TÉMOIN EST PRÉSENT » écarté,
  « BOULOGNE SUR MER » gardé) ; une entité en capitales s'arrête avant son premier verbe courant
  (« AWA DUPONT SIGNE » donne « AWA DUPONT »), jamais avant son premier mot ni avant le second
  après une civilité (« SIGNE HANSEN », « MADAME CLAIRE DEMEURE EST TÉMOIN » donne « MADAME CLAIRE
  DEMEURE ») ; un verbe qui ouvre une société lui appartient (« VERSE SAS »). Une commune d'un seul
  mot en capitales n'y est trouvée qu'après un code postal, « NÉ(E) LE … À », « FAIT À », ou par
  propagation ; seule dans le texte libre, elle reste visible et la seconde passe la signale. Une
  entité qui court sur deux lignes, ou sur deux colonnes (deux espaces ou plus, tabulation : les noms
  d'un bloc de signature), en fait deux si chaque partie porte au moins deux mots capitalisés
  hors particules (« DE LA FONTAINE » à la ligne reste avec le nom qui précède). Modèle absent :
  `ModelMissing`.
- **Mots-outils et verbes** (`detection/noms.py`) : `FUNCTION_WORDS` (est, et, de, la, par, pour,
  avec, dans, qui, que, dont, au, ce, se, lui, leur, notre…) et `CAPS_VERBS` (SIGNE, ACCEPTE,
  DÉCLARE, EST, SONT, SERA, A, ONT, DOIT, PEUT, REMET, VERSE, PAIE, OCCUPE, DEMEURE, AGISSANT…) sont
  des listes fixes. Elles servent à couper un nom en capitales sur-capturé, jamais les mots vides de
  spaCy, qui contiennent de vrais noms (HUI, MIN, SON, VU, LI…) ; aucune n'est jamais une forme
  d'un mot.
- **Entités et placeholders** (`entites.py`, `propagation.py`) : chevauchements résolus par la
  mention la plus longue (à égalité : règles, structure, NER, propagation). Une partie de la
  comparution forme une entité, chaque représentant une autre. Un nom ailleurs rejoint l'entité
  unique de même type qui porte sa forme (une personne ne rejoint jamais une société) ; deux
  entités qui la portent (homonymes, époux, « M. Kerbrat ») en font une mention ambiguë, à
  arbitrer. La coupe avant un verbe courant ne vaut que pour une personne isolée (sans partie ni
  rôle de comparution) : une partie, déjà bornée par la comparution (« MONSIEUR PAUL DONNE »,
  « MADAME SIGNE HANSEN »), et une société (« GRAND EST BÂTIMENT », « VERSE ») gardent leur
  étendue. Un nom en capitales sur-capturé (« MADAME N'DIAYE EST ENGAGÉE ») est rogné à la plus
  longue forme connue qui l'ouvre, si elle fait deux mots ou si un verbe courant, un mot-outil ou
  un mot du vocabulaire ou une particule la suit (« AWA N'DIAYE LA SOMME », « PAUL KERBRAT DU
  SERVICE » : rattachés à la partie) ; une particule après le seul prénom d'une partie
  (« MONSIEUR JEAN LE GALL », « JEAN DE LA FONTAINE », pour un Jean Kerbrat connu) dit au contraire
  que le nom continue ; sinon (« MADAME AWA DUPONT », où seul « AWA » est connu) il devient une
  nouvelle entité, dont les formes ne viennent que du début du nom (avant le premier verbe,
  mot-outil ou mot connu). Un nom de la NER chevauché par une forme connue n'en garde le
  reste que si celui-ci fait deux mots capitalisés hors vocabulaire, et l'entité recalcule ses
  formes. Chaque nom est ensuite cherché partout, sans casse ni
  accents, aussi après une élision (« d'Élodie », « D'AWA ») : forme complète, nom seul, prénom
  seul (3 lettres ou plus, hors vocabulaire), initiales (« J.-P. D. », « J. Dupont », « JP
  Dupont »), nom de société sans article ; un mot seul n'est pris qu'avec une majuscule
  (« Claire », pas « claire »). Placeholders `[BAILLEUR_1]`,
  `[REPRESENTANT_1]`… dès qu'un rôle est défini, sinon `[PERSONNE_1]`, `[ADRESSE_1]`… ; une
  ambiguïté `M1` devient `[AMBIGU_1]`. Les décisions (ambiguïté tranchée, entité démasquée,
  commune gardée, texte à masquer en plus) ne renumérotent jamais les placeholders.
- **Vocabulaire** (`data/vocabulaire.txt`) : environ 420 formes juridiques et courantes
  (mois, jours, intitulés, rôles, codes, institutions, formes sociales, formules de comparution
  comme « D'UNE PART », « IL A ÉTÉ CONVENU », « AU CAPITAL DE »), sans prénom, sans nom
  d'entreprise réelle, sans nom de ville sauf France.

## Masquage et seconde passe (état actuel)

- **Masquage** (`masquage.py`) : chaque mention, dans tous les blocs (corps, en-têtes, révisions,
  commentaires, texte caché), est remplacée par son placeholder de droite à gauche ; une ambiguïté
  non tranchée par `[AMBIGU_<n>]`. La civilité collée devant une personne part avec elle
  (« M. Kerbrat », « Mme et M. Dupont »). Deux étendues qui se chevauchent : la plus longue, puis la
  plus à gauche.
- **Seconde passe** (`controle.py`) : relit le texte masqué et produit des alertes `A1`, `A2`… dans
  l'ordre du document, positions sur le texte masqué :
  - `valeur_connue` : valeur d'une entité (forme canonique et ses formes, texte de chaque mention si
    les blocs d'origine sont passés à `check(..., original=blocs)`) encore visible, sans casse ni
    accents, minuscules comprises (« le dossier kerbrat ») ; jamais exemptée par une décision garder.
    Ignorées : valeurs de moins de 3 caractères, capital social. Une valeur d'un seul mot courant
    (« Juin », « Poste ») n'alerte que collée à une civilité, un rôle, une voie (« M. JUIN ») ou à un
    mot lui-même signalé (« Lucas Juin »).
  - `majuscule` : mot capitalisé hors début de phrase (début de bloc, après `. ! ? : ;` sauf
    abréviation « M. », « J. », « art. », après une puce), hors placeholder, sauf mot du vocabulaire
    ou mot-outil non juxtaposé à une civilité qui le précède, un rôle ou un mot de voie (particules,
    « et », « l' », « d' » sautés ; ponctuation, point compris, et colonnes coupent : « Mme France », « avenue de la
    République » alertent ; « M. le Maire », « MONSIEUR LE MAIRE », « en Avril. M. Kerbrat » non pour
    le mot courant). En
    début de ligne sans ponctuation avant, et en tête de phrase pour un mot en capitales (« DUPONT a
    signé »), seul un mot courant est exempté. Ligne en capitales (60 % des lettres) : mot collé à
    une civilité (« M. FRANCE », « M. LI »), ou mot de 3 lettres ou plus qui n'est ni au vocabulaire,
    ni mot-outil, ni verbe courant, ni mot vide de spaCy (facultatif) ; un mot-outil n'y est jamais
    signalé (« M. ET MME DURANT » : DURANT seul). La civilité elle-même n'est jamais signalée. Mots
    signalés consécutifs (espace, trait d'union, apostrophe) : une seule alerte (« DUVALCOURT MORVAN
    IMMOBILIER », « M. Le Gall ») ; un mot déjà couvert par une autre alerte (valeur connue, url…) en
    est retiré avant la fusion, ses voisins gardent la leur (« remis à Paul Kerbrat » : « Paul »
    majuscule, « Kerbrat » valeur connue). Un mot exempté par sa seule place en tête de phrase se joint
    à l'alerte voisine (« Locataire : Paul Durand », « Paul Kerbrat signe ») mais n'alerte jamais seul.
  - `chiffres` : 6 chiffres ou plus, séparés au plus par une espace, un point, une barre ou un tiret
    (« 06.12.34.56.78 », « 23/01234 »), hors date, montant (€, euros, EUR ou % dans les 3
    caractères), référence d'article (« art. L. 1234-5 ») ou de texte (« loi n° 89-462 »).
  - `arobase`, `url` ; `date_naissance` : date dans les 40 caractères après « né(e)(s) »,
    « date de naissance », ou « NE LE » / « NE À » écrits en capitales sans accent (« née MARTIN le
    2 juin 1965 » compris ; la négation en minuscules, « ne pourra … » ou « ne le résiliera pas avant
    le 1er juillet 2027 », non).
  - `initiales` : jeton isolé de 2 ou 3 capitales (« ED », « JK ») ou lettres pointées (« J.K. »,
    « J. D. », « J.-P. »), hors vocabulaire, rôle, mot-outil, forme sociale (« SA », « SCI ») et
    abréviation (« Ets », « NO ») ; « J. Dupont » n'en est pas une. Un jeton déjà signalé `majuscule`
    (« JK » en milieu de phrase, « LI HUI MIN » en une alerte) garde ce motif : `initiales` ne s'ajoute
    que là où rien d'autre n'alerte (tête de phrase après « Paraphes : », ligne en capitales).
  - Une décision garder exempte une occurrence des motifs autres que `valeur_connue`. Sa clé
    (`entites.occurrence_key`, ou `entites.Ranks` pour plusieurs clés) est `(localisation, texte
    normalisé, rang)`, le rang étant compté sur **tous les blocs de même localisation** dans l'ordre
    du document (corps, puis révisions, texte caché… dans l'ordre d'émission) : garder « Orange » du
    corps de la page 1 n'exempte pas « Orange » du texte caché de la page 1. La clé porte sur le
    texte masqué : quand le masquage change (nouvelle décision), les rangs peuvent bouger et le
    fichier d'ajustements (tâche 11) doit recalculer les clés sur le nouveau texte masqué. Une
    commune gardée n'est plus signalée, sauf collée à une civilité (« M. Valence »). Une étendue ne
    porte qu'une alerte, `valeur_connue` d'abord. Clés calculées seulement pour les formes gardées :
    un bloc de 200 000 caractères est relu en moins d'une seconde.
  - Limites connues : un mot capitalisé seul en début de phrase ou après « : » (« Témoin : Fabre. »,
    « Fabre signera ») n'est signalé que s'il est une valeur connue ou en capitales ; un nom en
    minuscules inconnu, un code postal seul ne sont pas signalés. En
    capitales, tout mot hors vocabulaire est signalé (verbes, adjectifs) : volume d'alertes élevé
    sur un contrat tout en capitales, à mesurer sur le corpus.

### Fichier d'ajustements (`ajustements.py`)

Une décision par ligne (`A…` alerte, `M…` ambiguïté, `C…` commune), clé relue depuis les champs
visibles `localisation | rang` (la localisation peut contenir « | »). Un `#` en début de ligne, même
indenté, est un commentaire ; un BOM est toléré. L'en-tête rappelle qu'une alerte `valeur_connue` ne
peut pas être gardée (« utilisez masquer »). Une ligne libre `masquer: texte` règle aussi, à la
réécriture, toute alerte non traitée portant le même texte (elle repasse en `masquer`). Les décisions
dont le texte a changé sont listées sous « Décisions périmées ».

### Validation humaine et publication

- **Validation** (`validation.py`) : le texte masqué et le rapport sont ouverts depuis le coffre avec
  l'application par défaut du système (seul sous-processus avec l'OCR, jamais attendu, échec
  ignoré), puis une boîte de dialogue pose la question « Relisez les fichiers ouverts. Publier ce
  contrat masqué ? » (la CLI y ajoute l'identifiant neutre) : Publier, Ajuster ou Abandonner ; fermer
  la fenêtre vaut abandon. Ordre d'essai : dialogue du système (voir « Dialogue de validation »),
  puis `tkinter`, puis le clavier seulement si l'entrée et la sortie standard sont des terminaux, et
  il faut taper le mot entier (`publier`, casse indifférente ; ni chiffre ni initiale) ; sinon la
  réponse est `impossible` et rien n'est publié. Dans la fenêtre `tkinter`, seul un clic publie :
  aucun bouton n'a le focus au départ, « Publier » est hors de l'ordre de tabulation, Entrée ne
  déclenche aucun bouton, et la commande Tk `send` (X11) est retirée. Aucune option, variable
  d'environnement, fichier ni tube ne répond à la place de l'utilisateur. Limite : un programme qui
  simule clavier ou souris sur la session de l'utilisateur, ou un pseudo-terminal piloté par un autre
  programme, n'est pas détecté.
- **Publication** (`publication.py`) : refusée, avant toute écriture, si l'identifiant n'est pas un id
  neutre connu du coffre (6 caractères hexadécimaux) ou si la première ligne n'est pas le marqueur
  `statut=valide_humain` de ce contrat, ou si son champ `corps=` manque ou ne correspond pas au corps
  du texte. Fige d'abord la table de travail en `coffre/<id>/publications/<corps>.json`, inscrit
  l'empreinte SHA-256 des octets écrits au registre avec la date du marqueur et `corps`, puis écrit
  `contrat-<id>.masque.md` de façon atomique, en UTF-8, octet pour octet sans conversion des fins de
  ligne (le rendu produit des `\n`), et enfin le chemin, l'empreinte et la date dans l'état du contrat.
  Les entrées du registre écrites par la v4.5.0 (sans `corps`) restent lues par `verifier`. Deux
  publications au corps identique (seules des valeurs masquées ont changé) partagent une table : la
  dernière publiée.
- **Vérification** : `publie` si l'empreinte du fichier est au registre ; `modifie` si sa première
  ligne est un marqueur dont l'identifiant est connu du coffre (BOM et fins de ligne `\r\n`
  tolérés) ; sinon, ou si le fichier est illisible, `inconnu`. Jamais de contenu affiché.

### Dialogue de validation

Ordre d'essai : dialogue natif du système ci-dessous ; s'il est indisponible, fenêtre `tkinter` ;
sans affichage, clavier si l'entrée et la sortie standard sont des terminaux ; sinon `impossible`
(rien n'est publié). Mêmes garanties à chaque étape : aucune option de pré-acceptation, « Publier »
jamais bouton par défaut, fermer la fenêtre vaut abandon (nuance clavier sous Windows ci-dessous).

- **Windows** : `TaskDialogIndirect` des contrôles communs v6 (`comctl32`, via `ctypes`, sans
  dépendance) : titre `legal-france`, question en texte principal, trois boutons « Publier »,
  « Ajuster », « Abandonner ». « Abandonner » est le bouton par défaut (à l'ouverture, Entrée ou
  Échap abandonnent), la croix de fermeture vaut abandon. Contrairement à la fenêtre `tkinter`, les
  trois boutons sont dans l'ordre de tabulation : Tab jusqu'à « Publier » puis Entrée ou Espace
  publie. C'est voulu : un choix délibéré au clavier, par une personne devant l'écran, vaut un clic
  (aucun appui unique ne publie). Si les contrôles communs v6 ne sont pas chargés, l'outil active le
  manifeste de `shell32` (contexte d'activation, appel réel vérifié en test sans fenêtre) ; si
  `TaskDialogIndirect` reste introuvable ou renvoie une erreur, repli sur `tkinter` sans plantage.
- **macOS** : `osascript -e 'display dialog …'`, la question passée en argument (aucun shell), bouton
  par défaut et bouton d'annulation « Abandonner ». Seul ce bouton (ou Échap, erreur -128) donne
  « abandonner » ; `osascript` absent ou toute autre erreur (session sans interface) : repli sur
  `tkinter`, puis terminal, puis `impossible`.
- **Linux et autres** : `tkinter` directement.
- La signature de `validation.confirm` et ses garanties sont inchangées ; les tests ne passent que par
  des appels système remplacés, jamais par une vraie fenêtre. Le clic humain sur la fenêtre native n'a
  pas encore été exécuté (voir « État de la validation »).

## Licences des dépendances

Vérifiées à la source le 2026-10-19. Le projet ne redistribue aucune dépendance ; elles s'installent
sur le poste de l'utilisateur. Cet outil est la seule exception à la règle « Python standard, sans
dépendance » du dépôt ; les 8 skills fonctionnent sans lui et les paquets distribués ne l'embarquent pas.

| Bibliothèque | Licence | Source | Vérifiée le |
|---|---|---|---|
| pypdf | BSD 3-Clause | https://github.com/py-pdf/pypdf/blob/main/LICENSE | 2026-10-19 |
| Pillow | MIT-CMU (HPND) | https://github.com/python-pillow/Pillow/blob/main/LICENSE | 2026-10-19 |
| spaCy | MIT | https://github.com/explosion/spaCy/blob/master/LICENSE | 2026-10-19 |
| fr_core_news_lg | LGPL-LR | https://github.com/explosion/spacy-models/releases/tag/fr_core_news_lg-3.8.0 | 2026-10-19 |
| Tesseract | Apache 2.0 | https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE | 2026-10-19 |

PyMuPDF est exclu (AGPL).
