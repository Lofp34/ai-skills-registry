# RACI Matrix Framework

**Responsible, Accountable, Consulted, Informed**

---

## 📋 Vue d'Ensemble

**Origine :** Méthode de gestion de projet, popularisée par Bain & Company  
**Usage :** Clarifier les rôles et responsabilités pour éviter confusion et conflits  
**Niveau :** Essentiel - À créer pour tout projet/processus  
**Expert :** Thomas Bernard (Bain)

---

## 🎯 Qu'est-ce que RACI ?

RACI est une **matrice de responsabilités** qui définit clairement qui fait quoi dans un projet ou un processus.

### Les 4 Rôles RACI

| Rôle | Signification | Description | Nombre par tâche |
|------|---------------|-------------|------------------|
| **R** | **Responsible** (Responsable) | Celui qui **FAIT** le travail | 1 ou plusieurs |
| **A** | **Accountable** (Autorité/Approbateur) | Celui qui **VALIDE** et assume la responsabilité finale | **1 SEUL** (règle d'or) |
| **C** | **Consulted** (Consulté) | Celui dont on demande l'**AVIS** (communication bidirectionnelle) | 0 ou plusieurs |
| **I** | **Informed** (Informé) | Celui qui est **TENU INFORMÉ** (communication unidirectionnelle) | 0 ou plusieurs |

---

## 📊 Structure d'une Matrice RACI

### Format Standard

```
          │ Personne 1 │ Personne 2 │ Personne 3 │ Personne 4
══════════╪════════════╪════════════╪════════════╪════════════
Tâche 1   │     R      │     A      │     C      │     I
Tâche 2   │     C      │     R      │     A      │     I
Tâche 3   │     I      │     I      │     R      │     A
```

---

## 🎯 Exemple Concret : Projet Formation Commerciale

### Contexte
Laurent doit livrer une formation pour ID Solutions. Voici la RACI :

| Activité | Laurent (Prestataire) | Christelle (DRH) | Maxime (Participant) | Manager Commercial |
|----------|----------------------|------------------|---------------------|-------------------|
| **Signature convention** | C | **A** | I | I |
| **Définition besoins formation** | R | C | C | **A** |
| **Conception formation** | R, **A** | I | C | I |
| **Validation contenu** | R | C | I | **A** |
| **Animation formation** | R, **A** | I | R (participe) | C |
| **Validation acquis** | C | I | R | **A** |
| **Coaching post-formation** | R, **A** | I | R (bénéficiaire) | C |
| **Paiement facture** | I | **A** | I | I |

### Lecture de la Matrice

**Ligne "Conception formation" :**
- **Laurent = R, A** : Il fait ET valide (car prestataire expert)
- **Christelle = I** : Juste informée du contenu
- **Maxime = C** : Son avis est demandé (ses besoins)
- **Manager = I** : Juste informé

---

## 🔍 Les 4 Rôles en Détail

### 1️⃣ R = Responsible (Celui qui FAIT)

**Définition :** La ou les personne(s) qui **exécutent** la tâche

**Questions :**
- Qui fait le travail ?
- Qui est dans l'action ?
- Qui produit le livrable ?

**Caractéristiques :**
- ✅ Peut être plusieurs personnes (équipe)
- ✅ Peut être la même personne que A (si c'est un expert)
- ❌ Ne peut PAS être vide (sinon personne ne fait rien !)

**Exemple :**
- Tâche : "Rédiger la proposition commerciale"
- R = Le consultant (Laurent)

---

### 2️⃣ A = Accountable (Celui qui VALIDE)

**Définition :** La personne qui **approuve** et assume la responsabilité finale

**Questions :**
- Qui a le dernier mot ?
- Qui valide que c'est bien fait ?
- Qui sera tenu responsable si ça échoue ?

**Caractéristiques :**
- ✅ **1 SEUL par tâche** (règle d'or absolue)
- ✅ C'est souvent le manager ou le sponsor
- ❌ Ne JAMAIS avoir 2 A (sinon conflit de décision)

**Exemple :**
- Tâche : "Valider le budget formation"
- A = La DRH (Christelle) - elle seule décide

**⚠️ RÈGLE D'OR RACI :**
> **Un seul A par ligne. Toujours. Sans exception.**

Si vous avez 2 A, c'est que :
- Soit vous devez décomposer la tâche en 2 sous-tâches
- Soit vous devez clarifier qui a vraiment le pouvoir de décision

---

### 3️⃣ C = Consulted (Celui dont on demande l'AVIS)

**Définition :** Les personnes consultées **AVANT** de prendre une décision (communication bidirectionnelle)

**Questions :**
- De qui ai-je besoin de l'avis ?
- Qui doit donner son expertise ?
- Qui peut bloquer ou faire échouer si on ne le consulte pas ?

**Caractéristiques :**
- ✅ Communication bidirectionnelle (dialogue)
- ✅ Leur avis compte (même s'il n'est pas décisionnel)
- ⚠️ À limiter (trop de C = réunionite aiguë)

**Exemple :**
- Tâche : "Définir le contenu de la formation"
- C = Le manager commercial (il donne son avis sur ce qui est pertinent)
- C = Maxime (il exprime ses besoins)

---

### 4️⃣ I = Informed (Celui qui est INFORMÉ)

**Définition :** Les personnes tenues informées **APRÈS** que la décision est prise (communication unidirectionnelle)

**Questions :**
- Qui doit être au courant ?
- Qui sera impacté par cette décision ?
- Qui a besoin de savoir pour faire son travail ?

**Caractéristiques :**
- ✅ Communication unidirectionnelle (on les informe, ils ne donnent pas d'avis)
- ✅ Pas de pouvoir de décision ou de blocage
- ⚠️ À limiter aussi (trop de I = info overload)

**Exemple :**
- Tâche : "Signer le contrat de formation"
- I = Maxime (il est juste informé que c'est signé)

---

## 📈 Comment Créer une Matrice RACI

### Étape 1 : Lister les Activités/Tâches (lignes)

**Décomposer le projet en tâches clés**

Pour un projet de formation :
1. Définition des besoins
2. Rédaction de la proposition
3. Signature du contrat
4. Conception pédagogique
5. Animation de la formation
6. Évaluation des acquis
7. Coaching post-formation
8. Facturation et paiement

**Astuce :** Ni trop détaillé (pas 50 lignes), ni trop macro (pas 3 lignes)  
**Idéal :** 8-15 tâches clés

---

### Étape 2 : Lister les Acteurs (colonnes)

**Identifier toutes les parties prenantes**

Pour un projet de formation :
- Laurent (Prestataire formateur)
- Christelle (DRH, sponsor)
- Maxime (Participant)
- Manager commercial (Utilisateur final)
- Service comptabilité (Paiement)

---

### Étape 3 : Remplir la Matrice

**Pour chaque cellule, se poser :**
- Cette personne fait-elle cette tâche ? → R
- Cette personne valide-t-elle ? → A
- Doit-on consulter son avis ? → C
- Doit-on juste l'informer ? → I
- Aucun rôle ? → Laisser vide

**⚠️ Vérifier pour chaque ligne :**
- [ ] Il y a au moins 1 R (sinon personne ne fait)
- [ ] Il y a exactement 1 A (ni 0, ni 2)
- [ ] Les C sont limités (< 3-4 max)
- [ ] Les I sont limités (ne pas spammer tout le monde)

---

### Étape 4 : Valider avec les Parties Prenantes

**Organiser une réunion de validation RACI**

Passer en revue chaque ligne :
- "Pour cette tâche, on est d'accord que c'est toi qui fais (R) ?"
- "Et c'est bien toi qui valides (A) ?"
- "On vous consulte vous deux (C), ça vous va ?"

**Bénéfice :** Tout le monde sait qui fait quoi, plus de confusion !

---

## ⚠️ Erreurs Fréquentes

### ❌ Erreur 1 : Plusieurs A pour une même tâche

**Symptôme :**
```
Tâche : Valider le budget
Laurent = A
Christelle = A
```

**Problème :** Qui décide vraiment ? Conflit assuré.

**Solution :** Clarifier qui a le dernier mot
```
Laurent = R (fait la proposition)
Christelle = A (valide seule)
```

---

### ❌ Erreur 2 : Trop de C (tout le monde consulté)

**Symptôme :**
```
Tâche : Conception formation
5 personnes en C
```

**Problème :** Réunionite, lenteur, paralysie décisionnelle

**Solution :** Limiter à 2-3 C maximum, les autres en I

---

### ❌ Erreur 3 : Pas de R (personne ne fait)

**Symptôme :**
```
Tâche : Rédiger le rapport
Tout le monde en A, C ou I, mais pas de R
```

**Problème :** Personne ne fait le travail !

**Solution :** Désigner explicitement qui FAIT

---

### ❌ Erreur 4 : Confondre C et I

**C = Consulté** → Communication bidirectionnelle, AVANT la décision  
**I = Informé** → Communication unidirectionnelle, APRÈS la décision

**Exemple :**
- Si vous envoyez juste un email "FYI" → I
- Si vous demandez l'avis dans une réunion → C

---

## 💡 Variantes de RACI

### RACI-VS (avec Vérificateur et Signataire)

| Rôle | Description |
|------|-------------|
| R | Responsible (fait) |
| A | Accountable (valide) |
| C | Consulted (avis demandé) |
| I | Informed (juste informé) |
| **V** | **Verify** (vérifie la qualité) |
| **S** | **Sign** (signe formellement) |

**Utilité :** Projets avec processus qualité strict

---

### RASCI (avec Supporteur)

| Rôle | Description |
|------|-------------|
| R | Responsible |
| A | Accountable |
| **S** | **Support** (aide le R) |
| C | Consulted |
| I | Informed |

---

## 🎯 RACI pour Processus Récurrents

### Exemple : Processus de Vente

| Étape du Process | Commercial | Manager | Juridique | Finance |
|------------------|------------|---------|-----------|---------|
| Prospection | R, A | I | - | - |
| Qualification (BANT) | R, A | C | - | - |
| Proposition commerciale | R | A | C | I |
| Négociation contrat | R | C | A (clauses) | C (prix) |
| Signature | C | I | C | I (Client = A) |
| Facturation | I | I | - | R, A |

---

## ✅ Checklist RACI

Avant de valider votre matrice RACI :

**Pour chaque LIGNE (tâche) :**
- [ ] Il y a au moins 1 **R** (quelqu'un fait le travail)
- [ ] Il y a exactement 1 **A** (un seul décideur)
- [ ] Les **C** sont limités (< 4 personnes)
- [ ] Les **I** sont pertinents (pas de spam)

**Pour chaque COLONNE (personne) :**
- [ ] La charge de travail est équilibrée (pas trop de R pour une personne)
- [ ] Les rôles sont cohérents avec le poste/niveau

**Globalement :**
- [ ] La matrice a été validée par toutes les parties prenantes
- [ ] Elle est accessible et partagée (dans un doc projet)
- [ ] Elle sera mise à jour si les rôles changent

---

## 💡 Conseil Thomas (Bain)

> *"Chez Bain, on crée une RACI pour CHAQUE projet client. Règle simple : Si tu ne sais pas qui est le A d'une tâche, tu vas avoir des problèmes. La RACI n'est pas de la bureaucratie, c'est de la clarté. Et la clarté accélère l'exécution. Pas de RACI = meetings interminables + conflits de territoire."*

---

## 🔗 Frameworks Complémentaires

**Utiliser RACI avec :**
- **Critical Path Method** : Identifier qui fait les tâches critiques
- **SMART Goals** : Clarifier les objectifs de chaque R
- **Issue Tree** : Décomposer les tâches pour la RACI

---

## 📚 Pour Aller Plus Loin

**Templates :**
- Template RACI Excel (à créer)
- Template RACI PowerPoint (présentation)

**Outils :**
- Monday.com, Asana, Trello (avec colonnes RACI)
- Excel/Google Sheets (version simple)

---

**Prochains frameworks :**
- SMART Goals (définir des objectifs clairs)
- Critical Path Method (identifier les tâches critiques)
- Gantt Chart (planification projet)