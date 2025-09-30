#!/usr/bin/env ruby
# frozen_string_literal: true

require 'json'
require 'fileutils'
require 'date'

##
# Conversion script to transform legacy Ayurvedic consultation markdown files
# to structured JSON format with standardized recommendations.
class ConsultationParser
  def initialize
    # Load standard recommendations
    standard_recs_file = File.read('standard-recommendations.json')
    @standard_recs = JSON.parse(standard_recs_file)['standardRecommendations']
  end

  def parse_patient_info(content)
    patient = {}

    # Get first 10 lines for basic info
    lines = content.split("\n")[0..9]

    lines.each do |line|
      cleaned_line = line.gsub(/\*/, '').strip

      # Name
      if cleaned_line.include?('Name') && cleaned_line.include?('–')
        name_match = cleaned_line.match(/Name\s*[-–]\s*([^–]+?)(?:\s+Date|$)/)
        patient['name'] = name_match[1].strip if name_match
      end

      # Date
      if cleaned_line.include?('Date') && cleaned_line.include?('–')
        date_match = cleaned_line.match(/Date\s*[-–]\s*([^–]+?)(?:\s+|$)/)
        patient['date'] = date_match[1].strip if date_match
      end

      # Age
      if cleaned_line.include?('Age') && cleaned_line.include?('years')
        age_match = cleaned_line.match(/Age\s*[-–]\s*(\d+)\s*years/)
        patient['age'] = age_match[1].to_i if age_match
      end

      # Sex
      if cleaned_line.include?('Sex') && cleaned_line.include?('–')
        sex_match = cleaned_line.match(/Sex\s*[-–]\s*([^–]+?)(?:\s+|$)/)
        patient['sex'] = sex_match[1].strip if sex_match
      end

      # Profession
      if cleaned_line.include?('Profession') && cleaned_line.include?('–')
        prof_match = cleaned_line.match(/Profession\s*[-–]\s*([^–]+?)(?:\s+|$)/)
        patient['profession'] = prof_match[1].strip if prof_match
      end
    end

    # Family information
    family = {}

    family_text = extract_section(content, /Family.*?(?=Married|Present|$)/m)
    family['hasFamily'] = family_text&.include?('Yes') || false

    married_text = extract_section(content, /Married.*?(?=Children|Present|$)/m)
    if married_text
      family['married'] = married_text.gsub('Married –', '').strip
    end

    children_text = extract_section(content, /Children.*?(?=Born|Present|$)/m)
    if children_text
      family['children'] = children_text.gsub('Children –', '').strip
    end

    patient['family'] = family unless family.empty?

    # Birth place
    birth_match = content.match(/Born in\s*[-–]?\s*([^\n]+)/)
    patient['birthPlace'] = birth_match[1].strip if birth_match

    # Pets
    pets_match = content.match(/Pets\s*[-–]\s*([^\n]+)/)
    patient['pets'] = pets_match[1].strip if pets_match

    # Email
    email_match = content.match(/Email\s*[-–:]\s*([^\s\n]+@[^\s\n]+)/)
    patient['email'] = email_match[1].strip if email_match

    # Phone
    phone_match = content.match(/Phone\s*[-–:]\s*([^\n]+)/)
    patient['phone'] = phone_match[1].strip if phone_match

    patient
  end

  def extract_section(content, pattern)
    match = content.match(pattern)
    match ? match[0] : nil
  end

  def parse_consultation_info(content)
    consultation = {}

    # Present complaint
    complaint_match = content.match(/Present complaint\*\*\s*\n(.*?)(?=\*\*|No Covid|TM|$)/m)
    consultation['presentComplaint'] = clean_text(complaint_match[1]) if complaint_match

    # COVID history
    covid_matches = content.scan(/(No Covid[^*\n]*|Covid positive[^*\n]*|No vaccine[^*\n]*|vaccine[^*\n]*)/i)
    unless covid_matches.empty?
      consultation['covidHistory'] = covid_matches.flatten.join(', ')
    end

    # TM practice
    tm_match = content.match(/TM.*?(?=\n|$)/)
    consultation['tmPractice'] = tm_match[0] if tm_match

    consultation
  end

  def parse_assessment(content)
    assessment = {
      'vitals' => {},
      'lifestyle' => { 'food' => {} },
      'ayurvedicAssessment' => {}
    }

    # Vitals patterns
    vitals_patterns = {
      'pulse' => /Pulse\s*[-–]\s*([^\n]+)/i,
      'bowel' => /Bowel\s*[-–]\s*([^\n]+)/i,
      'urination' => /Urination\s*[-–]\s*([^\n]+)/i,
      'tongue' => /Tongue\s*[-–]\s*([^\n]+)/i,
      'sleep' => /Sleep\s*[-–]\s*([^\n]+)/i,
      'hunger' => /Hunger\s*[-–]\s*([^\n]+)/i,
      'thirst' => /Thirst\s*[-–]\s*([^\n]+)/i,
      'menstruation' => /Menstruation\s*[-–]\s*([^\n]+)/i
    }

    vitals_patterns.each do |key, pattern|
      match = content.match(pattern)
      assessment['vitals'][key] = match[1].strip if match
    end

    # Lifestyle patterns
    lifestyle_patterns = {
      'dailyRoutine' => /Daily routine\s*[-–]\s*([^\n]+)/i,
      'smoking' => /Smoking\s*[-–]\s*([^\n]+)/i,
      'alcohol' => /Alcohol\s*[-–]\s*([^\n]+)/i,
      'exercise' => /Exercise\s*[-–]\s*([^\n]+)/i,
      'emotions' => /Emotions\s*[-–]\s*([^\n]+)/i
    }

    lifestyle_patterns.each do |key, pattern|
      match = content.match(pattern)
      assessment['lifestyle'][key] = match[1].strip if match
    end

    # Food patterns
    food_patterns = {
      'hoteling' => /Food\s*[-–]\s*([^\n]+)/i,
      'oils' => /Oil\s*[-–]\s*([^\n]+)/i,
      'breakfast' => /Breakfast\s*[-–]\s*([^\n]+)/i,
      'lunch' => /Lunch\s*[-–]\s*([^\n]+)/i,
      'dinner' => /Dinner\s*[-–]\s*([^\n]+)/i,
      'fruits' => /Fruits\s*[-–]\s*([^\n]+)/i
    }

    food_patterns.each do |key, pattern|
      match = content.match(pattern)
      assessment['lifestyle']['food'][key] = match[1].strip if match
    end

    # Ayurvedic Assessment patterns
    ayur_patterns = {
      'prakruti' => /Prakruti\s*[-–]\s*([^\n]+)/i,
      'vikruti' => /Vikruti\s*[-–]\s*([^\n]+)/i,
      'dosha' => /Dosha\s*[-–]\s*([^\n]+)/i,
      'dushya' => /Dushya\s*[-–]\s*([^\n]+)/i
    }

    ayur_patterns.each do |key, pattern|
      match = content.match(pattern)
      assessment['ayurvedicAssessment'][key] = match[1].strip if match
    end

    assessment
  end

  def parse_treatment(content)
    treatment = {
      'shamana' => [],
      'panchakarma' => [],
      'additionalAdvice' => []
    }

    # Shamana (Internal Medicine)
    shamana_section = extract_section(content, /Shamana.*?(?=Panchakarma|Advice|Avoid)/m)
    if shamana_section
      medicine_lines = shamana_section.scan(/(\d+)\.\s*\*\*(.*?)\*\*/)
      medicine_lines.each do |_, medicine_text|
        if medicine_text.include?('–')
          parts = medicine_text.split('–', 2)
          medicine_name = parts[0].strip
          dosage = parts.length > 1 ? parts[1].strip : ""
          treatment['shamana'] << {
            'medicine' => medicine_name,
            'dosage' => dosage
          }
        end
      end
    end

    # Panchakarma
    panchakarma_section = extract_section(content, /Panchakarma\*\*(.*?)(?=\*\*Advice|\*\*Avoid)/m)
    if panchakarma_section
      panchakarma_lines = panchakarma_section.scan(/(\d+)\.\s*\*\*(.*?)\*\*/)
      panchakarma_lines.each do |_, therapy|
        treatment['panchakarma'] << therapy.strip
      end
    end

    # Additional Advice
    advice_patterns = [
      /Aroma therapy[^\n]*/i,
      /Chanting of mantras[^\n]*/i,
      /Advice to do Moolabandha/i,
      /Use of Asafetida[^\n]*/i,
      /Drink medicated water[^\n]*/i
    ]

    advice_patterns.each do |pattern|
      matches = content.scan(pattern)
      treatment['additionalAdvice'].concat(matches.flatten)
    end

    treatment
  end

  def clean_text(text)
    return '' unless text

    # Remove markdown formatting
    text = text.gsub(/\*\*/, '')
    # Remove extra whitespace
    text = text.gsub(/\s+/, ' ')
    text.strip
  end

  def parse_file(filepath)
    content = File.read(filepath, encoding: 'utf-8')

    consultation_data = {
      'patient' => parse_patient_info(content),
      'consultation' => parse_consultation_info(content),
      'assessment' => parse_assessment(content),
      'treatment' => parse_treatment(content),
      'standardRecommendations' => @standard_recs,
      'metadata' => {
        'createdAt' => DateTime.now.iso8601,
        'lastModified' => DateTime.now.iso8601,
        'version' => '1.0',
        'language' => 'en',
        'originalFile' => File.basename(filepath)
      }
    }

    consultation_data
  end

  def convert_all_files(input_dir: '.', output_dir: './converted')
    FileUtils.mkdir_p(output_dir)

    # Find all consultation files
    consultation_files = Dir.entries(input_dir).select do |f|
      f.end_with?('.md') &&
        !f.downcase.include?('consultation') &&
        !f.downcase.include?('template') &&
        !f.downcase.include?('readme')
    end

    puts "Found #{consultation_files.length} consultation files to convert"

    consultation_files.each do |filename|
      begin
        puts "Converting #{filename}..."
        filepath = File.join(input_dir, filename)
        consultation_data = parse_file(filepath)

        # Create output filename
        base_name = File.basename(filename, '.md')
        output_filename = "#{base_name}.json"
        output_path = File.join(output_dir, output_filename)

        # Save JSON
        File.write(output_path, JSON.pretty_generate(consultation_data))

        puts "✓ Converted to #{output_filename}"

      rescue => e
        puts "✗ Error converting #{filename}: #{e.message}"
      end
    end

    puts "\nConversion complete! Check the '#{output_dir}' directory for results."
  end
end

# Main execution
if __FILE__ == $0
  parser = ConsultationParser.new
  parser.convert_all_files
end