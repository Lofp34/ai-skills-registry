# Routage des Frameworks Elite BA pour Visual Production Studio

## Objectif

Standardiser la sélection des frameworks Elite BA (72 disponibles) pendant l'étape 0 M+B et les blocs stratégiques d'Isabelle.

Source de vérité :
- `../elite-business-advisory/references/FRAMEWORKS-INDEX.md`
- `../elite-business-advisory/references/framework-*.md`

---

## Règles de Routage

- Toujours commencer avec 1 framework de structuration (Marie) + 1 framework d'exécution (Thomas)
- Limiter à 2-6 frameworks par mission
- Éviter le sur-cadrage théorique : chaque framework doit déboucher sur une décision
- N'activer Sophie que sur demande utilisateur explicite ou risque juridique majeur détecté

---

## Mapping Principal (Marie + Thomas)

| Type de demande | Frameworks prioritaires | Fichiers |
|---|---|---|
| Cadrage d'un problème complexe | MECE + Issue Tree | `framework-mece.md`, `framework-issue-tree.md` |
| Plan de transformation commerciale | Results Delivery + Rapid Results | `framework-results-delivery.md`, `framework-rapid-results.md` |
| Structuration d'offre | Value Proposition + Impact/Effort | `framework-value-prop.md`, `framework-impact-effort.md` |
| Préparation RDV / qualification | BANT + SPIN | `framework-bant.md`, `framework-spin.md` |
| Priorisation d'actions | Impact/Effort + ICE | `framework-impact-effort.md`, `framework-ice.md` |
| Positionnement stratégique | SWOT + Porter's Five Forces | `framework-swot.md`, `framework-porter-5-forces.md` |
| Pricing et valeur | Value-Based Pricing + EVC | `framework-value-based-pricing.md`, `framework-evc.md` |
| Croissance et scale | Core Business Focus + Repeatable Model | `framework-core-business.md`, `framework-repeatable-model.md` |

---

## Mapping Complémentaire (si besoin)

| Besoin secondaire | Frameworks | Fichiers |
|---|---|---|
| Gouvernance de projet | RACI + OKR | `framework-raci.md`, `framework-okr.md` |
| Négociation commerciale | BATNA + ZOPA + Concession Matrix | `framework-batna.md`, `framework-zopa.md`, `framework-concession-matrix.md` |
| Segmentation clients | STP + Customer Segmentation | `framework-stp.md`, `framework-customer-segmentation.md` |
| Décision d'investissement | Decision Tree + Cost-Benefit | `framework-decision-tree.md`, `framework-cost-benefit.md` |

---

## Activation Conditionnelle de Sophie (Juridique)

### Triggers automatiques

- contrat, clause, CGV, NDA
- propriété intellectuelle (IP), confidentialité
- RGPD / données personnelles
- limitation de responsabilité
- litige / arbitrage / contentieux
- marché public / compliance

### Routage Sophie

| Type de risque juridique | Frameworks Sophie | Fichiers |
|---|---|---|
| Contractualisation | Modular Contracting + Plain Language Contracting | `framework-modular-contracting.md`, `framework-plain-language.md` |
| Répartition des risques | Risk-Sharing + Limitation of Liability | `framework-risk-sharing.md`, `framework-limitation-liability.md` |
| Données personnelles | RGPD Compliance | `framework-rgpd.md` |
| Litiges et sortie de conflit | Dispute Resolution Ladder | `framework-dispute-resolution.md` |
| IP / confidentialité | IP Protection | `framework-ip-protection.md` |

Règle : en cas de trigger, le skill propose l'activation Sophie. Si l'utilisateur confirme, Sophie est intégrée au flux.

---

## Format de Sélection Recommandé

```json
{
  "mission_type": "",
  "primary_frameworks": [
    {
      "name": "",
      "file": "../elite-business-advisory/references/framework-*.md",
      "owner": "Marie|Thomas|Sophie",
      "purpose": ""
    }
  ],
  "secondary_frameworks": [],
  "legal_trigger": {
    "detected": false,
    "reason": "",
    "sophie_proposed": false
  }
}
```

---

## Contrôle Qualité

- [ ] Minimum 1 framework Marie + 1 framework Thomas
- [ ] Maximum 6 frameworks au total
- [ ] Tous les fichiers cités existent dans `../elite-business-advisory/references/`
- [ ] Sophie activée uniquement selon règle
- [ ] Sélection reliée à des décisions/action items concrets
