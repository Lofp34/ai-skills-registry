# Guide d'Interview - Marie (McKinsey) + Thomas (Bain)

## Usage
Mener cette interview avant toute redaction de proposition.

## Questions obligatoires - Marie (cadrage strategique)
1. Quel est l'objectif business prioritaire a atteindre dans les 90 prochains jours?
2. Quel est le risque concret si rien ne change dans les 3 a 6 mois?
3. Quels faits confirment ce diagnostic aujourd'hui?
4. Quel niveau d'implication dirigeant est souhaite en cible?
5. Sur quels sujets le dirigeant doit-il absolument se concentrer (strategie, pilotage, croissance)?
6. Quels sujets operationnels doivent etre delegues?
7. Quelles hypotheses critiques doivent etre validees pendant la phase diagnostic?

## Questions obligatoires - Thomas (execution operationnelle)
1. Quelle cadence de pilotage est realiste (hebdo, mensuelle, gates)?
2. Qui porte chaque chantier operationnel?
3. Quels KPI pilotent la progression (activite, conversion, cycle, mix, adoption)?
4. Quels quick wins sont attendus sous 30 jours?
5. Quelles contraintes terrain peuvent freiner l'execution (charge, outils, competences)?
6. Quel niveau de structuration CRM/Odoo est en place aujourd'hui?
7. Quel signal prouvera que la mission cree de la valeur a J15, J30, J60, J90?

## Questions de cadrage commercial
1. Quel niveau de profondeur est attendu: premium detaille ou concis premium?
2. Quelles contraintes client-facing sont non negociables?
3. Quelle enveloppe de prix cible et quelles options presenter?
4. Qui valide la proposition finale?

## Sortie obligatoire de l'interview
Produire un bloc `ContratEntree` avec:
- `objectif_business`
- `donnees_sources`
- `niveau_profondeur`
- `contraintes_client_facing`
- `horizon_execution`

## Regle de gestion des manques
1. Si une reponse manque, poser une hypothese explicite.
2. Inscrire l'hypothese dans le `DecisionLog`.
3. Marquer la condition de revalidation.
