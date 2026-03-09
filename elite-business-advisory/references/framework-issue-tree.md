# Issue Tree Framework

**Décomposition structurée de problèmes complexes**

---

## 📋 Vue d'Ensemble

**Origine :** McKinsey & Company (années 1960-70)
**Usage :** Décomposer un problème complexe en sous-problèmes gérables et actionnables
**Niveau :** Essentiel - Base de toute analyse structurée
**Expert :** Marie Durand (McKinsey)

---

## 🎯 Qu'est-ce qu'un Issue Tree ?

Un Issue Tree (arbre des problèmes) est une **représentation visuelle hiérarchique** qui décompose un problème principal en sous-problèmes de plus en plus spécifiques, jusqu'à atteindre des éléments analysables et actionnables.

C'est l'outil fondamental de la **pensée structurée McKinsey**. Avant de résoudre un problème, il faut le comprendre. Et pour le comprendre, il faut le **décomposer**.

### Principe Fondamental

> **Un problème complexe = Somme de problèmes simples**

### Structure Visuelle

```
                    ┌─────────────────┐
                    │ PROBLÈME        │
                    │ PRINCIPAL       │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │ Sous-       │   │ Sous-       │   │ Sous-       │
    │ problème 1  │   │ problème 2  │   │ problème 3  │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                 │                 │
      ┌────┼────┐       ┌────┼────┐       ┌────┼────┐
      │    │    │       │    │    │       │    │    │
     1.1  1.2  1.3     2.1  2.2  2.3     3.1  3.2  3.3
```

---

## 🔍 Les 2 Types d'Issue Trees

### 1️⃣ Diagnostic Tree (Arbre de Diagnostic)

**Usage :** Comprendre POURQUOI un problème existe

**Question clé :** "Pourquoi avons-nous ce problème ?"

**Structure :** Causes → Sous-causes → Facteurs

**Exemple :**
```
Pourquoi le CA baisse-t-il ?
├── Volume des ventes en baisse
│   ├── Moins de nouveaux clients
│   │   ├── Prospection insuffisante
│   │   ├── Taux de conversion faible
│   │   └── Marché en contraction
│   └── Clients existants achètent moins
│       ├── Satisfaction en baisse
│       ├── Concurrence plus agressive
│       └── Réduction budgets clients
└── Prix moyen en baisse
    ├── Remises plus fréquentes
    ├── Mix produit défavorable
    └── Pression concurrentielle
```

---

### 2️⃣ Solution Tree (Arbre de Solutions)

**Usage :** Identifier COMMENT résoudre le problème

**Question clé :** "Comment pouvons-nous résoudre ce problème ?"

**Structure :** Options → Sous-options → Actions

**Exemple :**
```
Comment augmenter le CA de 20% ?
├── Augmenter le volume de ventes
│   ├── Acquérir plus de clients
│   │   ├── Intensifier la prospection
│   │   ├── Améliorer le taux de conversion
│   │   └── Lancer campagne marketing
│   └── Vendre plus aux clients existants
│       ├── Cross-sell / Up-sell
│       ├── Programme de fidélité
│       └── Réduire le churn
└── Augmenter le prix moyen
    ├── Réviser la politique tarifaire
    ├── Réduire les remises
    └── Pousser les offres premium
```

---

## 📊 Exemple Concret : Consultant Formation

### Contexte
Laurent est consultant formation. Son objectif : atteindre 150K€ de CA cette année. Actuellement à 80K€. Comment atteindre l'objectif ?

### Issue Tree (Solution Tree)

```
Comment atteindre 150K€ de CA (vs 80K€ actuels) ?
│
├── 1. AUGMENTER LE NOMBRE DE MISSIONS
│   │
│   ├── 1.1 Acquérir plus de nouveaux clients
│   │   ├── 1.1.1 Prospecter activement (LinkedIn, email)
│   │   ├── 1.1.2 Demander des recommandations
│   │   ├── 1.1.3 Participer à des événements sectoriels
│   │   └── 1.1.4 Publier du contenu expert
│   │
│   ├── 1.2 Augmenter le taux de conversion
│   │   ├── 1.2.1 Améliorer les propositions commerciales
│   │   ├── 1.2.2 Mieux qualifier les prospects (BANT)
│   │   └── 1.2.3 Réduire le cycle de vente
│   │
│   └── 1.3 Fidéliser les clients existants
│       ├── 1.3.1 Proposer des missions récurrentes
│       ├── 1.3.2 Offrir du coaching post-formation
│       └── 1.3.3 Créer un programme de suivi annuel
│
└── 2. AUGMENTER LE REVENU PAR MISSION
    │
    ├── 2.1 Augmenter les prix
    │   ├── 2.1.1 Valoriser mieux l'expertise (références)
    │   ├── 2.1.2 Créer des offres premium
    │   └── 2.1.3 Réduire les remises accordées
    │
    ├── 2.2 Vendre des offres plus complètes
    │   ├── 2.2.1 Packager formation + coaching
    │   ├── 2.2.2 Ajouter des outils/templates
    │   └── 2.2.3 Proposer du suivi post-formation
    │
    └── 2.3 Cibler des clients plus gros
        ├── 2.3.1 Viser les ETI et grands comptes
        ├── 2.3.2 Répondre aux appels d'offres
        └── 2.3.3 Développer des partenariats
```

