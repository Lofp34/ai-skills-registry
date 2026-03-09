# Checklist iOS recente (Liquid Glass + HIG)

## Objectif
Appliquer les principes Apple recents sans casser la clarte produit.

## Principes de base
1. Content-first: le contenu prime sur l habillage.
2. Hierarchie claire: une action principale visible immediatement.
3. Coherence systeme: composants natifs avant surcouche custom.
4. Progressive disclosure: details affiches seulement quand utiles.

## Liquid Glass (application pragmatique)
- Conserver les couches systeme (bars, sheets, materials) et leur comportement.
- Eviter les fonds opaques lourds qui annulent la profondeur visuelle.
- Garder contraste texte/fond et lisibilite en toutes tailles.
- Utiliser les effets comme signal d etat, pas comme decoration.

## Navigation et structure
- Structurer autour de `NavigationStack`.
- Limiter la profondeur de navigation.
- Regrouper les actions secondaires en sheet/menu contextuel.
- Toujours afficher un chemin de retour evident.

## Etats UX
- Definir: `empty`, `ready`, `loading`, `processing`, `success`, `error`.
- Afficher message court + indicateur visuel + prochaine action.
- Eviter les etats silencieux.

## Accessibilite
- Supporter Dynamic Type sans chevauchement.
- Respecter le contraste et la lisibilite.
- Prevoir labels VoiceOver explicites.
- Garder des cibles tactiles confortables.

## Privacy et permissions
- Demander une permission uniquement au moment utile.
- Expliquer la valeur utilisateur avant la demande.
- Fournir un fallback si permission refusee.

## Performance et fiabilite
- Montrer la progression pour operations longues.
- Preserver l etat utilisateur sur interruption.
- Degrader proprement en cas d erreur reseau/API.

## App Review readiness
- Clarifier les flux sensibles (audio, donnees personnelles).
- Eviter promesses non tenables.
- Verifier legalite locale des fonctionnalites sensibles.
