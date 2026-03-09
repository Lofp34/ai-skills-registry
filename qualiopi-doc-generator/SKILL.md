---
name: qualiopi-doc-generator
description: Générateur de documents conformes Qualiopi pour organismes de formation certifiés RNQ. Utiliser dès que l'utilisateur mentionne convention de formation, programme de formation, déroulé pédagogique, devis formation, document Qualiopi, ou demande de créer/générer un document administratif lié à son activité de formation. Aussi déclencher quand l'utilisateur dit "prépare une convention", "fais-moi un programme", "génère un devis", "document pour mon client", "je dois envoyer les documents au client", ou toute variante impliquant la production de documents contractuels ou pédagogiques pour un organisme de formation. Ne PAS déclencher pour des questions générales sur Qualiopi ou la préparation d'audit (utiliser les documents sources directement).
---

# Générateur de Documents Conformes Qualiopi

## Objectif

Ce skill génère des documents professionnels (conventions, programmes, devis) qui respectent les exigences du Référentiel National Qualité (RNQ) V9 du 8 janvier 2024. Chaque document intègre automatiquement les mentions et informations requises par les indicateurs Qualiopi applicables, évitant ainsi les non-conformités lors des audits.

## Contexte réglementaire

La certification Qualiopi impose aux organismes de formation de fournir des documents contenant des informations précises et vérifiables. Les indicateurs clés impactant les documents sont :

- **Indicateur 1** : Information accessible, détaillée et vérifiable (prérequis, objectifs, durée, modalités/délais d'accès, tarifs, contacts, méthodes, modalités d'évaluation, accessibilité PSH)
- **Indicateur 2** : Diffusion d'indicateurs de résultats (taux de satisfaction, nombre d'apprenants, etc.)
- **Indicateur 4** : Analyse du besoin du bénéficiaire
- **Indicateur 5** : Objectifs opérationnels et évaluables
- **Indicateur 6** : Contenus et modalités adaptés aux objectifs et publics
- **Indicateur 9** : Information sur les conditions de déroulement

## Workflow

### Étape 1 : Collecter les informations

Avant de générer un document, collecter les informations nécessaires auprès de l'utilisateur. Consulter le fichier de référence correspondant au type de document demandé :

| Document demandé | Fichier de référence |
|---|---|
| Convention de formation | `references/convention.md` |
| Programme / déroulé pédagogique | `references/programme.md` |
| Devis conforme Qualiopi | `references/devis.md` |

Lire le fichier de référence correspondant **avant** de commencer la génération. Ce fichier contient la structure exacte, les mentions obligatoires et les indicateurs Qualiopi associés.

### Étape 2 : Poser les questions manquantes

Comparer les informations déjà fournies par l'utilisateur (dans le message ou via la mémoire) avec la checklist du fichier de référence. Ne poser que les questions dont la réponse manque. Regrouper les questions pour minimiser les allers-retours.

Informations typiquement connues via la mémoire ou le contexte :
- Raison sociale de l'OF, SIRET, NDA, adresse
- Nom du dirigeant / responsable
- Contacts référents (pédagogique, handicap, qualité)

Informations à demander systématiquement (sauf si déjà fournies) :
- Informations sur le client (entreprise, contact, adresse)
- Intitulé et détails de la formation
- Dates, durée, lieu, modalités
- Nombre de participants
- Tarif

### Étape 3 : Générer le document

Utiliser le skill `docx` pour les conventions et devis (format Word personnalisable).
Utiliser le skill `docx` ou `pdf` pour les programmes selon la préférence de l'utilisateur.

Appliquer ces principes de mise en forme :
- **En-tête** : logo ou raison sociale de l'OF, NDA, SIRET
- **Typographie** : professionnelle et lisible (Arial ou équivalent, 11-12pt corps)
- **Structure** : sections clairement identifiées avec numérotation
- **Pied de page** : mention NDA, SIRET, pagination
- **Date et versioning** : chaque document daté, avec mention "Mis à jour le JJ/MM/AAAA"

### Étape 4 : Vérification de conformité

Avant de finaliser, vérifier que le document contient TOUTES les mentions obligatoires listées dans le fichier de référence correspondant. Ne jamais livrer un document incomplet au regard des exigences Qualiopi.

## Informations de l'organisme de formation

Si l'utilisateur a configuré ses informations d'OF dans la mémoire Claude, les utiliser automatiquement. Sinon, demander lors de la première utilisation et suggérer de les sauvegarder en mémoire pour les prochaines fois.

Informations de l'OF à connaître :
- Raison sociale complète
- Forme juridique
- Adresse du siège
- SIRET
- Numéro de déclaration d'activité (NDA) + préfecture
- Nom du représentant légal
- Contact principal (téléphone, email)
- Référent pédagogique (nom, contact)
- Référent handicap (nom, contact)
- Référent qualité (nom, contact)
- Numéro de certification Qualiopi et organisme certificateur
- Site web / catalogue en ligne

## Règles de rédaction

1. **Objectifs en verbes d'action** : Toujours formuler les objectifs pédagogiques avec des verbes d'action mesurables (taxonomie de Bloom : identifier, appliquer, analyser, créer, évaluer...). Jamais "comprendre" ou "connaître" seuls.

2. **Modalités d'évaluation explicites** : Préciser le type d'évaluation (QCM, mise en situation, étude de cas, auto-positionnement) ET les critères de réussite (ex : "70% de bonnes réponses").

3. **Accessibilité PSH** : Toujours inclure une mention sur l'accessibilité et le contact du référent handicap. C'est une exigence transversale du RNQ.

4. **Délais d'accès** : Mentionner systématiquement le délai entre l'inscription et le début de la formation.

5. **Indicateurs de résultats** : Sur les programmes, inclure au minimum le taux de satisfaction et le nombre de participants si disponibles.

6. **Dates et versioning** : Tous les documents doivent être datés. Le guide de lecture V9 insiste sur le fait que l'information doit être "à jour".
