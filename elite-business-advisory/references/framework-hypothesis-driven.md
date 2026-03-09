# Hypothesis-Driven Approach Framework

**Résoudre les problèmes par hypothèses testables**

---

## 📋 Vue d'Ensemble

**Origine :** McKinsey & Company (méthode scientifique appliquée au consulting)
**Usage :** Structurer une analyse en partant d'hypothèses à valider/invalider
**Niveau :** Essentiel - Méthode de travail quotidienne des consultants
**Expert :** Marie Durand (McKinsey)

---

## 🎯 Qu'est-ce que l'Approche Hypothesis-Driven ?

L'approche Hypothesis-Driven (ou "approche par hypothèses") consiste à **formuler des réponses probables AVANT de collecter des données**, puis à tester ces hypothèses méthodiquement.

C'est l'opposé de l'approche "boiling the ocean" (tout analyser avant de conclure).

### Principe Fondamental

> **Ne cherchez pas des données pour trouver une réponse. Formulez une réponse hypothétique, puis cherchez les données pour la valider ou l'invalider.**

### Pourquoi Cette Approche ?

| Approche Classique | Approche Hypothesis-Driven |
|-------------------|---------------------------|
| Collecter toutes les données | Formuler une hypothèse |
| Analyser pendant des semaines | Identifier les données clés |
| Espérer qu'une conclusion émerge | Tester rapidement |
| Risque : Paralysie par l'analyse | Résultat : Réponse en quelques jours |

---

## 🔍 Les 4 Étapes de l'Approche

### 1️⃣ Étape 1 : Structurer le Problème (Issue Tree)

**Objectif :** Décomposer le problème en composantes analysables

**Méthode :**
1. Formuler le problème principal
2. Construire un Issue Tree MECE
3. Identifier les branches prioritaires

**Exemple :**
```
Problème : Pourquoi la marge opérationnelle baisse-t-elle ?
│
├── Les revenus baissent
│   ├── Volume en baisse
│   └── Prix moyen en baisse
│
└── Les coûts augmentent
    ├── Coûts de production
    ├── Coûts commerciaux
    └── Coûts administratifs
```

---

### 2️⃣ Étape 2 : Formuler des Hypothèses

**Objectif :** Transformer chaque branche en hypothèse testable

**Règles d'une bonne hypothèse :**
- **Spécifique** : Pas vague, précise
- **Testable** : On peut la valider/invalider avec des données
- **Actionnable** : Si vraie, on sait quoi faire

**Format standard :**
> "Nous pensons que [cause/solution] parce que [raisonnement initial]"

**Exemple (suite) :**

| Branche | Hypothèse |
|---------|-----------|
| Volume en baisse | "Le volume baisse principalement à cause de la perte de 2 clients majeurs" |
| Prix moyen en baisse | "Le prix moyen baisse car on accorde trop de remises (+15% vs N-1)" |
| Coûts de production | "Les coûts de production ont augmenté de 10% à cause des matières premières" |

---

### 3️⃣ Étape 3 : Concevoir les Tests (Analyses)

**Objectif :** Définir PRÉCISÉMENT ce qu'il faut analyser pour valider/invalider

**Pour chaque hypothèse :**
1. Quelles données sont nécessaires ?
2. Où les trouver ?
3. Quel seuil pour valider/invalider ?

**Format :**
```
Hypothèse : [Énoncé]
Données nécessaires : [Liste]
Source : [Où trouver]
Critère de validation : [Si X alors validé, sinon invalidé]
```

**Exemple :**

| Hypothèse | Données | Source | Critère |
|-----------|---------|--------|---------|
| Perte de 2 clients majeurs | Liste clients perdus + CA associé | CRM + Comptabilité | Si >50% de la baisse → Validé |
| Trop de remises | % remises N vs N-1 | Système facturation | Si hausse >10% → Validé |
| Hausse matières premières | Coûts MP N vs N-1 | Comptabilité achats | Si hausse >8% → Validé |

---

### 4️⃣ Étape 4 : Tester et Itérer

**Objectif :** Exécuter les analyses et conclure

**Process :**
1. Collecter les données identifiées (seulement celles-là)
2. Analyser selon les critères définis
3. Conclure : Hypothèse Validée / Invalidée / À affiner
4. Si invalidée → Formuler nouvelle hypothèse
5. Si validée → Passer aux recommandations

**Exemple de conclusion :**

| Hypothèse | Résultat | Conclusion |
|-----------|----------|------------|
| Perte de 2 clients majeurs | 2 clients perdus = 35% de la baisse | ⚠️ Partiellement validé (pas >50%) |
| Trop de remises | Remises +18% vs N-1 | ✅ Validé |
| Hausse matières premières | MP +3% vs N-1 | ❌ Invalidé |

