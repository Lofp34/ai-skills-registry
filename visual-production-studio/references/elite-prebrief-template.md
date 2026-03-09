# Template de Pré-Brief Stratégique — Cellule M+B (Marie + Thomas)

## Principe

Le pré-brief M+B est le cadrage stratégique obligatoire AVANT l'enquête terrain de Nathalie.

Il sert à :
- structurer le problème,
- expliciter les hypothèses,
- prioriser les leviers,
- préparer un brief terrain plus rapide et plus robuste.

Aucune hypothèse ne devient un fait sans validation terrain.

---

## Structure du Pré-Brief

### 1. Identité de la Demande

| Champ | Contenu |
|---|---|
| **Nom de la mission** | |
| **Client / Prospect** | |
| **Date de cadrage** | |
| **Demande initiale utilisateur** | Citation exacte |
| **Type de mission pressenti** | Formation / Bootcamp / Offre / Parcours client / Vente / Mixte |

### 2. Problématique Structurée (Marie)

| Champ | Contenu |
|---|---|
| **Question directrice** | Formulation claire du problème à résoudre |
| **Arbre de problématique (MECE/Issue Tree)** | 3-5 branches maximum |
| **Hypothèses critiques** | 5 à 10 hypothèses testables |
| **Hypothèses prioritaires à valider terrain** | Top 3 |
| **Ce qui est hors périmètre** | Exclusions explicites |

### 3. Priorisation et Exécution (Thomas)

| Champ | Contenu |
|---|---|
| **Objectifs 30-90 jours** | SMART / Rapid Results |
| **Quick wins proposés** | 3 à 5 actions à faible effort / impact élevé |
| **Chantiers structurants** | 1 à 3 chantiers moyen terme |
| **KPIs de pilotage** | Leading + lagging indicators |
| **Risques opérationnels** | Top 5 + plan de mitigation |

### 4. Grille de Décision

| Champ | Contenu |
|---|---|
| **Options envisagées** | Option A / B / C |
| **Critères de choix** | Impact, effort, délai, risque, faisabilité |
| **Recommandation M+B** | Option recommandée + justification |
| **Niveau de confiance** | Faible / Moyen / Élevé |

### 5. Plan de Validation Terrain pour Nathalie

| Champ | Contenu |
|---|---|
| **Données à collecter en priorité** | CRM, interviews, documents, signaux marché |
| **Questions critiques à poser** | 5 à 10 questions |
| **Évidences attendues** | Preuves minimales pour valider/invalider hypothèses |
| **Seuil de décision pour passer à Philippe** | Conditions explicites de GO |

### 6. Frameworks Mobilisés

| Framework | Fichier source | Pourquoi |
|---|---|---|
| | `../elite-business-advisory/references/framework-*.md` | |

Règles :
- 2 à 6 frameworks maximum
- chaque framework doit être relié à une décision concrète

### 7. Bloc Juridique (Sophie)

| Champ | Contenu |
|---|---|
| **Trigger juridique détecté ?** | Oui / Non |
| **Motif du trigger** | Contrat / RGPD / IP / Responsabilité / Litige / Marché public |
| **Action proposée** | Activer Sophie / Pas d'activation |
| **Validation utilisateur requise** | Oui / Non |

---

## Format de Sortie Recommandé (JSON)

```json
{
  "mission": "",
  "client": "",
  "problem_statement": "",
  "hypotheses": [
    {
      "id": "H1",
      "statement": "",
      "priority": "high|medium|low",
      "validation_status": "to_validate"
    }
  ],
  "quick_wins_30_90": [""],
  "kpis": [
    {
      "name": "",
      "type": "leading|lagging",
      "target": "",
      "horizon": ""
    }
  ],
  "risks": [
    {
      "name": "",
      "severity": "high|medium|low",
      "mitigation": ""
    }
  ],
  "frameworks_used": [
    {
      "name": "",
      "file": "../elite-business-advisory/references/framework-*.md",
      "usage": ""
    }
  ],
  "legal_trigger": {
    "detected": false,
    "reason": "",
    "proposed_action": ""
  }
}
```

---

## Checklist de Qualité M+B

- [ ] Problème formulé en une phrase claire et mesurable
- [ ] Hypothèses structurées et testables
- [ ] Priorisation impact/effort explicite
- [ ] KPIs cibles définis
- [ ] Plan de validation terrain exploitable par Nathalie
- [ ] Frameworks cités avec fichiers source
- [ ] Trigger juridique évalué
