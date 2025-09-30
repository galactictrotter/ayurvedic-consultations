#!/usr/bin/env python3
"""
Refined conversion script to transform Ayurvedic consultation markdown files
to structured JSON format with improved field extraction and markdown cleanup.

Version 2.0 - Enhanced parser with complete data extraction
"""

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class ConsultationParserV2:
    def __init__(self):
        # Load standard recommendations
        with open('standard-recommendations.json', 'r', encoding='utf-8') as f:
            self.standard_recs = json.load(f)['standardRecommendations']

    def clean_markdown(self, text: str) -> str:
        """Remove all markdown formatting and extra whitespace"""
        if not text:
            return ""
        # Remove markdown bold
        text = re.sub(r'\*\*', '', text)
        # Remove escape characters
        text = text.replace('\\-', '-').replace('\\+', '+')
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def parse_patient_info(self, content: str) -> Dict[str, Any]:
        """Extract patient demographic information with improved parsing"""
        patient = {}

        # Get first 15 lines for header info
        lines = content.split('\n')[:15]

        # Parse Name and Date (can be on same line or separate lines)
        for line in lines[:8]:
            clean_line = self.clean_markdown(line)

            # Name and Date on same line
            if 'Name' in line and 'Date' in line:
                # Extract name
                name_match = re.search(r'Name\s*[-–]\s*(.+?)\s+Date', clean_line)
                if name_match:
                    patient['name'] = name_match.group(1).strip()
                # Extract date
                date_match = re.search(r'Date\s*[-–]\s*(.+?)$', clean_line)
                if date_match:
                    patient['date'] = date_match.group(1).strip()

            # Date only
            elif 'Date' in line and 'Name' not in line and 'date' not in patient:
                date_match = re.search(r'Date\s*[-–]\s*(.+?)$', clean_line)
                if date_match:
                    patient['date'] = date_match.group(1).strip()

            # Name only
            elif 'Name' in line and 'Date' not in line and 'name' not in patient:
                name_match = re.search(r'Name\s*[-–]\s*(.+?)$', clean_line)
                if name_match:
                    patient['name'] = name_match.group(1).strip()

        # Parse Age and Sex (can be on same line or separate lines)
        for line in lines[:8]:
            clean_line = self.clean_markdown(line)

            # Age and Sex on same line
            if 'Age' in line and 'Sex' in line:
                # Extract age
                age_match = re.search(r'Age\s*[-–]\s*(\d+)\s*years', clean_line)
                if age_match:
                    patient['age'] = int(age_match.group(1))
                # Extract sex
                sex_match = re.search(r'Sex\s*[-–]\s*(\w+)', clean_line)
                if sex_match:
                    patient['sex'] = sex_match.group(1).strip()

            # Age only
            elif 'Age' in line and 'Sex' not in line and 'age' not in patient:
                age_match = re.search(r'Age\s*[-–]\s*(\d+)\s*years', clean_line)
                if age_match:
                    patient['age'] = int(age_match.group(1))

            # Sex only
            elif 'Sex' in line and 'Age' not in line and 'sex' not in patient:
                sex_match = re.search(r'Sex\s*[-–]\s*(\w+)', clean_line)
                if sex_match:
                    patient['sex'] = sex_match.group(1).strip()

        # Profession
        for line in lines[:10]:
            if 'Profession' in line and 'Sex' not in line:
                clean_line = self.clean_markdown(line)
                prof_match = re.search(r'Profession\s*[-–]\s*(.+?)$', clean_line)
                if prof_match:
                    patient['profession'] = prof_match.group(1).strip()
                    break

        # Family information
        family = {}

        # Family status
        family_match = re.search(r'Family\s*[-–]\s*(\w+)', content)
        if family_match:
            family['hasFamily'] = family_match.group(1).strip().lower() in ['yes', 'true']

        # Married
        married_match = re.search(r'Married\s*[-–]\s*([^\n*]+?)(?:\*\*|$)', content)
        if married_match:
            family['married'] = self.clean_markdown(married_match.group(1))

        # Children
        children_match = re.search(r'Children\s*[-–]\s*([^\n*]+?)(?:\*\*|$)', content)
        if children_match:
            family['children'] = self.clean_markdown(children_match.group(1))

        if family:
            patient['family'] = family

        # Birth place
        birth_match = re.search(r'Born in\s*[-–]?\s*([^\n*]+?)(?:\*\*|$)', content)
        if birth_match:
            patient['birthPlace'] = self.clean_markdown(birth_match.group(1))

        # Pets
        pets_match = re.search(r'Pets\s*[-–]\s*([^\n*]+?)(?:\*\*|$)', content)
        if pets_match:
            patient['pets'] = self.clean_markdown(pets_match.group(1))

        # Email
        email_match = re.search(r'Email\s*[-–:]\s*([^\s\n]+@[^\s\n]+)', content)
        if email_match:
            patient['email'] = email_match.group(1).strip()

        # Phone
        phone_match = re.search(r'Phone\s*[-–:]\s*([^\n*]+?)(?:\*\*|$)', content)
        if phone_match:
            patient['phone'] = self.clean_markdown(phone_match.group(1))

        return patient

    def parse_consultation_info(self, content: str) -> Dict[str, Any]:
        """Extract consultation and medical history information"""
        consultation = {}

        # Present complaint - improved multi-line extraction
        complaint_match = re.search(
            r'\*\*Present complaint\*\*\s*\n\s*\*\*([^*]+?)\*\*',
            content,
            re.DOTALL
        )
        if complaint_match:
            consultation['presentComplaint'] = self.clean_markdown(complaint_match.group(1))

        # COVID history
        covid_matches = re.findall(
            r'(No Covid[^*\n]*|Covid positive[^*\n]*|No [Vv]accine[^*\n]*|[0-9]+\s*dose[^*\n]*)',
            content,
            re.IGNORECASE
        )
        if covid_matches:
            consultation['covidHistory'] = self.clean_markdown(', '.join(covid_matches))

        # TM practice
        tm_match = re.search(r'TM\s*[-–]([^*\n]+?)(?:\*\*|$)', content)
        if tm_match:
            consultation['tmPractice'] = self.clean_markdown(tm_match.group(1))

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
            'pulse': r'Pulse\s*[-–]\s*([^\n*]+?)(?:\*\*|Bowel|$)',
            'bowel': r'Bowel\s*[-–]\s*([^\n*]+?)(?:\*\*|$)',
            'urination': r'Urination\s*[-–]\s*([^\n*]+?)(?:\*\*|Tongue|$)',
            'tongue': r'Tongue\s*[-–]\s*([^\n*]+?)(?:\*\*|$)',
            'sleep': r'Sleep\s*[-–]\s*([^\n*]+?)(?:\*\*|Hunger|$)',
            'hunger': r'Hunger\s*[-–]\s*([^\n*]+?)(?:\*\*|$)',
            'thirst': r'Thirst\s*[-–]\s*([^\n*]+?)(?:\*\*|Menstruation|$)',
            'menstruation': r'Menstruation\s*[-–]\s*([^\n*]+?)(?:\*\*|$)'
        }

        for key, pattern in vitals_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                assessment['vitals'][key] = self.clean_markdown(match.group(1))

        # Lifestyle
        lifestyle_patterns = {
            'dailyRoutine': r'Daily routine\s*[-–]\s*([^\n*]+?)(?:\*\*|$)',
            'smoking': r'Smoking\s*[-–]\s*([^\n*]+?)(?:\*\*|Alcohol|$)',
            'alcohol': r'Alcohol\s*[-–]\s*([^\n*]+?)(?:\*\*|Exercise|$)',
            'exercise': r'Exercise\s*[-–]\s*([^\n*]+?)(?:\*\*|Emotions|$)',
            'emotions': r'Emotions\s*[-–]\s*([^\n*]+?)(?:\*\*|$)'
        }

        for key, pattern in lifestyle_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                assessment['lifestyle'][key] = self.clean_markdown(match.group(1))

        # Food
        food_patterns = {
            'hoteling': r'Food\s*[-–]\s*([^\n*]+?)(?:\*\*|Oil|$)',
            'oils': r'Oil\s*[-–]\s*([^\n*]+?)(?:\*\*|$)',
            'breakfast': r'Breakfast\s*[-–]\s*([^\n*]+?)(?:\*\*|Lunch|$)',
            'lunch': r'Lunch\s*[-–]\s*([^\n*]+?)(?:\*\*|Dinner|$)',
            'dinner': r'Dinner\s*[-–]\s*([^\n*]+?)(?:\*\*|Fruits|$)',
            'fruits': r'Fruits\s*[-–]\s*([^\n*]+?)(?:\*\*|$)'
        }

        for key, pattern in food_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                assessment['lifestyle']['food'][key] = self.clean_markdown(match.group(1))

        # Ayurvedic Assessment
        ayur_patterns = {
            'prakruti': r'Prakruti\s*[-–]\s*([^\n*]+?)(?:\*\*|Vikruti|$)',
            'vikruti': r'Vikruti\s*[-–]\s*([^\n*]+?)(?:\*\*|Dosha|$)',
            'dosha': r'Dosha\s*[-–]\s*([^\n*]+?)(?:\*\*|Dushya|$)',
            'dushya': r'Dushya\s*[-–]\s*([^\n*]+?)(?:\*\*|$)'
        }

        for key, pattern in ayur_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                assessment['ayurvedicAssessment'][key] = self.clean_markdown(match.group(1))

        return assessment

    def parse_treatment(self, content: str) -> Dict[str, Any]:
        """Extract treatment recommendations with improved shamana parsing"""
        treatment = {
            'shamana': [],
            'panchakarma': [],
            'additionalAdvice': []
        }

        # Shamana (Internal Medicine) - improved extraction
        shamana_section = re.search(
            r'\*\*Shamana.*?\*\*\s*\n(.*?)(?=\*\*(?:Advise|Panchakarma|Avoid))',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if shamana_section:
            shamana_text = shamana_section.group(1)
            # Match numbered items with medicine and dosage
            medicine_lines = re.findall(
                r'\d+\.\s*\*\*([^*]+?)\*\*',
                shamana_text
            )

            for medicine_text in medicine_lines:
                medicine_text = self.clean_markdown(medicine_text)
                # Split on dash/hyphen to separate medicine name from dosage
                if '–' in medicine_text or '-' in medicine_text:
                    parts = re.split(r'\s*[-–]\s*', medicine_text, maxsplit=1)
                    medicine_name = parts[0].strip()
                    dosage = parts[1].strip() if len(parts) > 1 else ""

                    treatment['shamana'].append({
                        'medicine': medicine_name,
                        'dosage': dosage
                    })
                else:
                    # No clear separator, put everything as medicine
                    treatment['shamana'].append({
                        'medicine': medicine_text.strip(),
                        'dosage': ""
                    })

        # Panchakarma
        panchakarma_section = re.search(
            r'\*\*Panchakarma\*\*\s*\n(.*?)(?=\*\*(?:Avoid|Take))',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if panchakarma_section:
            panchakarma_text = panchakarma_section.group(1)
            panchakarma_lines = re.findall(r'\d+\.\s*\*\*([^*]+?)\*\*', panchakarma_text)
            for therapy in panchakarma_lines:
                treatment['panchakarma'].append(self.clean_markdown(therapy))

        # Additional Advice
        advice_patterns = [
            r'Aroma therapy[^\n*]+',
            r'Chanting of mantras[^\n*]+',
            r'Advice to do Moolabandha',
            r'Use of Asafetida[^\n*]+',
            r'Drink medicated water[^\n*]+'
        ]

        for pattern in advice_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                cleaned = self.clean_markdown(match)
                if cleaned:
                    treatment['additionalAdvice'].append(cleaned)

        return treatment

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
                'version': '2.0',
                'language': 'en',
                'originalFile': os.path.basename(filepath)
            }
        }

        return consultation_data

    def convert_all_files(self, input_dir: str = '.', output_dir: str = './converted2') -> None:
        """Convert all consultation markdown files to JSON"""
        os.makedirs(output_dir, exist_ok=True)

        # Find all consultation files
        consultation_files = [f for f in os.listdir(input_dir)
                            if f.endswith('.md') and
                            'consultation' not in f.lower() and
                            'template' not in f.lower() and
                            'readme' not in f.lower()]

        print(f"Found {len(consultation_files)} consultation files to convert")
        print(f"Output directory: {output_dir}")
        print()

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
                import traceback
                traceback.print_exc()

        print(f"\nConversion complete! Check the '{output_dir}' directory for results.")

def main():
    parser = ConsultationParserV2()
    parser.convert_all_files()

if __name__ == "__main__":
    main()