### Analyse

**Niveau 1 :** 2 leviers principaux (Volume × Prix)
**Niveau 2 :** 6 sous-leviers
**Niveau 3 :** 18 actions concrètes

**Quick-wins identifiés :**
- 1.1.2 Demander des recommandations (effort faible, impact fort)
- 1.3.1 Proposer des missions récurrentes (client déjà convaincu)
- 2.1.3 Réduire les remises (0 effort, impact immédiat)

---

## 📈 Comment Construire un Issue Tree

### Étape 1 : Formuler le Problème Principal

**Règles pour bien formuler :**
- Être **spécifique** (pas vague)
- Être **mesurable** si possible
- Commencer par "Pourquoi" (diagnostic) ou "Comment" (solution)

**❌ Mauvais :**
- "Les ventes ne vont pas bien"
- "Il faut améliorer les choses"

**✅ Bon :**
- "Pourquoi le taux de conversion a-t-il baissé de 30% à 20% ?"
- "Comment augmenter le CA de 80K€ à 150K€ en 12 mois ?"

---

### Étape 2 : Identifier les Branches Principales (Niveau 1)

**Méthode MECE obligatoire :**
- **Mutuellement Exclusives** : Pas de chevauchement entre branches
- **Collectivement Exhaustives** : Couvrir toutes les possibilités

**Patterns courants pour le Niveau 1 :**

| Problème | Décomposition MECE |
|----------|-------------------|
| Augmenter le CA | Volume × Prix |
| Améliorer la rentabilité | Revenus - Coûts |
| Réduire les coûts | Coûts fixes + Coûts variables |
| Augmenter la productivité | Temps × Efficacité |
| Conquérir un marché | Clients actuels + Nouveaux clients |

---

### Étape 3 : Décomposer Chaque Branche (Niveaux 2, 3...)

**Continuer jusqu'à atteindre des éléments :**
- **Analysables** : On peut trouver des données
- **Actionnables** : On peut prendre une décision

**Règle des 3-5 branches :**
- Chaque niveau devrait avoir 3 à 5 sous-branches
- Moins de 3 → Trop vague, décomposer davantage
- Plus de 5 → Trop détaillé, regrouper

---

### Étape 4 : Vérifier la Logique MECE

**Pour chaque niveau, vérifier :**

**Test d'exclusivité mutuelle :**
> "Si je résous la branche A, est-ce que ça résout aussi la branche B ?"
> Si oui → Chevauchement → Restructurer

**Test d'exhaustivité :**
> "Y a-t-il une solution/cause possible qui n'est dans aucune branche ?"
> Si oui → Branche manquante → Ajouter

---

### Étape 5 : Prioriser les Branches

**Utiliser l'Impact-Effort Matrix :**
- Évaluer chaque branche finale (Impact + Effort)
- Identifier les Quick-Wins
- Planifier les Major Projects

---

## 💡 Variantes et Astuces

### Variante 1 : Driver Tree (Arbre des Leviers)

**Quand l'utiliser :** Pour les objectifs quantitatifs (CA, marge, conversions).

**Principe :** Décomposer un KPI en facteurs multiplicatifs.

**Exemple :**
```
CA = Nombre de clients × Panier moyen × Fréquence d'achat
```

### Variante 2 : Arbre Hybride (Diagnostic → Solution)

**Quand l'utiliser :** Quand il faut passer rapidement du "pourquoi" au "comment".

**Méthode :**
1. Construire l'arbre de diagnostic
2. Pour chaque cause prioritaire, créer un sous-arbre de solutions

### Variante 3 : Arbre à 80/20

**Quand l'utiliser :** En phase d'exploration rapide.

**Principe :** Aller seulement jusqu'au niveau qui explique 80% du problème, puis approfondir uniquement ces branches.

---

## 💡 Patterns d'Issue Trees Fréquents

### Pattern 1 : Revenus

```
Augmenter les revenus
├── Augmenter le volume
│   ├── Plus de clients
│   └── Plus d'achats par client
└── Augmenter le prix unitaire
    ├── Prix catalogue
    └── Réduire remises
```

### Pattern 2 : Profitabilité

