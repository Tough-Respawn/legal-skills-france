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

## Détection (état actuel)

- **Règles** (`detection/regles.py`) : identifiants à forme fixe (IBAN, SIREN, SIRET, NIR,
  TVA, RCS, e-mail, téléphone, adresse, date et lieu de naissance, immatriculation, pièce
  d'identité, n° de contrat). La clé de contrôle type la mention, elle n'exempte jamais.
  Naissance (« NÉE LE 2 JUIN 1990 À SAINT-ÉTIENNE »), capital (« 10 000 EUROS ») et RCS
  (« RCS DE LYON … ») sont lus aussi en capitales ; le lieu de naissance est un seul nom, composé
  par trait d'union ou apostrophe, après « Saint » ou un article au plus (« À LYON DE NATIONALITÉ
  FRANÇAISE » donne « LYON »).
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
  est lu sur une copie à l'initiale majuscule, et seules ses entités de 2 à 4 mots sont gardées :
  une commune d'un seul mot en capitales n'y est trouvée qu'après un code postal, « NÉ(E) LE …
  À », « FAIT À », ou par propagation ; seule dans le texte libre, elle reste visible et la
  seconde passe la signale. Modèle absent : `ModelMissing`.
- **Entités et placeholders** (`entites.py`, `propagation.py`) : chevauchements résolus par la
  mention la plus longue (à égalité : règles, structure, NER, propagation). Une partie de la
  comparution forme une entité, chaque représentant une autre. Un nom ailleurs rejoint l'entité
  unique de même type qui porte sa forme (une personne ne rejoint jamais une société) ; deux
  entités qui la portent (homonymes, époux, « M. Kerbrat ») en font une mention ambiguë, à
  arbitrer. Un nom en capitales sur-capturé (« MADAME N'DIAYE EST ENGAGÉE ») est rogné à la plus
  longue forme connue qui l'ouvre, si elle fait deux mots ou si un mot vide ou courant la suit ;
  sinon (« MADAME AWA DUPONT EST TÉMOIN », où seul « AWA » est connu) il reste entier, en nouvelle
  entité. Chaque nom est ensuite cherché partout, sans casse ni
  accents, aussi après une élision (« d'Élodie », « D'AWA ») : forme complète, nom seul, prénom
  seul (3 lettres ou plus, hors vocabulaire), initiales (« J.-P. D. », « J. Dupont », « JP
  Dupont »), nom de société sans article ; un mot seul n'est pris qu'avec une majuscule
  (« Claire », pas « claire »). Placeholders `[BAILLEUR_1]`,
  `[REPRESENTANT_1]`… dès qu'un rôle est défini, sinon `[PERSONNE_1]`, `[ADRESSE_1]`… ; une
  ambiguïté `M1` devient `[AMBIGU_1]`. Les décisions (ambiguïté tranchée, entité démasquée,
  commune gardée, texte à masquer en plus) ne renumérotent jamais les placeholders.
- **Vocabulaire** (`data/vocabulaire.txt`) : environ 400 formes juridiques et courantes
  (mois, jours, intitulés, rôles, codes, institutions, formes sociales), sans prénom, sans
  nom d'entreprise réelle, sans nom de ville sauf France.

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