**Nouvelle hypothèse à tester :**
> "Les 65% restants de la baisse viennent d'une réduction des volumes chez les clients existants"

---

## 📊 Exemple Concret : Consultant Formation

### Contexte
Laurent constate que son taux de conversion (propositions → contrats signés) a chuté de 40% à 25%. Pourquoi ?

### Étape 1 : Issue Tree

```
Pourquoi le taux de conversion a-t-il baissé de 40% à 25% ?
│
├── Qualité des prospects en baisse
│   ├── Prospects moins qualifiés
│   ├── Prospects avec moins de budget
│   └── Prospects pas décisionnaires
│
├── Proposition commerciale moins efficace
│   ├── Offre moins adaptée aux besoins
│   ├── Prix perçu comme trop élevé
│   └── Présentation moins convaincante
│
└── Process de vente dégradé
    ├── Délai de réponse trop long
    ├── Suivi insuffisant
    └── Moins de temps consacré
```

### Étape 2 : Hypothèses Prioritaires

**H1 :** "Le taux de conversion baisse car je reçois plus de prospects via LinkedIn (moins qualifiés) qu'avant (recommandations)"

**H2 :** "Le taux de conversion baisse car mon prix a augmenté de 20% et n'est plus aligné avec la perception de valeur"

**H3 :** "Le taux de conversion baisse car je réponds aux demandes en 5 jours au lieu de 24h"

### Étape 3 : Tests Définis

| Hypothèse | Données | Source | Critère |
|-----------|---------|--------|---------|
| H1 - Source prospects | % prospects LinkedIn vs Recommandations (N vs N-1) | CRM / Notes | Si LinkedIn >50% et conversion LinkedIn <20% → Validé |
| H2 - Prix élevé | Objections "trop cher" dans les refus | Emails / Notes | Si "prix" dans >40% des refus → Validé |
| H3 - Délai réponse | Temps moyen de réponse N vs N-1 | Emails | Si délai moyen >3 jours → Validé |

### Étape 4 : Résultats

| Hypothèse | Données Collectées | Résultat |
|-----------|-------------------|----------|
| H1 | LinkedIn : 60% des prospects (vs 30% N-1), conversion LinkedIn : 15% vs Reco : 55% | ✅ **Validé** |
| H2 | "Trop cher" : 25% des refus | ❌ Invalidé |
| H3 | Délai moyen : 2 jours (vs 1 jour N-1) | ⚠️ Partiellement |

### Conclusion Actionnable

**Cause principale identifiée :** Dégradation de la qualité des prospects (trop de LinkedIn, pas assez de recommandations)

**Recommandations :**
1. Lancer une campagne systématique de demande de recommandations
2. Mieux qualifier les prospects LinkedIn avant d'envoyer une proposition (BANT)
3. Créer un lead magnet pour attirer des prospects plus qualifiés

---

## 📈 Comment Formuler de Bonnes Hypothèses

### La Structure SMART pour Hypothèses

| Critère | Question | Exemple ❌ | Exemple ✅ |
|---------|----------|-----------|-----------|
| **Spécifique** | L'hypothèse est-elle précise ? | "Les clients ne sont pas contents" | "Le NPS a baissé de 45 à 30 à cause du délai de livraison" |
| **Mesurable** | Peut-on la quantifier ? | "On vend moins" | "Le volume a baissé de 20% sur le segment PME" |
| **Actionnable** | Si vraie, sait-on quoi faire ? | "Le marché est difficile" | "On perd des clients face au concurrent X sur le critère prix" |
| **Réaliste** | Est-ce plausible ? | "Tous nos commerciaux sont incompétents" | "Le nouveau process de vente rallonge le cycle de 2 semaines" |
| **Testable** | A-t-on accès aux données ? | "Les clients pensent que..." | "Les avis Google mentionnent le délai dans 60% des cas" |

### Les 3 Sources d'Hypothèses

**1. Intuition / Expérience**
- Que pensez-vous intuitivement ?
- Qu'avez-vous observé ?

**2. Données Préliminaires**
- Que disent les chiffres disponibles ?
- Y a-t-il des tendances visibles ?

**3. Benchmarks / Best Practices**
- Que font les concurrents ?
- Que dit la théorie ?

---

## 💡 Variantes et Astuces

### Variante 1 : Hypothèses en Arborescence

**Quand l'utiliser :** Problèmes complexes avec plusieurs causes possibles.

**Principe :** Créer une hypothèse principale, puis des sous-hypothèses par branche de l'Issue Tree.

