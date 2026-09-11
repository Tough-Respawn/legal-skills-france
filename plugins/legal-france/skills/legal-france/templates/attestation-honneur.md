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
qualification_fields:
  - connaissance_personnelle
  - periode_fait
  - formalite_destinataire
  - pieces_disponibles
derived_fields:
  - ville_signature
  - date_du_jour
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`.

Vérifier l'usage et la nature exacte du fait à attester. Distinguer une
attestation administrative d'un témoignage destiné à la justice, dont les
formalités doivent être examinées séparément. Ne pas transformer une
supposition, une déclaration d'autrui ou un engagement futur en fait
personnellement constaté. Une attestation mensongère ne se corrige pas par
un avertissement. Une date incertaine reste à établir ; cette incertitude
ne suffit pas à conclure que l'utilisateur commet une infraction. Pour un
hébergement, ne pas ajouter gratuité, continuité ou absence de participation
aux frais si ces faits ne sont pas fournis : les demander ou laisser le
passage à compléter dans l'acte. Demander seulement les justificatifs utiles
à l'organisme.

## Questionnaire

1. À quel organisme et pour quelle démarche cette attestation est-elle destinée ? Un formulaire ou des mentions sont-ils imposés ?
2. Quel fait précis connaissez-vous personnellement, à quelles dates ou pendant quelle période ? Distinguer ce que vous avez constaté de ce qui vous a été rapporté.
3. Quelles pièces utiles possédez-vous et lesquelles l'organisme demande-t-il ? Ne transmettre que les éléments nécessaires à la démarche.
4. Après qualification : nom, adresse et, si utiles au formulaire, date et lieu de naissance, destinataire ? Des champs anonymisés sont possibles.

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
- Vérifier les justificatifs exigés par le destinataire ; ne pas demander systématiquement une copie intégrale de pièce d’identité pour analyser la demande.
- Vérifier le mode de signature accepté pour la démarche ; ne pas présenter la signature manuscrite originale comme une exigence universelle.
- Pour une attestation d’hébergement : vérifier auprès du destinataire les pièces et formalités requises ; ne pas qualifier une pièce de disponible avant confirmation.
- Conserver une copie signée.

- Contrôle du 2026-09-10 : [art. 441-7 C. pén.](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037398925), version depuis le 12/09/2018 ; vérifier les formalités du destinataire avant utilisation. Pour un témoignage judiciaire, consulter aussi l’art. 202 CPC : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006410330.
