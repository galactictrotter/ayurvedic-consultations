---
# Ayurvedic Lifestyle Consultation Template
patient:
  name: ""
  age: 0
  sex: ""
  date: ""
  profession: ""
  family:
    hasFamily: false
    married: ""
    children: ""
  birthPlace: ""
  pets: ""
  email: ""
  phone: ""

consultation:
  presentComplaint: ""
  medicalHistory: ""
  covidHistory: ""
  tmPractice: ""

assessment:
  vitals:
    pulse: ""
    bowel: ""
    urination: ""
    tongue: ""
    sleep: ""
    hunger: ""
    thirst: ""
    menstruation: ""
  lifestyle:
    dailyRoutine: ""
    smoking: ""
    alcohol: ""
    exercise: ""
    emotions: ""
    food:
      hoteling: ""
      oils: ""
      breakfast: ""
      lunch: ""
      dinner: ""
      fruits: ""
  ayurvedicAssessment:
    prakruti: ""
    vikruti: ""
    dosha: ""
    dushya: ""

treatment:
  shamana: []
  panchakarma: []
  additionalAdvice: []

translations:
  fr:
    patient:
      name: "Nom"
      age: "Âge"
      sex: "Sexe"
      date: "Date"
      profession: "Profession"
      family: "Famille"
      married: "Marié(e)"
      children: "Enfants"
      birthPlace: "Lieu de naissance"
    consultation:
      presentComplaint: "Plainte actuelle"
      medicalHistory: "Antécédents médicaux"
      covidHistory: "Historique COVID"
      tmPractice: "Pratique de la MT"
    assessment:
      vitals: "Signes vitaux"
      lifestyle: "Mode de vie"
      ayurvedicAssessment: "Évaluation ayurvédique"
    treatment:
      shamana: "Médecine interne (Shamana)"
      panchakarma: "Panchakarma"
      additionalAdvice: "Conseils supplémentaires"

metadata:
  createdAt: ""
  lastModified: ""
  version: "1.0"
  language: "en-fr"
---

# Lifestyle Consultation Form / Formulaire de Consultation de Mode de Vie

## Patient Information / Informations du Patient

**Name / Nom:** {{ patient.name }}
**Date / Date:** {{ patient.date }}
**Age / Âge:** {{ patient.age }} years / ans
**Sex / Sexe:** {{ patient.sex }}
**Profession:** {{ patient.profession }}

{% if patient.family.hasFamily %}
**Family / Famille:** Yes / Oui
{% endif %}
{% if patient.family.married %}
**Married / Marié(e):** {{ patient.family.married }}
{% endif %}
{% if patient.family.children %}
**Children / Enfants:** {{ patient.family.children }}
{% endif %}
{% if patient.birthPlace %}
**Born in / Né(e) à:** {{ patient.birthPlace }}
{% endif %}
{% if patient.pets %}
**Pets / Animaux domestiques:** {{ patient.pets }}
{% endif %}
{% if patient.email %}
**Email:** {{ patient.email }}
{% endif %}
{% if patient.phone %}
**Phone / Téléphone:** {{ patient.phone }}
{% endif %}

## Present Complaint / Plainte Actuelle

{{ consultation.presentComplaint }}

{% if consultation.medicalHistory %}
**Medical History / Antécédents médicaux:** {{ consultation.medicalHistory }}
{% endif %}
{% if consultation.covidHistory %}
**COVID History / Historique COVID:** {{ consultation.covidHistory }}
{% endif %}
{% if consultation.tmPractice %}
**TM Practice / Pratique MT:** {{ consultation.tmPractice }}
{% endif %}

## Clinical Assessment / Évaluation Clinique

{% if assessment.vitals.pulse %}
**Pulse:** {{ assessment.vitals.pulse }}
{% endif %}
{% if assessment.vitals.bowel %}
**Bowel / Intestin:** {{ assessment.vitals.bowel }}
{% endif %}
{% if assessment.vitals.urination %}
**Urination / Miction:** {{ assessment.vitals.urination }}
{% endif %}
{% if assessment.vitals.tongue %}
**Tongue / Langue:** {{ assessment.vitals.tongue }}
{% endif %}
{% if assessment.vitals.sleep %}
**Sleep / Sommeil:** {{ assessment.vitals.sleep }}
{% endif %}
{% if assessment.vitals.hunger %}
**Hunger / Faim:** {{ assessment.vitals.hunger }}
{% endif %}
{% if assessment.vitals.thirst %}
**Thirst / Soif:** {{ assessment.vitals.thirst }}
{% endif %}
{% if assessment.vitals.menstruation %}
**Menstruation:** {{ assessment.vitals.menstruation }}
{% endif %}

