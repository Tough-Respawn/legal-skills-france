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
  « DUVALCOURT CONSEIL SAS IMMATRICULÉE »), chaque côté est jugé seul : un candidat fait
  seulement de mots du vocabulaire est rejeté, un nom placé avant sa forme ne commence pas par
  un article ou une préposition devant un mot capitalisé, et « et », « & » lient les mots d'un
  nom (« Dupont et Fils SARL »). « SA » devant un mot connu en capitales est le possessif. Les
  titres (« M. le Maire », « Maître d'Œuvre ») ne sont pas pris pour des noms. Après une ligne
  qui commence par « Fait à », « Lu et approuvé » ou « Signature », un « Fait à » suivi d'un
  lieu après une fin de phrase (jamais « Fait à la demande du Bailleur »), ou une ligne de
  légendes (« Le Locataire  Le Bailleur ») : noms des blocs de signature, colonnes comprises,
  commune de « Fait à », et `[IMAGE]` devient `[SIGNATURE]`. Un terme défini qui n'est ni un
  rôle connu ni au vocabulaire (« ci-après Duvalcourt Conseil ») est masqué comme un nom.
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
