---
name: client-intake
description: Gérer l’ingestion opérationnelle des transcriptions, notes et emails pour créer/mettre à jour les dossiers clients, fiches personnes et tableaux de bord. Utiliser quand de nouveaux contenus arrivent (WhatsApp, Gmail, notes) et qu’il faut décider create/update avec mode proposition.
---

1. Traiter tout nouveau contenu (transcriptions, notes, emails) comme une source d’événement.
2. Identifier le client concerné (avec score de confiance) puis router vers le dossier cible.
3. Détecter les personnes (collaborateurs, contacts, prospects) et créer une fiche individuelle si absente.
4. Toujours enrichir la fiche personne via MCP `anysite-hdw` en priorité (LinkedIn et web parsing), puis compléter avec sources web publiques si nécessaire.
5. Inclure la photo LinkedIn quand disponible (`photo_linkedin_url` + image intégrée en HTML quand possible).
6. Respecter l’arborescence:
   - Client: `Contacts/` (pas de sous-dossier `Personnes`)
   - Ressources internes: `Ressources/Personnes/`
7. En mode `proposition`, ne pas écrire de modifications sensibles avant validation explicite de Laurent.
8. Envoyer une proposition WhatsApp structurée:
   - Client détecté
   - Nouvelles personnes détectées
   - Fiches à créer/mettre à jour
   - Impacts dashboard
   - Action demandée: `VALIDE` / `AJUSTE`
9. Après validation, exécuter les mises à jour puis tracer dans `memory/YYYY-MM-DD.md`.
10. Mettre à jour les dashboards si impact business, relationnel ou opérationnel détecté.