## Lifestyle Assessment / Évaluation du Mode de Vie

{% if assessment.lifestyle.dailyRoutine %}
**Daily routine / Routine quotidienne:** {{ assessment.lifestyle.dailyRoutine }}
{% endif %}
{% if assessment.lifestyle.smoking %}
**Smoking / Tabagisme:** {{ assessment.lifestyle.smoking }}
{% endif %}
{% if assessment.lifestyle.alcohol %}
**Alcohol / Alcool:** {{ assessment.lifestyle.alcohol }}
{% endif %}
{% if assessment.lifestyle.exercise %}
**Exercise / Exercice:** {{ assessment.lifestyle.exercise }}
{% endif %}
{% if assessment.lifestyle.emotions %}
**Emotions / Émotions:** {{ assessment.lifestyle.emotions }}
{% endif %}

### Food Habits / Habitudes Alimentaires

{% if assessment.lifestyle.food.hoteling %}
**Hoteling:** {{ assessment.lifestyle.food.hoteling }}
{% endif %}
{% if assessment.lifestyle.food.oils %}
**Oil / Huile:** {{ assessment.lifestyle.food.oils }}
{% endif %}
{% if assessment.lifestyle.food.breakfast %}
**Breakfast / Petit déjeuner:** {{ assessment.lifestyle.food.breakfast }}
{% endif %}
{% if assessment.lifestyle.food.lunch %}
**Lunch / Déjeuner:** {{ assessment.lifestyle.food.lunch }}
{% endif %}
{% if assessment.lifestyle.food.dinner %}
**Dinner / Dîner:** {{ assessment.lifestyle.food.dinner }}
{% endif %}
{% if assessment.lifestyle.food.fruits %}
**Fruits:** {{ assessment.lifestyle.food.fruits }}
{% endif %}

## Ayurvedic Assessment / Évaluation Ayurvédique

{% if assessment.ayurvedicAssessment.prakruti %}
**Prakruti:** {{ assessment.ayurvedicAssessment.prakruti }}
{% endif %}
{% if assessment.ayurvedicAssessment.vikruti %}
**Vikruti:** {{ assessment.ayurvedicAssessment.vikruti }}
{% endif %}
{% if assessment.ayurvedicAssessment.dosha %}
**Dosha:** {{ assessment.ayurvedicAssessment.dosha }}
{% endif %}
{% if assessment.ayurvedicAssessment.dushya %}
**Dushya:** {{ assessment.ayurvedicAssessment.dushya }}
{% endif %}

## Treatment Recommendations / Recommandations de Traitement

### Shamana (Internal Medicine) / Médecine Interne

{% for medicine in treatment.shamana %}
{{ loop.index }}. **{{ medicine.medicine }}** - {{ medicine.dosage }}
{% endfor %}

### Panchakarma

{% for therapy in treatment.panchakarma %}
{{ loop.index }}. **{{ therapy }}**
{% endfor %}

{% if treatment.additionalAdvice %}
### Additional Advice / Conseils Supplémentaires

{% for advice in treatment.additionalAdvice %}
- **{{ advice }}**
{% endfor %}
{% endif %}

## Standard Recommendations / Recommandations Standards

### Avoid/Stop/Reduce / Éviter/Arrêter/Réduire

{{ standardRecommendations.avoidStopReduce }}

### Take/Use / Prendre/Utiliser

{{ standardRecommendations.takeUse }}

### Lifestyle / Mode de Vie

{{ standardRecommendations.lifestyle }}

{{ standardRecommendations.selfCare }}

{{ standardRecommendations.mentalWellness }}

### Panchakarma Advice / Conseils Panchakarma

{{ standardRecommendations.panchakarmaAdvice }}

### Follow-up / Suivi

{{ standardRecommendations.followUp }}