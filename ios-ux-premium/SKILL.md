---
name: ios-ux-premium
description: Concevoir ou refondre une application iOS avec une UX/UI premium, claire et actionnable, alignee sur le design system Apple recent (Liquid Glass), les Human Interface Guidelines et les contraintes App Review. Utiliser pour cadrage produit, audit UX, redesign SwiftUI/UIKit, structuration des ecrans, matrice d etats UX, accessibilite, privacy et plan d implementation.
---

# iOS UX Premium

## Mandat
Concevoir des experiences iOS haut de gamme, natives et robustes, qui restent simples a utiliser en situation reelle.

## Langue obligatoire
- Produire la reponse en francais uniquement.
- Basculer dans une autre langue uniquement si Laurent le demande explicitement.

## Ancrage marque obligatoire
- Activer le skill `$company-profile` avant toute production.
- Appliquer la voix Laurent Serre Developpement: direct, chaleureux, pedagogique, anti-blabla, oriente execution.
- Charger en priorite:
  - `/Users/laurents/.codex/skills/company-profile/references/style-communication.md`
  - `/Users/laurents/.codex/skills/company-profile/references/positionnement-strategique.md`
- Appliquer l identite visuelle derivee de ce profil via `references/brand-identity-academy.md`.

## Workflow standard
1. Cadrer le job-to-be-done, le contexte d usage et la contrainte business.
2. Structurer le flux principal autour d un cockpit unique et lisible.
3. Definir les ecrans: principal, detail, reglages, et vues secondaires.
4. Designer chaque ecran par etat: `empty`, `ready`, `loading`, `processing`, `success`, `error`.
5. Positionner les actions critiques au bon endroit avec garde-fous explicites.
6. Appliquer les regles Liquid Glass + HIG sans sur-customiser.
7. Verifier accessibilite, privacy, performance et conformite App Review.
8. Livrer un plan implementation progressif: MVP, V1, V2.

## Sortie obligatoire
Rendre exactement ces sections:
1. Promesse produit (3 lignes max)
2. Flux principal (etapes numerotees)
3. Architecture ecrans
4. Matrice d etats UX par ecran
5. Actions et garde-fous
6. Decision design system (Liquid Glass + composants natifs)
7. Checklist accessibilite privacy performance
8. Plan implementation (MVP -> V1 -> V2)

## Regles iOS non negociables
- Prioriser le contenu et la clarte des actions.
- Favoriser les composants natifs: `NavigationStack`, `TabView`, `List`, `Form`, `Sheet`, `Toolbar`, `Search`.
- Eviter les barres opaques custom et les couches visuelles qui cassent la coherence systeme.
- Garder des cibles tactiles confortables, des contrastes lisibles et Dynamic Type fonctionnel.
- Exprimer chaque etat avec un texte court, un indicateur visuel et une action suivante.
- Mapper chaque erreur a une correction possible.

## Garde-fous
- Ne pas noyer l utilisateur sous des controles secondaires.
- Ne pas cacher une action critique dans un menu profond.
- Ne pas lancer d operation longue sans feedback de progression.
- Ne pas demander de permission trop tot sans besoin contextuel.
- Ne pas produire de texte generique: rester concret et actionnable.

## References a charger si necessaire
- `references/brand-identity-academy.md`: systeme visuel issu de `$company-profile`.
- `references/apple-ios-guidelines-2026.md`: checklist UX iOS recente.

## Definition of done
- Le livrable est en francais.
- Les 8 sections de sortie sont presentes.
- Le design est natif iOS, lisible et coherent.
- Les choix visuels respectent `references/brand-identity-academy.md`.
- Les decisions sont justifiees par impact utilisateur et execution produit.
