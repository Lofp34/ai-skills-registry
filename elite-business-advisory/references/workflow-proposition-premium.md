# Workflow Proposition Premium (McKinsey + Bain)

## Objectif
Produire un pack de proposition commerciale premium en une V1 robuste, sans rendu superficiel, avec un niveau de qualite dirigeant.

## Roles
1. Marie (McKinsey): cadrage analytique, problem statement, hypotheses, narration executive.
2. Thomas (Bain): plan d'execution 90 jours, gouvernance, ownership, KPI, quick wins.
3. Laurent: arbitrage final business, langage client, niveau d'engagement et pricing.

## Etape 0 - Ingestion des preuves
### Entrees
- Brief utilisateur.
- Sources factuelles (PDF, MD, verbatims, notes).

### Actions
1. Lire toutes les sources disponibles.
2. Extraire les faits non discutables.
3. Construire une `EvidenceMatrix` minimale.
4. Identifier les hypotheses et les signaler.

### Sorties
- `EvidenceMatrix` initiale.
- Liste des inconnues critiques.

## Etape 1 - Interview duale obligatoire
### Actions Marie
1. Clarifier enjeu business principal.
2. Clarifier ambition et resultat attendu.
3. Clarifier le risque du statu quo.
4. Clarifier le role cible du dirigeant.

### Actions Thomas
1. Clarifier cadence et horizon (J15/J30/J60/J90).
2. Clarifier ownership et roles equipe.
3. Clarifier KPI de pilotage.
4. Clarifier contraintes terrain et capacite d'execution.

### Sorties
- Contrat d'entree complet.
- Hypotheses explicites consignees.

## Etape 2 - Architecture d'offre
### Actions
1. Construire une logique 2 phases: Diagnostic + 90 jours.
2. Definir 2 options max: Premium et Essentiel.
3. Lier chaque option aux resultats attendus et au niveau d'accompagnement.
4. Maintenir forfait fixe.

### Sorties
- Architecture d'offre validee.
- Trame des livrables.

## Etape 3 - Production du pack
### Livrables obligatoires
1. `ProposalDocument`
2. `PlanActionDetaille`
3. `OralScript`
4. `EvidenceMatrix`
5. `DecisionLog`

### Regles de production
1. Garder une coherence stricte entre tous les livrables.
2. Ne pas mentionner IA/agents en externe.
3. Attribuer la mission a Laurent en client-facing.

## Etape 4 - QA gates bloquants
Appliquer les gates de `qa-gates-proposition.md`:
1. Fond strategique.
2. Profondeur operationnelle.
3. Qualite langue FR.
4. Esthetique et pagination PDF.
5. Confidentialite client-facing.

## Etape 5 - Finalisation
### Actions
1. Exporter les versions finales coherentes.
2. Verifier lisibilite dirigeant en lecture 3 minutes.
3. Preparer resume de decision pour soutenance.

### Definition de fin
- Tous les gates sont valides.
- Le client peut repondre en 3 minutes: probleme, methode, resultat, decision.
