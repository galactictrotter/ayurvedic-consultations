# Design Updates Applied

## Margins
- **Changed from:** 18mm/16mm/20mm/16mm (varying margins)
- **Changed to:** 0.5 inch all around (12.7mm uniform)

## Design Tokens (from Plantissima)

### Color Palette
- **Brand Red:** `#D85344` - Used for H2 headings and header border
- **Plantissima Green:** `#65695b` - Used for H3 headings and labels
- **Earthy Olive:** `#7D8B4C` - Used for patient block border and badges
- **Golden Yellow:** `#F2B21A` - Used for bullet points
- **Dark Gray:** `#404040` - Primary text color
- **Medium Gray:** `#6E6E6E` - Secondary text
- **Light Gray:** `#F0F0F0` - Borders
- **Off-White:** `#FCFCFC` - Background tints

### Typography
- **Primary Font:** Gentium Book Plus (serif) - Body, H1, H3
- **Secondary Font:** Merriweather (serif) - H2 headings
- **Font Size:** 11pt body, responsive headings
- **Line Height:** 1.35
- **Letter Spacing:** 0.02rem on headings

### Layout Features
- Border radius: 0.15rem (subtle rounded corners)
- Patient block: Off-white background with earthy olive left border
- Header: Brand red bottom border (2px)
- Golden yellow bullet points for lists
- Proper French typography support

## Files Modified
1. `app/styles/print.css` - Complete redesign with Plantissima tokens
2. `app/templates/report.html.erb` - Added Google Fonts (Gentium Book Plus, Merriweather)
3. `app/scripts/render.rb` - Updated margins to 0.5in

## Usage
Generate PDFs with the new design:
```bash
ruby app/scripts/render.rb bi   # Bilingual
ruby app/scripts/render.rb en   # English only
ruby app/scripts/render.rb fr   # French only
```

## Design Philosophy
The Plantissima design emphasizes:
- Warm, earthy color palette
- Classical serif typography
- Elegant Italian-inspired aesthetics
- Professional medical document appearance
- Print-optimized for high-quality output
