# Critical Path Method Framework

**Identifier les taches critiques d'un projet**

---

## 📋 Vue d'Ensemble

**Origine :** DuPont / CPM (1950s)
**Usage :** Planifier un projet et reduire les delais
**Niveau :** Avance - Pilotage de projets complexes
**Expert :** Thomas Bernard (Bain)

---

## 🎯 Qu'est-ce que le Critical Path Method ?

Le CPM identifie la **sequence de taches qui determine la duree minimale** d'un projet. Toute tache sur le chemin critique, si elle derape, **retarde le projet entier**.

### Principe Fondamental

> **Le chemin critique est la chaine sans marge.**

---

## 🔍 Les 4 Etapes

### 1️⃣ Lister les taches

**Question cle :** Quelles taches composent le projet ?

**Ce qu'on cherche :**
- Taches principales
- Dependencies

**Exemples :**
- ✅ Design -> Dev -> Test -> Deploiement

---

### 2️⃣ Estimer les durees

**Question cle :** Combien de temps par tache ?

**Ce qu'on cherche :**
- Estimation realiste
- Duree en jours

---

### 3️⃣ Construire le reseau

**Question cle :** Dans quel ordre executer ?

**Ce qu'on cherche :**
- Diagramme reseau
- Chemins possibles

---

### 4️⃣ Identifier le chemin critique

**Question cle :** Quelle sequence est la plus longue ?

**Ce qu'on cherche :**
- Duree totale
- Marges (slack)

---

## 📊 Exemple Concret : Lancement d'une offre

### Contexte
Projet de 8 semaines.

| Tache | Duree | Dependances |
|------|-------|------------|
| A. Design | 2 | - |
| B. Dev | 3 | A |
| C. Tests | 2 | B |
| D. Marketing | 2 | A |
| E. Lancement | 1 | C, D |

Chemin critique : A -> B -> C -> E = 8 semaines.

---

## 📈 Comment Utiliser CPM ?

### Etape 1 : Cartographier le projet

**Methode :** Liste de taches + dependances.

**Astuce :** Niveau de detail suffisant, pas micro.

---

### Etape 2 : Construire le reseau

**Methode :** Diagramme simple (Gantt + dependances).

**Astuce :** Utiliser un outil simple (Excel, Asana).

---

### Etape 3 : Calculer le chemin critique

**Methode :** Chemin le plus long.

**Astuce :** Toute tache critique doit etre surveillee.

---

### Etape 4 : Optimiser

**Methode :** Reduire les taches critiques (crashing).

**Astuce :** Ajouter ressources sur ces taches seulement.

---

## 💡 Variantes et Astuces

### Variante 1 : PERT + CPM

**Quand l'utiliser :** Durees incertaines.

**Principe :** Ajouter estimation optimiste/pessimiste.

### Variante 2 : Chemins paralleles

**Quand l'utiliser :** Gros projets.

**Principe :** Identifier plusieurs chemins critiques.

### Variante 3 : CPM + RACI

**Quand l'utiliser :** Equipes multi-acteurs.

**Principe :** Lier chaque tache critique a un owner.

---

## ⚠️ Erreurs Frequentes / Pieges a Eviter

### ❌ Erreur 1 : Sous-estimer les durees

**Symptome :** Retards en cascade.

**Probleme :** Chemin critique faux.

**Solution :** Estimations realistes + buffer.

---

### ❌ Erreur 2 : Ignorer les dependances

**Symptome :** Planning incoherent.

**Probleme :** Taches executes trop tot.

**Solution :** Clarifier toutes les dependances.

---

### ❌ Erreur 3 : Ne pas suivre le chemin critique

**Symptome :** Focus sur des taches non critiques.

**Probleme :** Retard global.

**Solution :** Revue hebdo des taches critiques.

---

## ✅ Checklist CPM

**Preparation :**
- [ ] Liste des taches et dependances
- [ ] Durees estimees

**Analyse :**
- [ ] Chemin critique identifie
- [ ] Marges calculees

**Execution :**
- [ ] Owners des taches critiques
- [ ] Suivi hebdo

---

## 💡 Conseil Thomas (Bain)

> *"Le CPM vous dit ou agir. Si vous devez accelerer, n'ajoutez pas des ressources partout. Ajoutez-les sur le chemin critique."*

---

## 🔗 Frameworks Complementaires

**Utiliser CPM avec :**
- **GROW Model** : Suivi et coaching
- **RACI** : Responsabilites
- **Results Delivery** : Execution
- **Agile/Scrum** : Iterations rapides

---

## 📚 Pour Aller Plus Loin

**Lectures recommandees :**
- "Project Management" - Kerzner
- "Critical Path Method" - Kelley

**Outils :**
- Diagramme de reseau
- Gantt avec dependances

---

**Prochains frameworks :**
- Agile/Scrum
- Lean Methodology
- Kaizen
