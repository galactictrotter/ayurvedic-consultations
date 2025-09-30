# frozen_string_literal: true
require "json"
require "i18n"
require "tilt"
require "grover"
require "time"
require "active_support"
require "active_support/core_ext/time"

ROOT = File.expand_path("../..", __dir__)
I18n.load_path += Dir[File.join(ROOT, "app", "locales", "*.yml")]
I18n.available_locales = %i[en fr]
I18n.default_locale = :en

def t(key, lang)
  # If lang is "bi", default to "en" for UI labels
  effective_lang = lang == "bi" ? "en" : lang
  I18n.t(key, locale: effective_lang.to_sym, default: key)
end

def pick_lang(val, lang)
  case val
  when Hash
    val[lang] || val["en"] || val["fr"] || ""
  when String
    val
  else
    ""
  end
end

def fmt_date(str, lang)
  return "" if str.nil? || str.empty?
  # Handle DD/MM/YYYY format
  begin
    if str.match?(/^\d{2}\/\d{2}\/\d{4}$/)
      day, month, year = str.split("/")
      t = Time.new(year.to_i, month.to_i, day.to_i)
    else
      t = Time.parse(str)
    end

    if lang == "fr"
      t.strftime("%d/%m/%Y")  # e.g., 31/12/2025
    else
      t.strftime("%B %-d, %Y") # e.g., December 31, 2025
    end
  rescue
    str # Return original if parsing fails
  end
end

template = Tilt::ERBTemplate.new(File.join(ROOT, "app", "templates", "report.html.erb"))

mode = (ARGV[0] || "bi") # "en", "fr", or "bi"
abort("mode must be en|fr|bi") unless %w[en fr bi].include?(mode)

Dir[File.join(ROOT, "data", "*.json")].sort.each do |path|
  client = JSON.parse(File.read(path))
  html = template.render(
    Object.new,
    client: client,
    lang: mode,
    t: method(:t),
    pick_lang: method(:pick_lang),
    fmt_date: method(:fmt_date)
  )

  basename = File.basename(path, ".json")
  date = Time.now.strftime("%Y-%m-%d")
  suffix = { "en" => "EN", "fr" => "FR", "bi" => "Bilingual" }[mode]
  out = File.join(ROOT, "app", "output", "#{date}_#{basename}_#{suffix}.pdf")

  begin
    grover = Grover.new(html)
    pdf = grover.to_pdf(
      format: 'A4',
      margin: {
        top: '0.5in',
        bottom: '0.5in',
        left: '0.5in',
        right: '0.5in'
      },
      print_background: true,
      prefer_css_page_size: true,
      timeout: 60000  # 60 second timeout
    )
    File.write(out, pdf)
    puts "✓ Wrote #{out}"
  rescue => e
    puts "✗ Error generating #{basename}: #{e.message}"
  end
end