```
Améliorer la profitabilité
├── Augmenter les revenus
│   └── [voir Pattern 1]
└── Réduire les coûts
    ├── Coûts fixes
    │   ├── Loyer
    │   ├── Salaires fixes
    │   └── Abonnements
    └── Coûts variables
        ├── Matières premières
        ├── Sous-traitance
        └── Commissions
```

### Pattern 3 : Taux de Conversion

```
Améliorer le taux de conversion
├── Améliorer la qualité des leads
│   ├── Meilleur ciblage
│   ├── Meilleure qualification (BANT)
│   └── Sources de leads plus qualitatives
└── Améliorer le processus de vente
    ├── Proposition de valeur plus claire
    ├── Réduire les frictions
    └── Améliorer le closing
```

### Pattern 4 : Satisfaction Client

```
Améliorer la satisfaction client
├── Améliorer le produit/service
│   ├── Qualité
│   ├── Fonctionnalités
│   └── Fiabilité
├── Améliorer l'expérience
│   ├── Avant-vente
│   ├── Achat
│   └── Après-vente
└── Améliorer la relation
    ├── Réactivité
    ├── Personnalisation
    └── Communication
```

---

## ⚠️ Erreurs Fréquentes

### ❌ Erreur 1 : Branches Non-MECE

**Symptôme :**
```
Augmenter le CA
├── Vendre plus
├── Acquérir des clients
└── Augmenter les prix
```

**Problème :** "Vendre plus" et "Acquérir des clients" se chevauchent

**Solution :**
```
Augmenter le CA
├── Volume (nombre de ventes)
│   ├── Nouveaux clients
│   └── Clients existants
└── Prix (valeur par vente)
```

---

### ❌ Erreur 2 : Aller Trop Profond Trop Vite

**Symptôme :** Issue tree avec 6+ niveaux dès le départ

**Problème :** Perte de vue d'ensemble, paralysie par l'analyse

**Solution :** Commencer à 2-3 niveaux, approfondir uniquement les branches prioritaires

---

### ❌ Erreur 3 : Mélanger Diagnostic et Solution

**Symptôme :**
```
Pourquoi le CA baisse ?
├── Manque de prospection → Prospecter plus
├── Prix trop élevés → Baisser les prix
```

**Problème :** Mélange causes et solutions dans le même arbre

**Solution :** Faire DEUX arbres séparés :
1. Diagnostic Tree : Identifier les causes
2. Solution Tree : Identifier les solutions pour chaque cause

---

### ❌ Erreur 4 : Branches Trop Vagues

**Symptôme :**
```
Comment augmenter le CA ?
├── Améliorer les ventes
├── Être plus efficace
└── Mieux communiquer
```

**Problème :** Impossible à analyser ou à actionner

**Solution :** Chaque branche doit être spécifique et mesurable

---

## ✅ Checklist Issue Tree

**Formulation du problème :**
- [ ] Le problème est spécifique (pas vague)
- [ ] Le problème est mesurable (objectif chiffré)
- [ ] Le type d'arbre est choisi (Diagnostic ou Solution)

**Structure MECE :**
- [ ] Les branches sont mutuellement exclusives
- [ ] Les branches sont collectivement exhaustives
- [ ] Chaque niveau a 3-5 branches

**Profondeur :**
- [ ] L'arbre a 2-4 niveaux (pas plus)
- [ ] Les branches finales sont analysables
- [ ] Les branches finales sont actionnables

**Priorisation :**
- [ ] Les branches ont été évaluées (impact/effort)
- [ ] Les Quick-Wins sont identifiés
- [ ] Un plan d'action est défini

---

## 💡 Conseil Marie (McKinsey)

> *"L'Issue Tree est le premier outil que j'enseigne à tout nouveau consultant McKinsey. C'est la base de tout. Avant de chercher des données, avant de faire des recommandations, on construit l'arbre. Un bon Issue Tree, c'est 50% du travail fait. La clé ? Être MECE à chaque niveau. Si votre arbre n'est pas MECE, vos conclusions seront bancales. Prenez le temps de bien structurer avant de foncer."*

---

## 🔗 Frameworks Complémentaires

**Utiliser Issue Tree avec :**
- **MECE** : Garantir la structure logique de chaque niveau
- **Hypothesis-Driven Approach** : Transformer les branches en hypothèses testables
- **Pyramid Principle** : Communiquer les conclusions de l'analyse
- **Impact-Effort Matrix** : Prioriser les branches identifiées

---

## 📚 Pour Aller Plus Loin

**Lectures recommandées :**
- "The McKinsey Mind" - Ethan M. Rasiel
- "Problem Solving 101" - Ken Watanabe

**Outils :**
- Tableur avec indentation automatique pour construire l'arbre
- Whiteboard (Miro, FigJam) pour itérer rapidement

---

**Prochains frameworks :**
- Hypothesis-Driven Approach
- Pyramid Principle
- 80/20 Rule (Pareto)
