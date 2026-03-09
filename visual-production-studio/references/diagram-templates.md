# Templates de Diagrammes — Philippe Grandval

## Règles Générales

- Chaque nœud contient : ID, nom, durée, format, objectif
- Les arêtes portent les conditions de transition
- Les couleurs codent le type : 🟦 contenu / 🟩 exercice / 🟨 évaluation / 🟥 décision
- Toujours inclure un nœud START et un nœud END
- Maximum 15 nœuds par diagramme (sinon découper en sous-diagrammes)

---

## 1. Parcours Apprenant (Bootcamp / Formation)

```mermaid
graph TD
    START([🎯 Début du parcours]) --> DIAG[📋 Diagnostic initial<br/>30min - Quiz - Évaluer le niveau]
    DIAG -->|Niveau identifié| M1[📚 Module 1: Titre<br/>2h - Présentiel - Objectif]
    M1 --> EX1[🎯 Exercice 1: Titre<br/>45min - Mise en situation - Objectif]
    EX1 --> M2[📚 Module 2: Titre<br/>2h - Présentiel - Objectif]
    M2 --> EX2[🎯 Exercice 2: Titre<br/>1h - Role-play - Objectif]
    EX2 --> EVAL[📝 Évaluation finale<br/>30min - Quiz + Cas - Mesurer acquis]
    EVAL -->|Score ≥ 70%| CERT([✅ Certification])
    EVAL -->|Score < 70%| REMEDIATION[🔄 Remédiation<br/>1h - Tutorat - Renforcer lacunes]
    REMEDIATION --> EVAL

    style DIAG fill:#FFF3CD
    style M1 fill:#CCE5FF
    style M2 fill:#CCE5FF
    style EX1 fill:#D4EDDA
    style EX2 fill:#D4EDDA
    style EVAL fill:#FFF3CD
    style REMEDIATION fill:#F8D7DA
```

### Structure JSON associée

```json
{
  "type": "parcours_apprenant",
  "titre": "",
  "audience": "",
  "duree_totale": "",
  "nodes": [
    {
      "id": "M1",
      "type": "module|exercice|evaluation|remediation",
      "titre": "",
      "duree": "",
      "format": "presentiel|elearning|mixte|async",
      "objectif_pedagogique": "",
      "methode": "",
      "prerequis": []
    }
  ],
  "edges": [
    {
      "from": "M1",
      "to": "EX1",
      "condition": "",
      "label": ""
    }
  ]
}
```

---

## 2. Processus de Vente

```mermaid
graph TD
    START([🎯 Début du cycle]) --> QUAL{📋 Qualification<br/>BANT/SPIN}
    QUAL -->|Qualifié| DISCO[🔍 Découverte<br/>RDV 1 - 1h - Comprendre besoins]
    QUAL -->|Non qualifié| NURTURE[📧 Nurturing<br/>Séquence email - Maintenir contact]
    DISCO --> DIAG[📊 Diagnostic<br/>Restitution - 45min - Présenter analyse]
    DIAG --> PROP[📄 Proposition<br/>Envoi offre - Personnalisée]
    PROP --> NEGO{🤝 Négociation}
    NEGO -->|Accord| CLOSE([✅ Closing - Signature])
    NEGO -->|Objection prix| VALEUR[💎 Argumentation valeur<br/>ROI, références, garanties]
    NEGO -->|Objection timing| URGENCE[⏰ Création urgence<br/>Offre limitée, quick-win]
    VALEUR --> NEGO
    URGENCE --> NEGO
    NEGO -->|Refus| DEBRIEF[📝 Debrief<br/>Analyser les raisons - Capitaliser]
    NURTURE -->|Signal achat| QUAL

    style QUAL fill:#FFF3CD
    style NEGO fill:#FFF3CD
    style CLOSE fill:#D4EDDA
    style DEBRIEF fill:#F8D7DA
```

---

## 3. Parcours Client (Onboarding → Fidélisation)

