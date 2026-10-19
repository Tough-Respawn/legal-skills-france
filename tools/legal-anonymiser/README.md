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
