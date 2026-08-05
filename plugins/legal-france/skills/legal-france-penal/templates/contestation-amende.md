---
type: contestation-amende
domain: penal
short_description: Contestation d'amende forfaitaire auprès de l'officier du ministère public (OMP)
required_fields:
  - contrevenant_nom
  - contrevenant_adresse
  - numero_avis_contravention
  - date_constatation
  - lieu_constatation
  - nature_infraction
  - motif_contestation
optional_fields:
  - vehicule_immatriculation
  - vehicule_proprietaire    # if different from contrevenant
  - pieces_jointes
applicable_law:
  - art. 529-2 C. proc. pén. (procédure de l'amende forfaitaire)
  - art. 529-2 C. proc. pén. (requête en exonération, 45 jours) et art. 530 (réclamation contre l'amende forfaitaire MAJORÉE, 30 jours)
disclaimer_level: high
---

## Questionnaire

1. Nom complet du contrevenant (personne destinataire de l'avis) ?
2. Adresse complète ?
3. Numéro de l'avis de contravention (figurant sur l'avis reçu) ?
4. Date de constatation de l'infraction ?
5. Lieu de constatation (adresse ou route) ?
6. Nature de l'infraction (excès de vitesse, stationnement gênant, feu rouge, etc.) ?
7. *Si infraction véhicule :* immatriculation du véhicule concerné ?
8. *Si véhicule prêté ou loué :* nom du propriétaire / locataire du véhicule au moment des faits ?
9. Motif précis et factuel de la contestation (ex : "ce n'est pas mon véhicule", "véhicule vendu à cette date", "panneau de signalisation non visible", "erreur sur l'identité du conducteur", "véhicule volé") ?
10. *Optionnel :* pièces que vous pouvez joindre pour prouver vos dires (certificat de cession, déclaration de vol, photos, témoignages) ?

(Délai légal pour contester : **45 jours** à compter de l'envoi de l'avis, au-delà, la contravention devient une amende forfaitaire majorée.)

## Template

```
{{contrevenant_nom}}
{{contrevenant_adresse}}

Lettre recommandée avec accusé de réception

Officier du Ministère Public
Centre Automatisé de Constatation des Infractions Routières (ou tribunal indiqué sur l'avis)
{{adresse_omp_indique_sur_avis}}

À {{ville_contrevenant}}, le {{date_du_jour}}

Objet : Requête en exonération, Avis de contravention n° {{numero_avis_contravention}}

Monsieur l'Officier du Ministère Public,

J'ai l'honneur de contester l'avis de contravention référencé ci-dessus, qui m'a été adressé concernant les faits suivants :

- **Date de constatation** : {{date_constatation}}
- **Lieu** : {{lieu_constatation}}
- **Nature de l'infraction** : {{nature_infraction}}
{{#if vehicule_immatriculation}}- **Véhicule concerné** : immatriculation {{vehicule_immatriculation}}{{/if}}

### Motif de la contestation

{{motif_contestation}}

{{#if vehicule_proprietaire}}
Au moment des faits, le véhicule était {{situation_vehicule}} (au nom de {{vehicule_proprietaire}}). Je joins les pièces correspondantes.
{{/if}}

{{#if pieces_jointes}}
### Pièces jointes

{{pieces_jointes}}
{{/if}}

En application de l'article 529-2 du Code de procédure pénale, et dans le délai légal de 45 jours, je sollicite l'exonération de cette contravention.

Je vous prie de bien vouloir m'adresser votre décision motivée par retour de courrier, et de me notifier toute convocation devant le tribunal de police si vous décidiez de maintenir la poursuite.

Veuillez agréer, Monsieur l'Officier du Ministère Public, l'expression de ma considération distinguée.

{{contrevenant_nom}}
[Signature]
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur des articles 529-2 et 530 du Code de procédure pénale (délais et procédure).
- **Délai impératif : 45 jours** à compter de l'envoi de l'avis. Cachet de la poste faisant foi.
- L'envoi en lettre recommandée avec accusé de réception est **fortement recommandé** comme preuve d'envoi dans les délais.
- Joindre obligatoirement (selon les cas) :
  - L'original de l'avis de contravention OU la carte de paiement détachable (selon les instructions au dos de l'avis).
  - Le formulaire de requête en exonération (si fourni).
  - Les pièces justifiant la contestation (certificat de cession du véhicule, déclaration de vol, etc.).
- Conséquence d'une contestation rejetée : l'OMP peut transmettre au tribunal de police (les juridictions de proximité ont été supprimées au 1er juillet 2017). En cas de condamnation, le tribunal prononce une amende PÉNALE qui peut être supérieure à l'amende forfaitaire, plus d'éventuels frais.
- Si l'avis a été reçu il y a plus de 45 jours : il s'agit alors d'une amende forfaitaire **majorée** ; réclamation motivée à adresser à l'OFFICIER DU MINISTÈRE PUBLIC (pas au Trésor Public) dans les **30 jours** de l'envoi de l'avis (art. 530 CPP ; délai porté à 3 mois dans certains cas routiers avec avis LRAR). Vérifié le 2026-08-05.
- En cas de contestation pour "non-désignation du conducteur" (entreprises possédant des véhicules) : ne pas utiliser ce modèle, procédure spécifique.
