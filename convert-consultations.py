#!/usr/bin/env python3
"""
Conversion script to transform legacy Ayurvedic consultation markdown files
to structured JSON format with standardized recommendations.
"""

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class ConsultationParser:
    def __init__(self):
        # Load standard recommendations
        with open('standard-recommendations.json', 'r', encoding='utf-8') as f:
            self.standard_recs = json.load(f)['standardRecommendations']

    def parse_patient_info(self, content: str) -> Dict[str, Any]:
        """Extract patient demographic information"""
        patient = {}

        # Name and basic info - first few lines
        lines = content.split('\n')[:10]

        for line in lines:
            line = line.replace('*', '').strip()

            # Name
            if 'Name' in line and '–' in line:
                name_match = re.search(r'Name\s*[-–]\s*([^–]+?)(?:\s+Date|$)', line)
                if name_match:
                    patient['name'] = name_match.group(1).strip()

            # Date
            if 'Date' in line and '–' in line:
                date_match = re.search(r'Date\s*[-–]\s*([^–]+?)(?:\s+|$)', line)
                if date_match:
                    patient['date'] = date_match.group(1).strip()

            # Age
            if 'Age' in line and 'years' in line:
                age_match = re.search(r'Age\s*[-–]\s*(\d+)\s*years', line)
                if age_match:
                    patient['age'] = int(age_match.group(1))

            # Sex
            if 'Sex' in line and '–' in line:
                sex_match = re.search(r'Sex\s*[-–]\s*([^–]+?)(?:\s+|$)', line)
                if sex_match:
                    patient['sex'] = sex_match.group(1).strip()

            # Profession
            if 'Profession' in line and '–' in line:
                prof_match = re.search(r'Profession\s*[-–]\s*([^–]+?)(?:\s+|$)', line)
                if prof_match:
                    patient['profession'] = prof_match.group(1).strip()

        # Family information
        family = {}
        family_text = self.extract_section(content, r'Family.*?(?=Married|Present|$)', multiline=True)
        if family_text:
            family['hasFamily'] = 'Yes' in family_text

        married_text = self.extract_section(content, r'Married.*?(?=Children|Present|$)', multiline=True)
        if married_text:
            family['married'] = married_text.replace('Married –', '').strip()

        children_text = self.extract_section(content, r'Children.*?(?=Born|Present|$)', multiline=True)
        if children_text:
            family['children'] = children_text.replace('Children –', '').strip()

        if family:
            patient['family'] = family

        # Birth place
        birth_match = re.search(r'Born in\s*[-–]?\s*([^\n]+)', content)
        if birth_match:
            patient['birthPlace'] = birth_match.group(1).strip()

        # Pets
        pets_match = re.search(r'Pets\s*[-–]\s*([^\n]+)', content)
        if pets_match:
            patient['pets'] = pets_match.group(1).strip()

        # Email
        email_match = re.search(r'Email\s*[-–:]\s*([^\s\n]+@[^\s\n]+)', content)
        if email_match:
            patient['email'] = email_match.group(1).strip()

        # Phone
        phone_match = re.search(r'Phone\s*[-–:]\s*([^\n]+)', content)
        if phone_match:
            patient['phone'] = phone_match.group(1).strip()

        return patient

    def extract_section(self, content: str, pattern: str, multiline: bool = False) -> Optional[str]:
        """Extract a section using regex pattern"""
        flags = re.IGNORECASE | re.DOTALL if multiline else re.IGNORECASE
        match = re.search(pattern, content, flags)
        return match.group(0) if match else None

    def parse_consultation_info(self, content: str) -> Dict[str, Any]:
        """Extract consultation and medical history information"""
        consultation = {}

        # Present complaint
        complaint_match = re.search(r'Present complaint\*\*\s*\n(.*?)(?=\*\*|No Covid|TM|$)', content, re.DOTALL)
        if complaint_match:
            consultation['presentComplaint'] = self.clean_text(complaint_match.group(1))

        # COVID history
        covid_matches = re.findall(r'(No Covid[^*\n]*|Covid positive[^*\n]*|No vaccine[^*\n]*|vaccine[^*\n]*)', content, re.IGNORECASE)
        if covid_matches:
            consultation['covidHistory'] = ', '.join(covid_matches)

        # TM practice
        tm_match = re.search(r'TM.*?(?=\n|$)', content)
        if tm_match:
            consultation['tmPractice'] = tm_match.group(0)

        return consultation

    def parse_assessment(self, content: str) -> Dict[str, Any]:
        """Extract clinical assessment information"""
        assessment = {
            'vitals': {},
            'lifestyle': {'food': {}},
            'ayurvedicAssessment': {}
        }

        # Vitals
        vitals_patterns = {
            'pulse': r'Pulse\s*[-–]\s*([^\n]+)',
            'bowel': r'Bowel\s*[-–]\s*([^\n]+)',
            'urination': r'Urination\s*[-–]\s*([^\n]+)',
            'tongue': r'Tongue\s*[-–]\s*([^\n]+)',
            'sleep': r'Sleep\s*[-–]\s*([^\n]+)',
            'hunger': r'Hunger\s*[-–]\s*([^\n]+)',
            'thirst': r'Thirst\s*[-–]\s*([^\n]+)',
            'menstruation': r'Menstruation\s*[-–]\s*([^\n]+)'
        }

        for key, pattern in vitals_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                assessment['vitals'][key] = match.group(1).strip()

        # Lifestyle
        lifestyle_patterns = {
            'dailyRoutine': r'Daily routine\s*[-–]\s*([^\n]+)',
            'smoking': r'Smoking\s*[-–]\s*([^\n]+)',
            'alcohol': r'Alcohol\s*[-–]\s*([^\n]+)',
            'exercise': r'Exercise\s*[-–]\s*([^\n]+)',
            'emotions': r'Emotions\s*[-–]\s*([^\n]+)'
        }

        for key, pattern in lifestyle_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                assessment['lifestyle'][key] = match.group(1).strip()

        # Food
        food_patterns = {
            'hoteling': r'Food\s*[-–]\s*([^\n]+)',
            'oils': r'Oil\s*[-–]\s*([^\n]+)',
            'breakfast': r'Breakfast\s*[-–]\s*([^\n]+)',
            'lunch': r'Lunch\s*[-–]\s*([^\n]+)',
            'dinner': r'Dinner\s*[-–]\s*([^\n]+)',
            'fruits': r'Fruits\s*[-–]\s*([^\n]+)'
        }

        for key, pattern in food_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                assessment['lifestyle']['food'][key] = match.group(1).strip()

        # Ayurvedic Assessment
        ayur_patterns = {
            'prakruti': r'Prakruti\s*[-–]\s*([^\n]+)',
            'vikruti': r'Vikruti\s*[-–]\s*([^\n]+)',
            'dosha': r'Dosha\s*[-–]\s*([^\n]+)',
            'dushya': r'Dushya\s*[-–]\s*([^\n]+)'
        }

        for key, pattern in ayur_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                assessment['ayurvedicAssessment'][key] = match.group(1).strip()

        return assessment

    def parse_treatment(self, content: str) -> Dict[str, Any]:
        """Extract treatment recommendations"""
        treatment = {
            'shamana': [],
            'panchakarma': [],
            'additionalAdvice': []
        }

        # Shamana (Internal Medicine)
        shamana_section = self.extract_section(content, r'Shamana.*?(?=Panchakarma|Advice|Avoid)', multiline=True)
        if shamana_section:
            medicine_lines = re.findall(r'(\d+)\.\s*\*\*(.*?)\*\*', shamana_section)
            for _, medicine_text in medicine_lines:
                # Parse medicine and dosage
                if '–' in medicine_text:
                    parts = medicine_text.split('–', 1)
                    medicine_name = parts[0].strip()
                    dosage = parts[1].strip() if len(parts) > 1 else ""
                    treatment['shamana'].append({
                        'medicine': medicine_name,
                        'dosage': dosage
                    })

        # Panchakarma
        panchakarma_section = self.extract_section(content, r'Panchakarma\*\*(.*?)(?=\*\*Advice|\*\*Avoid)', multiline=True)
        if panchakarma_section:
            panchakarma_lines = re.findall(r'(\d+)\.\s*\*\*(.*?)\*\*', panchakarma_section)
            for _, therapy in panchakarma_lines:
                treatment['panchakarma'].append(therapy.strip())

        # Additional Advice (if any specific advice sections exist)
        advice_patterns = [
            r'Aroma therapy[^\n]*',
            r'Chanting of mantras[^\n]*',
            r'Advice to do Moolabandha',
            r'Use of Asafetida[^\n]*',
            r'Drink medicated water[^\n]*'
        ]

        for pattern in advice_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            treatment['additionalAdvice'].extend(matches)

        return treatment

    def clean_text(self, text: str) -> str:
        """Clean text by removing extra formatting and whitespace"""
        # Remove markdown formatting
        text = re.sub(r'\*\*', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def parse_file(self, filepath: str) -> Dict[str, Any]:
        """Parse a single consultation file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        consultation_data = {
            'patient': self.parse_patient_info(content),
            'consultation': self.parse_consultation_info(content),
            'assessment': self.parse_assessment(content),
            'treatment': self.parse_treatment(content),
            'standardRecommendations': self.standard_recs,
            'metadata': {
                'createdAt': datetime.now().isoformat(),
                'lastModified': datetime.now().isoformat(),
                'version': '1.0',
                'language': 'en',
                'originalFile': os.path.basename(filepath)
            }
        }

        return consultation_data

    def convert_all_files(self, input_dir: str = '.', output_dir: str = './converted') -> None:
        """Convert all consultation markdown files to JSON"""
        os.makedirs(output_dir, exist_ok=True)

        # Find all consultation files
        consultation_files = [f for f in os.listdir(input_dir)
                            if f.endswith('.md') and
                            'consultation' not in f.lower() and
                            'template' not in f.lower() and
                            'readme' not in f.lower()]

        print(f"Found {len(consultation_files)} consultation files to convert")

        for filename in consultation_files:
            try:
                print(f"Converting {filename}...")
                filepath = os.path.join(input_dir, filename)
                consultation_data = self.parse_file(filepath)

                # Create output filename
                base_name = os.path.splitext(filename)[0]
                output_filename = f"{base_name}.json"
                output_path = os.path.join(output_dir, output_filename)

                # Save JSON
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(consultation_data, f, indent=2, ensure_ascii=False)

                print(f"✓ Converted to {output_filename}")

            except Exception as e:
                print(f"✗ Error converting {filename}: {str(e)}")

        print(f"\nConversion complete! Check the '{output_dir}' directory for results.")

def main():
    parser = ConsultationParser()
    parser.convert_all_files()

if __name__ == "__main__":
    main()