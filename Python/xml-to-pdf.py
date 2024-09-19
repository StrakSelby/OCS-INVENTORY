import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Path to the directory containing XML files and output directory for PDFs
xml_directory = '/home/OCS-INVENTORY-main/Python/xml_files'
output_directory = '/home/OCS-INVENTORY-main/Python/pdf_output'

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

    # Add title
    title_element = root.find('title')
    title = title_element.text if title_element is not None and title_element.text is not None else "Untitled Document"
    pdf.setFont("Helvetica-Bold", 20)
    y_position = height - margin
    pdf.drawString(margin, y_position, title)
    y_position -= (line_height + section_spacing)  # Space after title

    fields = [
    'BATTERIES', 'BIOS', 'CPUS', 'SOUNDS',
    'STORAGES', 'VIDEOS' , 'HARDWARE'
    ]

    content_element = root.find("CONTENT")

    for field in fields:
        content_field = content_element.find(field)
        #print(f"Looking for field: {field}, Found: {content_element is not None}")
        if content_element is not None:
            for section in content_element:
                section_title = section.tag
                pdf.setFont("Helvetica-Bold", 14)
                y_position = draw_text(margin, y_position, section_title, width - 2 * margin)
                y_position -= section_spacing  # Space after section title
                pdf.setFont("Helvetica", 12)

                for section in content_field:
                    section_title = section.tag
                    section_content = section.text.strip() if section.text is not None else "No Content"
                    y_position = draw_text(margin, y_position, f"{section_title}: {section_content}", width - 2 * margin)
                    y_position -= section_spacing
                

                for child in section:
                    child_title = child.tag
                    child_text = child.text if child.text is not None else "No Content"
                    y_position = draw_text(margin, y_position, f"{child_title}: {child_text}", width - 2 * margin)
                    y_position -= section_spacing  # Space after each item
                    if y_position < margin:
                        pdf.showPage()
                        pdf.setFont("Helvetica", 12)
                        y_position = height - margin
    # Save the PDF
    pdf.save()
    print(f"PDF has been generated: {output_pdf}")

# Loop through all XML files in the directory
for filename in os.listdir(xml_directory):
    if filename.endswith(".xml"):
        input_xml = os.path.join(xml_directory, filename)
        output_pdf = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.pdf")

        # Convert XML to PDF for each file
        try:
            convert_xml_to_pdf(input_xml, output_pdf)
        except ET.ParseError:
            print(f"Error parsing {filename}: Invalid XML")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

print(f"All XML files have been converted to PDF in {output_directory}")
