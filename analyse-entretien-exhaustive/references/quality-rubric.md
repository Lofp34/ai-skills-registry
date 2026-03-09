# Rubrique qualité

## Critères bloquants
- Schéma JSON invalide.
- Fichiers obligatoires absents.
- Couverture des segments < 0.98.
- Assertions critiques sans preuve.

## Critères majeurs
- Contradictions intra-sujet non détectées.
- Sujet important absent de la taxonomie consolidée.
- Décisions ou risques non reliés à des `segment_refs`.

## Critères mineurs
- Redondances rédactionnelles dans les `.md`.
- Libellés de sujets trop génériques.
- Confiance rhétorique absente sur plusieurs mouvements.

## Checklist finale
1. Tous les fichiers requis existent.
2. `manifest.json` et `topic_map.json` conformes.
3. `topics/topic-XXX.json` complets pour chaque sujet.
4. `rhetorical_map.json` contient les 4 blocs attendus.
5. `validate_outputs.py --strict` passe sans erreur.
6. Couverture >= 0.98.
7. `qa_report.json` cohérent avec le calcul de couverture.
