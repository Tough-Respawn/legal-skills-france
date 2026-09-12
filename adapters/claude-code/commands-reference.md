## Commands Reference

The following slash commands are available. Template selection follows the Response Protocol (command > role > request nature):

| Command | Domain | Description |
|---------|--------|-------------|
| `/droit <question>` | Auto-detected | Main entry point : routes to the right domain automatically |
| `/jurisprudence <search>` | Cross-cutting | Case law research : always uses Recherche de jurisprudence template |
| `/droit-civil <question>` | Civil | Contracts, liability, property, family, inheritance |
| `/droit-penal <question>` | Criminal | Offenses, penalties, criminal procedure |
| `/droit-travail <question>` | Labor | Employment, dismissal, collective bargaining |
| `/droit-affaires <question>` | Business | Companies, commercial law, IP, competition |
| `/droit-administratif <question>` | Administrative | Public administration, administrative courts |
| `/droit-numerique <question>` | Digital | GDPR/RGPD, CNIL, data protection, e-commerce |
| `/droit-europeen <question>` | EU | Treaties, directives, regulations, CJEU |

**Template mapping:** `/jurisprudence` always triggers the Recherche de jurisprudence template. All other commands select the template based on the detected user role (lawyer → Consultation juridique, student → Cas pratique, citizen → Explication vulgarisée, business → Analyse de document if a document is provided, otherwise Consultation juridique).

---
