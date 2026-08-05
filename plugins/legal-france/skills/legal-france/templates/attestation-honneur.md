---
type: attestation-honneur
domain: meta
short_description: Attestation sur l'honneur (déclaration d'un fait, d'une situation, d'un engagement)
required_fields:
  - declarant_nom
  - declarant_date_naissance
  - declarant_lieu_naissance
  - declarant_adresse
  - fait_declare
  - usage_de_attestation
optional_fields:
  - destinataire
applicable_law:
  - art. 441-7 C. pén. (fausse attestation, sanctions)
disclaimer_level: high
---

## Questionnaire

1. Vos nom et prénom complets ?
2. Date de naissance (JJ/MM/AAAA) ?
3. Lieu de naissance (ville, département) ?
4. Adresse complète ?
5. Quel fait précis attestez-vous ? (formuler à la première personne : "Je soussigné(e)… atteste sur l'honneur que…")
6. À quoi servira cette attestation ? (ex : démarche CAF, dossier de logement, attestation d'hébergement, etc.)
7. *Optionnel :* destinataire précis (administration, organisme, personne) ?

## Template

```
ATTESTATION SUR L'HONNEUR

Je soussigné(e) {{declarant_nom}},
né(e) le {{declarant_date_naissance}} à {{declarant_lieu_naissance}},
demeurant {{declarant_adresse}},

atteste sur l'honneur que {{fait_declare}}.

Cette attestation est délivrée pour servir et valoir ce que de droit{{#if destinataire}}, à l'attention de {{destinataire}}{{/if}}, dans le cadre de {{usage_de_attestation}}.

Je certifie sur l'honneur que les informations fournies sont exactes et complètes. Je reconnais avoir été informé(e) qu'une fausse déclaration m'expose aux sanctions prévues par l'article 441-7 du Code pénal (jusqu'à un an d'emprisonnement et 15 000 euros d'amende).

Fait à {{ville_signature}}, le {{date_du_jour}}.

Signature :
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur de l'article 441-7 du Code pénal (peines actualisées).
- Joindre une copie d'une pièce d'identité (recommandé par la plupart des organismes destinataires).
- La signature doit être manuscrite originale.
- Pour une attestation d'hébergement : l'hébergeant signe + joint sa pièce d'identité + un justificatif de domicile.
- Conserver une copie signée.
