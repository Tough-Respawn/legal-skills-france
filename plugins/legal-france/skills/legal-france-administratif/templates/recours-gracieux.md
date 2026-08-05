---
type: recours-gracieux
domain: administratif
short_description: Recours gracieux contre une décision administrative (auprès de l'autorité qui a pris la décision)
required_fields:
  - requerant_nom
  - requerant_adresse
  - autorite_destinataire
  - autorite_adresse
  - reference_decision
  - date_decision
  - date_notification
  - objet_decision
  - moyens_de_droit
  - moyens_de_fait
optional_fields:
  - pieces_jointes
applicable_law:
  - art. L. 410-1 à L. 412-7 CRPA (recours administratifs préalables)
  - art. R. 421-1 et s. CJA (délais et formes, 2 mois pour le recours contentieux)
disclaimer_level: high
---

## Questionnaire

1. Vos nom et adresse (le requérant) ?
2. Nom exact de l'autorité qui a pris la décision (préfet de X, maire de Y, directeur de la CAF, etc.) ?
3. Adresse complète de cette autorité ?
4. Référence précise de la décision contestée (numéro, intitulé) ?
5. Date de la décision ?
6. Date à laquelle vous avez reçu la notification de cette décision (point de départ du délai de 2 mois) ?
7. Objet exact de la décision (ce qu'elle décide concrètement à votre égard) ?
8. Vos moyens de droit (sur quels textes ou principes la décision vous semble illégale : incompétence, vice de forme, violation de la loi, détournement de pouvoir, erreur d'appréciation) ?
9. Vos moyens de fait (en quoi les faits ont-ils été mal appréciés par l'administration ; éléments nouveaux ou ignorés) ?
10. *Optionnel :* pièces que vous joignez ?

(Délai impératif : **2 mois** à compter de la notification. Le recours gracieux conserve le délai pour saisir le tribunal administratif si rejeté.)

## Template

```
{{requerant_nom}}
{{requerant_adresse}}

Lettre recommandée avec accusé de réception

{{autorite_destinataire}}
{{autorite_adresse}}

À {{ville_requerant}}, le {{date_du_jour}}

Objet : Recours gracieux contre la décision n° {{reference_decision}} du {{date_decision}}

Madame, Monsieur le {{titre_autorite}},

Par la présente, je sollicite le retrait, ou à défaut la révision, de la décision référencée en objet, qui m'a été notifiée le {{date_notification}} et dont l'objet est : {{objet_decision}}.

### En droit

Je considère que cette décision est entachée d'illégalité pour les motifs suivants :

{{moyens_de_droit}}

### En fait

Les éléments suivants n'ont pas été appréciés à leur juste portée :

{{moyens_de_fait}}

{{#if pieces_jointes}}
### Pièces jointes

Je joins à la présente :

{{pieces_jointes}}
{{/if}}

### Demande

En conséquence, je sollicite respectueusement de votre haute bienveillance le retrait de la décision contestée, et la prise d'une nouvelle décision tenant compte des observations exposées ci-dessus.

Je vous rappelle que, conformément aux articles L. 411-2 du Code des relations entre le public et l'administration et R. 421-2 du Code de justice administrative, le présent recours conserve le délai du recours contentieux. À défaut de réponse de votre part dans un délai de deux mois, ce silence vaudra décision implicite de rejet (sauf disposition contraire) susceptible de recours pour excès de pouvoir devant le tribunal administratif compétent.

Je reste à votre disposition pour toute information complémentaire et vous prie d'agréer, Madame, Monsieur le {{titre_autorite}}, l'expression de ma haute considération.

{{requerant_nom}}
[Signature]
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur des articles L. 410-1, L. 411-2 du CRPA et R. 421-1, R. 421-2 du CJA.
- **Délai impératif : 2 mois** à compter de la notification de la décision contestée. Cachet de la poste faisant foi.
- Envoi en lettre recommandée avec accusé de réception **obligatoire** pour preuve d'envoi dans les délais.
- Identifier la bonne autorité destinataire : pour un recours **gracieux**, c'est l'autorité qui a pris la décision ; pour un recours **hiérarchique**, c'est son supérieur hiérarchique.
- En cas d'absence de réponse pendant 2 mois → décision implicite de rejet (silence vaut rejet : règle générale ; certaines décisions ont au contraire un silence valant acceptation, à vérifier).
- Pour conserver le délai du recours contentieux : il est conseillé de saisir le **tribunal administratif** dans les 2 mois suivant la décision explicite de rejet, OU dans les 2 mois suivant la naissance de la décision implicite de rejet (donc 4 mois après le recours gracieux non répondu).
- Cas particulier : matière fiscale, sécurité sociale, étrangers → procédures spécifiques.
- En cas d'urgence (acte exécutoire imminent) : envisager parallèlement un **référé-suspension** devant le tribunal administratif (art. L. 521-1 CJA).