```mermaid
graph TD
    START([🎯 Signature contrat]) --> KICK[🚀 Kick-off<br/>1h - Aligner objectifs et planning]
    KICK --> ONBOARD[📋 Onboarding<br/>1 sem - Questionnaires, docs, accès]
    ONBOARD --> DELIV1[📦 Livrable 1<br/>Titre - Durée - Format]
    DELIV1 --> CHECK1{✅ Point intermédiaire}
    CHECK1 -->|OK| DELIV2[📦 Livrable 2<br/>Titre - Durée - Format]
    CHECK1 -->|Ajustement| ADJUST[🔧 Correction<br/>Intégrer feedback]
    ADJUST --> DELIV2
    DELIV2 --> FINAL[📊 Restitution finale<br/>Bilan + recommandations]
    FINAL --> SATISF{⭐ Satisfaction}
    SATISF -->|Satisfait| UPSELL[🔄 Upsell/Cross-sell<br/>Nouvelle proposition]
    SATISF -->|Insatisfait| RECOVERY[🆘 Recovery<br/>Plan de rattrapage]
    UPSELL --> START

    style CHECK1 fill:#FFF3CD
    style SATISF fill:#FFF3CD
    style UPSELL fill:#D4EDDA
    style RECOVERY fill:#F8D7DA
```

---

## 4. Séquence de Prospection

```mermaid
graph LR
    START([🎯 Cible identifiée]) --> RESEARCH[🔍 Recherche<br/>J0 - LinkedIn + Web]
    RESEARCH --> TOUCH1[📧 Email 1<br/>J1 - Accroche personnalisée]
    TOUCH1 --> WAIT1[⏳ 3 jours]
    WAIT1 --> TOUCH2[💼 LinkedIn<br/>J4 - Demande connexion + message]
    TOUCH2 --> WAIT2[⏳ 4 jours]
    WAIT2 --> TOUCH3[📧 Email 2<br/>J8 - Relance valeur ajoutée]
    TOUCH3 --> WAIT3[⏳ 5 jours]
    WAIT3 --> TOUCH4[📞 Appel<br/>J13 - Call direct]
    TOUCH4 --> DECISION{📊 Résultat}
    DECISION -->|RDV obtenu| RDV([✅ Qualification])
    DECISION -->|Pas de réponse| TOUCH5[📧 Email 3<br/>J20 - Breakup email]
    DECISION -->|Refus poli| NURTURE[🔄 Nurture<br/>3 mois - Newsletter]
    NURTURE -->|Signal achat| START

    style DECISION fill:#FFF3CD
    style RDV fill:#D4EDDA
```

---

## 5. Architecture de Module (Zoom)

Pour détailler un seul bloc du parcours apprenant :

```mermaid
graph TD
    START([📚 Module X: Titre]) --> INTRO[🎬 Introduction<br/>5min - Vidéo/Oral - Contextualiser]
    INTRO --> ACTIV[💡 Activation<br/>10min - Question/Sondage - Mobiliser pré-acquis]
    ACTIV --> DEMO[📖 Démonstration<br/>20min - Contenu + Exemples - Transmettre]
    DEMO --> PRAT[🎯 Pratique guidée<br/>30min - Exercice encadré - Appliquer]
    PRAT --> CHECK{✅ Compréhension OK ?}
    CHECK -->|Oui| PRAT2[🎯 Pratique autonome<br/>20min - Cas réel - Transférer]
    CHECK -->|Non| CLARIF[🔄 Clarification<br/>10min - Questions/Reformulation]
    CLARIF --> PRAT
    PRAT2 --> DEBRIEF[📊 Debrief<br/>15min - Feedback collectif - Ancrer]
    DEBRIEF --> QUIZ[📝 Quiz de validation<br/>5min - 5 questions - Vérifier acquis]
    QUIZ --> END([✅ Module terminé])

    style ACTIV fill:#FFF3CD
    style DEMO fill:#CCE5FF
    style PRAT fill:#D4EDDA
    style PRAT2 fill:#D4EDDA
    style QUIZ fill:#FFF3CD
```

---

## Convention de Nommage

| Préfixe | Type de nœud | Couleur |
|---|---|---|
| M | Module / Contenu | 🟦 #CCE5FF |
| EX | Exercice / Mise en situation | 🟩 #D4EDDA |
| EVAL / QUIZ | Évaluation | 🟨 #FFF3CD |
| REMED / ADJUST | Correction / Remédiation | 🟥 #F8D7DA |
| DECISION | Point de décision (losange) | 🟨 #FFF3CD |

## Règles de Philippe

1. **Un diagramme = un niveau de zoom.** Ne pas mélanger vue macro et détail.
2. **Maximum 15 nœuds.** Au-delà, découper en sous-diagrammes liés.
3. **Chaque nœud a 4 infos :** titre, durée, format, objectif.
4. **Chaque arête conditionnelle est explicite.** Pas de "puis" vague.
5. **Toujours proposer le JSON structuré en plus du Mermaid** pour traçabilité.
