# Ayurvedic Consultation Management System

A comprehensive system for managing, standardizing, and generating bilingual Ayurvedic lifestyle consultation documents.

## Overview

This system transforms unstructured consultation markdown files into a standardized JSON format that can be used to generate bilingual (English/French) PDF reports for patients.

## Files Structure

### Core Components

- **`consultation-schema.json`** - JSON Schema defining the complete data structure for patient consultations
- **`consultation-template.md`** - Bilingual Markdown template with YAML front matter for document generation
- **`standard-recommendations.json`** - Standardized recommendation text blocks in both English and French
- **`convert-consultations.rb`** - Ruby script to convert legacy markdown files to structured JSON format

### Generated Directories

- **`converted/`** - Contains the converted JSON files from legacy markdown documents

## Data Structure

The system captures comprehensive patient information:

### Patient Information
- Demographics (name, age, sex, date)
- Contact details (email, phone)
- Personal details (profession, family status, children, birth place, pets)

### Medical Assessment
- Present complaints and medical history
- COVID and vaccination history
- TM (Transcendental Meditation) practice history
- Clinical vitals (pulse, bowel, urination, tongue, sleep, etc.)
- Lifestyle assessment (diet, exercise, emotions, daily routine)
- Ayurvedic assessment (Prakruti, Vikruti, Dosha, Dushya)

### Treatment Recommendations
- **Shamana** - Internal medicines with exact dosages (e.g., MA579, MA289)
- **Panchakarma** - Physical therapy recommendations
- **Additional Advice** - Specific recommendations per patient
- **Standard Recommendations** - Common lifestyle guidelines (identical across all patients)

## Usage

### Converting Legacy Files

Run the Ruby conversion script to transform existing markdown consultation files:

```bash
ruby convert-consultations.rb
```

This will:
1. Read all `.md` files in the current directory (excluding templates)
2. Parse patient information, assessments, and treatments
3. Generate structured JSON files in the `converted/` directory
4. Preserve all VERBATIM medical recommendations

### Adding New Consultations

1. Create a new consultation following the established pattern
2. Include patient email and phone number fields:
   ```
   **Email:** patient@example.com
   **Phone:** +33 1 23 45 67 89
   ```
3. Run the conversion script to generate structured data

### Generating Bilingual Documents

The system supports generating bilingual documents using the template structure. The template includes:

- English labels with French translations
- VERBATIM medical recommendations (unchanged for accuracy)
- Standardized text blocks in both languages

## Key Features

### VERBATIM Preservation
- All medicine names (MA579, MA289, etc.) preserved exactly
- Dosage instructions maintained word-for-word
- Critical for medical accuracy and liability

### Standardized Text Blocks
Common recommendations are standardized and translated:
- Avoid/Stop/Reduce guidelines
- Take/Use dietary recommendations
- Lifestyle recommendations
- Self-care practices
- Mental wellness advice
- Panchakarma advice
- Follow-up instructions

### Bilingual Support
- English-French field labels
- Pre-translated standard recommendations
- Template ready for PDF generation

## Medical Accuracy

⚠️ **CRITICAL**: All medical recommendations, dosages, and medicine codes are preserved VERBATIM from the original consultations. Any modifications to treatment recommendations should only be made by qualified Ayurvedic practitioners.

## Next Steps

1. **PDF Generation**: Implement automated PDF generation from JSON data
2. **Patient Portal**: Create a web interface for accessing consultation reports
3. **Translation Workflow**: Set up professional translation for patient-specific content
4. **Email Integration**: Automate sending bilingual PDFs to patients

## File Naming Convention

- Original: `Patient Name - Number.md`
- Converted: `Patient Name - Number.json`
- Maintains patient identification and consultation sequence