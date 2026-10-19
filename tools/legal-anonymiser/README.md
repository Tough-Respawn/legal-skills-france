# legal-anonymiser

Pseudonymisation locale de contrats, sans réseau. Squelette : le contenu est
complété par les tâches suivantes.

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
  avec au plus 200 caractères visibles, est repérée pour l'OCR, qui n'est pas encore
  branché.
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
  d'identité, n° de contrat). La clé de contrôle type la mention, elle n'exempte jamais.
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
  entité qui court sur deux lignes en fait deux si chaque ligne porte au moins deux mots capitalisés
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
    minuscules inconnu, des initiales (« J. D. »), un code postal seul ne sont pas signalés. En
    capitales, tout mot hors vocabulaire est signalé (verbes, adjectifs) : volume d'alertes élevé
    sur un contrat tout en capitales, à mesurer sur le corpus.

## Licences des dépendances

Vérifiées à la source le 2026-10-19. Le projet ne redistribue aucune dépendance.

| Bibliothèque | Licence | Source | Vérifiée le |
|---|---|---|---|
| pypdf | BSD 3-Clause | https://github.com/py-pdf/pypdf/blob/main/LICENSE | 2026-10-19 |
| Pillow | MIT-CMU (HPND) | https://github.com/python-pillow/Pillow/blob/main/LICENSE | 2026-10-19 |
| spaCy | MIT | https://github.com/explosion/spaCy/blob/master/LICENSE | 2026-10-19 |
| fr_core_news_lg | LGPL-LR | https://github.com/explosion/spacy-models/releases/tag/fr_core_news_lg-3.8.0 | 2026-10-19 |
| Tesseract | Apache 2.0 | https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE | 2026-10-19 |

PyMuPDF est exclu (AGPL).

### Fichier d'ajustements (`ajustements.py`)

Une décision par ligne (`A…` alerte, `M…` ambiguïté, `C…` commune), clé relue depuis les champs
visibles `localisation | rang` (la localisation peut contenir « | »). Un `#` en début de ligne, même
indenté, est un commentaire ; un BOM est toléré. Une ligne libre `masquer: texte` règle aussi, à la
réécriture, toute alerte non traitée portant le même texte (elle repasse en `masquer`). Les décisions
dont le texte a changé sont listées sous « Décisions périmées ».

## Validation humaine et publication

- **Validation** (`validation.py`) : le texte masqué et le rapport sont ouverts depuis le coffre avec
  l'application par défaut du système (seul sous-processus avec l'OCR, jamais attendu, échec
  ignoré), puis une fenêtre native pose la question « Relisez les fichiers ouverts. Publier ce
  contrat masqué ? » (la CLI y ajoute l'identifiant neutre) : Publier, Ajuster ou Abandonner ; fermer
  la fenêtre vaut abandon. Seul un clic publie : aucun bouton n'a le focus au départ, « Publier » est
  hors de l'ordre de tabulation, Entrée ne déclenche aucun bouton, et la commande Tk `send` (X11) est
  retirée. Sans `tkinter` ou sans affichage, la question passe au clavier seulement si l'entrée et la
  sortie standard sont des terminaux, et il faut taper le mot entier (`publier`, casse indifférente ;
  ni chiffre ni initiale) ; sinon la réponse est `impossible` et rien n'est publié. Aucune option,
  variable d'environnement, fichier ni tube ne répond à la place de l'utilisateur. Limite : un
  programme qui simule clavier ou souris sur la session de l'utilisateur, ou un pseudo-terminal piloté
  par un autre programme, n'est pas détecté.
- **Publication** (`publication.py`) : refusée, avant toute écriture, si l'identifiant n'est pas un id
  neutre connu du coffre (6 caractères hexadécimaux) ou si la première ligne n'est pas le marqueur
  `statut=valide_humain` de ce contrat. Écrit `contrat-<id>.masque.md` de façon atomique, en UTF-8,
  octet pour octet sans conversion des fins de ligne (le rendu produit des `\n`), inscrit d'abord
  l'empreinte SHA-256 des octets écrits au registre avec la date du marqueur, puis le chemin,
  l'empreinte et la date dans l'état du contrat.
- **Vérification** : `publie` si l'empreinte du fichier est au registre ; `modifie` si sa première
  ligne est un marqueur dont l'identifiant est connu du coffre (BOM et fins de ligne `\r\n`
  tolérés) ; sinon, ou si le fichier est illisible, `inconnu`. Jamais de contenu affiché.