### Variante 2 : Test en "Triangulation"

**Quand l'utiliser :** Données incertaines ou biaisées.

**Méthode :** Valider une hypothèse via 3 sources différentes (quant, qual, benchmark).

### Variante 3 : Hypothèse "Kill Switch"

**Quand l'utiliser :** Décisions à fort risque.

**Principe :** Définir un critère qui invalide immédiatement l'option pour éviter de perdre du temps.

---

## 💡 Le "Day One Answer"

### Concept McKinsey

Le **Day One Answer** est la réponse hypothétique que vous formulez **le premier jour** du projet, AVANT toute analyse approfondie.

**Pourquoi c'est puissant :**
- Force à avoir une opinion
- Guide toute l'analyse
- Évite de se disperser

**Format :**
> "Basé sur ce que nous savons aujourd'hui, nous pensons que [réponse]. Les analyses des prochaines semaines viseront à valider cette hypothèse."

**Exemple :**
> "Basé sur les premiers éléments, nous pensons que la baisse de marge vient principalement d'une hausse des remises commerciales (+15%) combinée à une augmentation des coûts de sous-traitance. Nous allons tester ces deux hypothèses cette semaine."

---

## ⚠️ Erreurs Fréquentes

### ❌ Erreur 1 : Hypothèses Non-Testables

**Symptôme :**
> "Les clients ne nous aiment plus"

**Problème :** Impossible à valider/invalider objectivement

**Solution :**
> "Le NPS a baissé de plus de 10 points sur les 6 derniers mois"

---

### ❌ Erreur 2 : Trop d'Hypothèses en Parallèle

**Symptôme :** 15 hypothèses à tester simultanément

**Problème :** Dispersion, aucune conclusion claire

**Solution :** Prioriser 3-5 hypothèses maximum, tester séquentiellement

---

### ❌ Erreur 3 : Biais de Confirmation

**Symptôme :** Chercher uniquement les données qui confirment l'hypothèse

**Problème :** Conclusions fausses, angle mort

**Solution :** Définir à l'avance les critères d'invalidation ET de validation

---

### ❌ Erreur 4 : Hypothèses Trop Vagues

**Symptôme :**
> "Il faut améliorer les ventes"

**Problème :** Ce n'est pas une hypothèse, c'est un objectif

**Solution :**
> "Les ventes peuvent augmenter de 15% en ciblant le segment ETI avec une offre packagée"

---

## ✅ Checklist Hypothesis-Driven

**Structuration :**
- [ ] Le problème est clairement formulé
- [ ] L'Issue Tree est construit (MECE)
- [ ] Les branches prioritaires sont identifiées

**Hypothèses :**
- [ ] 3-5 hypothèses sont formulées
- [ ] Chaque hypothèse est spécifique et testable
- [ ] Le "Day One Answer" est documenté

**Tests :**
- [ ] Les données nécessaires sont identifiées
- [ ] Les sources sont connues et accessibles
- [ ] Les critères de validation/invalidation sont définis

**Exécution :**
- [ ] Les analyses sont focalisées (pas de "boiling the ocean")
- [ ] Les résultats sont documentés (Validé/Invalidé)
- [ ] Les hypothèses invalidées génèrent de nouvelles hypothèses

---

## 💡 Conseil Marie (McKinsey)

> *"L'approche Hypothesis-Driven est ce qui différencie un consultant junior d'un senior. Le junior collecte des tonnes de données et espère qu'une réponse émerge. Le senior formule une réponse dès le jour 1 et utilise les données pour la valider. C'est contre-intuitif mais tellement plus efficace. Mon conseil : osez avoir tort. Une hypothèse invalidée est aussi précieuse qu'une hypothèse validée - elle vous fait avancer."*

---

## 🔗 Frameworks Complémentaires

**Utiliser Hypothesis-Driven avec :**
- **Issue Tree** : Structurer le problème avant de formuler les hypothèses
- **MECE** : S'assurer que les hypothèses couvrent tout le problème
- **Pyramid Principle** : Communiquer les résultats de manière structurée
- **80/20 Rule** : Prioriser les hypothèses à fort impact

---

## 📚 Pour Aller Plus Loin

**Lectures recommandées :**
- "The McKinsey Way" - Ethan M. Rasiel
- "Good Strategy Bad Strategy" - Richard Rumelt

**Outils :**
- Matrice Hypothese / Donnees / Test (tableur)
- Journal des hypotheses (format memo 1 page)

---

**Prochains frameworks :**
- Pyramid Principle
- McKinsey 7S Framework
- Scenario Planning
