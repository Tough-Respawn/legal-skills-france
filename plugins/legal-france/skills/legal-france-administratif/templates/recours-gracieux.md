---
type: recours-gracieux
domain: administratif
short_description: Recours gracieux contre une décision administrative (auprès de l'autorité qui a pris la décision)
required_fields:
  - requerant_nom
  - requerant_adresse
  - autorite_destinataire
  - autorite_adresse
  - objet_decision
  - moyens_de_fait
optional_fields:
  - reference_decision
  - date_decision
  - date_notification
  - pieces_jointes
applicable_law:
  - art. L. 410-1 et L. 411-2 CRPA (recours et régime général)
  - art. R. 421-1, R. 421-2, R. 421-5 et R. 421-7 CJA (délais et opposabilité selon le cas)
  - textes spéciaux gouvernant la décision, notamment L. 600-12-2 C. urb. si applicable
disclaimer_level: high
qualification_fields:
  - regime_decision
  - mentions_recours
  - mode_notification
  - recours_prealable
  - demandes_anterieures
  - urgence_execution
  - territoire
derived_fields:
  - designation_decision
  - presentation_decision
  - ville_requerant
  - date_du_jour
  - titre_autorite
  - moyens_de_droit
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`.

Lire la décision, ses annexes et sa notification avant de fixer le délai
ou de promettre sa conservation. Identifier le régime, l'autorité, les
voies obligatoires et l'objectif : réexamen, retrait, suspension ou recours.
Une décision d'urbanisme, d'éloignement, fiscale ou de prestations sociales
ne doit pas être traitée automatiquement par le régime général.

Le recours gracieux n'a pas un effet interruptif universel. Vérifier la
règle spéciale et son application dans le temps ; par exemple, examiner
L. 600-12-2 C. urb. pour les autorisations d'urbanisme. Si l'acte ou les
voies de recours manquent, demander leur contenu et signaler l'urgence
éventuelle avant une simple lettre de réexamen.

La règle de délai, sa computation et l'effet du recours appartiennent au
bilan juridique qui précède la lettre, avec leurs inconnues. Le corps utilise
la réserve neutre de voies de recours figurant dans le modèle : conserver
cette phrase sans y ajouter de déclaration sur la recevabilité du dépôt.
Une qualification certaine suppose un acte et des dates effectivement établis.

Pièces utiles : décision et notification intégrales, demande initiale et
accusé de réception, recours antérieurs, réponses et pièces fondant les
moyens. Le modèle peut formuler le droit à partir du récit de l'utilisateur,
sans exiger qu'il fournisse lui-même les articles applicables.

## Questionnaire

1. Quel résultat recherchez-vous et quelle décision précise contestez-vous ? Pouvez-vous fournir l'acte, ses annexes et les voies/délais indiqués ?
2. Quelles dates de décision, envoi, publication, présentation et réception sont établies, avec quelles preuves ? S'agit-il d'une décision expresse ou d'un silence sur une demande ?
3. Quelle autorité, quelle matière et quel territoire ? L'acte prévoit-il un recours préalable obligatoire ou une voie spéciale ?
4. Une exécution, mesure d'éloignement ou audience est-elle imminente ? Quels recours/demandes avez-vous déjà faits, à quelles dates et avec quelles réponses ?
5. Quels faits ou motifs contestez-vous, quelles pièces les étayent, et quelle modification demandez-vous ? Des moyens de droit peuvent être proposés après vérification.
6. Après qualification : identité/adresse, référence et objet de l'acte, coordonnées exactes de l'autorité, ou champs anonymisés ?

## Template

```
{{requerant_nom}}
{{requerant_adresse}}

Lettre recommandée avec accusé de réception

{{autorite_destinataire}}
{{autorite_adresse}}

À {{ville_requerant}}, le {{date_du_jour}}

Objet : Recours gracieux : {{designation_decision}}

Madame, Monsieur le {{titre_autorite}},

{{presentation_decision}}

Je sollicite le réexamen de cette décision relative à {{objet_decision}}, pour les raisons exposées ci-dessous.

### En droit

Les règles et observations suivantes fondent ma demande :

{{moyens_de_droit}}

### En fait

Les éléments de fait suivants justifient, selon moi, un réexamen :

{{moyens_de_fait}}

{{#if pieces_jointes}}
### Pièces jointes

Je joins à la présente :

{{pieces_jointes}}
{{/if}}

### Demande

En conséquence, je sollicite respectueusement de votre haute bienveillance le retrait de la décision contestée, et la prise d'une nouvelle décision tenant compte des observations exposées ci-dessus.

Je me réserve l’exercice des voies de recours ouvertes par les textes applicables.

Je reste à votre disposition pour toute information complémentaire et vous prie d'agréer, Madame, Monsieur le {{titre_autorite}}, l'expression de ma haute considération.

{{requerant_nom}}
[Signature]
```

## Vérifications juridiques avant envoi

- Déterminer le champ du CRPA, le texte spécial et la juridiction compétente. Vérifier les dates, les mentions de recours, un recours préalable obligatoire et les démarches déjà faites avant de calculer une échéance.
- Le bilan juridique extérieur à la lettre expose les effets vérifiés pour cette décision, séparément de la réserve neutre de recours du corps. Ne pas annoncer deux mois ni une interruption du délai contentieux pour tous les actes. L. 600-12-2 C. urb. prévoit notamment un régime distinct pour les décisions relatives aux autorisations d'urbanisme : vérifier son champ et son application temporelle.
- Distinguer recours gracieux recevable et maintien éventuel du délai contentieux. Un simple recours administratif ne suspend pas automatiquement l'exécution ; examiner une voie urgente adaptée lorsque les faits le nécessitent.
- Vérifier la règle applicable à la réponse ou au silence, le point de départ du recours suivant et le mode/preuve de dépôt. Ne pas présenter le recommandé comme un canal obligatoire universel ni le cachet postal comme décisif pour toute procédure.
- `designation_decision` et `presentation_decision` identifient soit la décision expresse avec les références et dates établies, soit la décision implicite avec la demande, sa réception et le délai de silence vérifiés. Ne pas inventer un numéro ou une notification pour une décision implicite.
- `moyens_de_droit` est construit à partir des faits rapportés et des sources vérifiées ; ne pas inventer un fait ou une pièce pour compléter un moyen.
- Sources contrôlées pour ces corrections le 2026-09-10 : https://www.service-public.gouv.fr/particuliers/vosdroits/F2474 et https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000052859788 (L. 600-12-2). Les délais spéciaux doivent être examinés dans chaque dossier.
