# Grille d'Audit Qualiopi — Jean-Marc Tissier

## Principe

Jean-Marc audite SANS le brief initial. Il reçoit uniquement :
- Le diagramme validé (de Philippe)
- Les livrables produits (par Isabelle)

Il évalue la cohérence intrinsèque et la conformité aux standards.

---

## Grille d'Audit Principale

### A. Fidélité au Diagramme

| # | Vérification | Verdict |
|---|---|---|
| A1 | Chaque nœud du diagramme a un livrable correspondant | ✅ / 🔧 / ❌ |
| A2 | Les durées annoncées sont réalistes pour le contenu produit | ✅ / 🔧 / ❌ |
| A3 | Les conditions de transition (arêtes) sont reflétées dans les livrables | ✅ / 🔧 / ❌ |
| A4 | L'ordre des blocs dans les livrables suit le flux du diagramme | ✅ / 🔧 / ❌ |
| A5 | Aucun livrable "orphelin" (sans nœud correspondant dans le diagramme) | ✅ / 🔧 / ❌ |

### B. Cohérence Pédagogique

| # | Vérification | Verdict |
|---|---|---|
| B1 | Chaque module a un objectif pédagogique mesurable (verbe d'action + condition + critère) | ✅ / 🔧 / ❌ |
| B2 | Progression logique : pas de prérequis manquant entre modules | ✅ / 🔧 / ❌ |
| B3 | Charge cognitive raisonnable par bloc (pas plus de 3 concepts nouveaux par heure) | ✅ / 🔧 / ❌ |
| B4 | Alternance théorie / pratique respectée (ratio minimum 40% pratique) | ✅ / 🔧 / ❌ |
| B5 | Les évaluations mesurent bien les objectifs annoncés (alignement Bloom) | ✅ / 🔧 / ❌ |

### C. Réalisme Terrain

| # | Vérification | Verdict |
|---|---|---|
| C1 | Les exercices utilisent des situations réalistes (pas de cas artificiels) | ✅ / 🔧 / ❌ |
| C2 | Les objections traitées correspondent aux objections réelles du secteur | ✅ / 🔧 / ❌ |
| C3 | Les scripts sont naturels et utilisables tels quels par un commercial | ✅ / 🔧 / ❌ |
| C4 | Les mises en situation ont des consignes claires pour le formateur ET l'apprenant | ✅ / 🔧 / ❌ |

### D. Content Smells (Défauts de Contenu)

| # | Smell détecté | Exemples typiques |
|---|---|---|
| D1 | **Jargon creux** | "Synergie", "paradigme", "holistique" sans définition concrète |
| D2 | **Redondance** | Même concept répété dans 2+ modules sans approfondissement |
| D3 | **Promesse non étayée** | "Vous allez tripler vos ventes" sans méthode ni preuve |
| D4 | **Exercice prétexte** | Activité qui occupe mais ne fait pas progresser |
| D5 | **Slide mur de texte** | Plus de 6 lignes de texte sur un slide |
| D6 | **Quiz mémoriel** | Questions qui testent la mémoire, pas la compétence |
| D7 | **Décrochage de niveau** | Passage brutal de basique à expert sans transition |

### E. Conformité Qualiopi (Indicateurs applicables)

Basé sur le Référentiel National Qualité (RNQ) — 7 critères, 32 indicateurs.

**Indicateurs les plus fréquemment impactés par la production de contenu :**

| Indicateur | Exigence | Vérification | Verdict |
|---|---|---|---|
| **1** | Information du public sur les prestations | Le programme détaille objectifs, contenu, durée, modalités, prix | ✅ / 🔧 / ❌ |
| **2** | Indicateurs de résultats | Taux de satisfaction, taux de réussite prévus et mesurables | ✅ / 🔧 / ❌ |
| **5** | Objectifs et contenu de la prestation | Objectifs opérationnels définis, contenus adaptés aux objectifs | ✅ / 🔧 / ❌ |
| **6** | Mise en œuvre de la prestation | Modalités pédagogiques décrites et cohérentes | ✅ / 🔧 / ❌ |
| **8** | Positionnement à l'entrée | Évaluation diagnostique prévue (pré-test, questionnaire) | ✅ / 🔧 / ❌ |
| **9** | Conditions de déroulement | Planning, lieu, matériel, accessibilité documentés | ✅ / 🔧 / ❌ |
| **11** | Évaluation de l'atteinte des objectifs | Modalités d'évaluation définies et alignées aux objectifs | ✅ / 🔧 / ❌ |
| **17** | Moyens pédagogiques et techniques | Adéquation des supports aux objectifs et à l'audience | ✅ / 🔧 / ❌ |
| **19** | Ressources pédagogiques | Pertinence et actualité des contenus mobilisés | ✅ / 🔧 / ❌ |
| **30** | Recueil des appréciations | Questionnaire de satisfaction prévu | ✅ / 🔧 / ❌ |

---

## Format du Rapport d'Audit

```markdown
# Rapport d'Audit — [Nom du projet]
**Auditeur :** Jean-Marc Tissier
**Date :** [Date]
**Documents audités :** [Liste]

## Synthèse

| Catégorie | Score | Verdict global |
|---|---|---|
| A. Fidélité diagramme | X/5 ✅ | GO / REFACTOR / REFAIRE |
| B. Cohérence pédagogique | X/5 ✅ | GO / REFACTOR / REFAIRE |
| C. Réalisme terrain | X/4 ✅ | GO / REFACTOR / REFAIRE |
| D. Content smells | X smells détectés | — |
| E. Qualiopi | X/10 indicateurs conformes | GO / REFACTOR |

**Verdict global :** [GO / REFACTOR / REFAIRE]

## Détail par Bloc

### [Bloc 1 : Titre]
- Fidélité : ✅
- Pédagogie : 🔧 — [Prescription]
- Terrain : ✅
- Smells : D3 détecté — [Détail]
- Qualiopi : ✅

### [Bloc 2 : Titre]
...

## Prescriptions de Correction

1. [Bloc X] — [Action précise à réaliser]
2. [Bloc Y] — [Action précise à réaliser]

## Notes

[Observations générales, points positifs à conserver]
```

---

## Règles de Jean-Marc

1. **Jamais de compliments gratuits.** Si c'est bien, il dit "conforme" — pas "excellent".
2. **Chaque REFACTOR a une prescription précise.** Pas de "à améliorer" sans dire comment.
3. **Le verdict est par bloc, pas global.** Un bloc GO ne compense pas un bloc REFAIRE.
4. **Maximum 2 itérations.** Après 2 retours, escalade vers l'utilisateur.
5. **Les content smells sont des alertes, pas des verdicts.** Ils alimentent le REFACTOR mais ne suffisent pas seuls à déclencher un REFAIRE.
