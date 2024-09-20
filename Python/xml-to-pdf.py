import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Path to the directory containing XML files and output directory for PDFs
xml_directory = '/home/vannaboth/OCS-INVENTORY/Python/xml_files'
output_directory = '/home/vannaboth/OCS-INVENTORY/Python/pdf_output'

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to convert a single XML file to PDF
def convert_xml_to_pdf(input_xml, output_pdf):
    # Parse the XML file
    tree = ET.parse(input_xml)
    root = tree.getroot()

    # Create PDF using ReportLab
    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    margin = 72  # 1 inch margin
    y_position = height - margin
    line_height = 14
    section_spacing = 20  # Space between sections

    # Set up basic fonts and layout
    pdf.setFont("Helvetica", 12)

    # Function to add text with word wrapping
    def draw_text(x, y, text, max_width):
        lines = []
        words = text.split()
        current_line = ''
        for word in words:
            test_line = f"{current_line} {word}".strip()
            width_test_line = pdf.stringWidth(test_line, 'Helvetica', 12)
            if width_test_line <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        for line in lines:
            pdf.drawString(x, y, line)
            y -= line_height
        return y

    content_element = root.find('CONTENT')

    # Ensure CONTENT and HARDWARE are found
    if content_element is not None:
        hardware_element = content_element.find('HARDWARE')
        if hardware_element is not None:
            section_title = hardware_element.tag
            pdf.setFont('Helvetica-Bold', 14)
            y_position = draw_text(margin, y_position, section_title, width - 2 * margin)
            y_position -= section_spacing  # Space after section title
            pdf.setFont('Helvetica', 12)

            # Now iterate over the children of HARDWARE
            for child in hardware_element:
                child_title = child.tag
                child_text = child.text.strip() if child.text is not None else 'No Content'
                y_position = draw_text(margin, y_position, f"{child_title}: {child_text}", width - 2 * margin)
                y_position -= section_spacing  # Space after each item

                # Handle page overflow
                if y_position < margin:
                    pdf.showPage()
                    pdf.setFont('Helvetica', 12)
                    y_position = height - margin

    
    # Save the PDF
    pdf.save()
    print(f"PDF has been generated: {output_pdf}")

# Loop through all XML files in the directory
for filename in os.listdir(xml_directory):
    if filename.endswith('.xml'):
        input_xml = os.path.join(xml_directory, filename)
        output_pdf = os.path.join(output_directory, f'{os.path.splitext(filename)[0]}.pdf')

        # Convert XML to PDF for each file
        try:
            convert_xml_to_pdf(input_xml, output_pdf)
        except ET.ParseError:
            print(f'Error parsing {filename}: Invalid XML')
        except Exception as e:
            print(f'Error processing {filename}: {str(e)}')

print(f'All XML files have been converted to PDF in {output_directory}')
