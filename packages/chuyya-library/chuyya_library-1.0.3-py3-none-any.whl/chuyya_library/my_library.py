from fpdf import FPDF
import os

class InvoicePDF(FPDF):
    def __init__(self, logo_path=None, font_path=None):
        super().__init__()
        self.logo_path = logo_path  # Path to the logo image

    def header(self):
        margin = 10

        # Draw a square border (rectangle) around the page
        self.set_line_width(0.5)
        self.rect(margin, margin, 210 - 2 * margin, 297 - 2 * margin)
        
        # Set a built-in font like Arial
        self.set_font("Arial", "B", 16)

        # Add logo if specified
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, x=75, y=15, w=60)  # Center logo
        else:
            self.cell(0, 20, "LOGO MISSING", ln=True, align="C")
        
        
        # Add title and other headers
        self.set_y(65)
        self.cell(0, 10, "CASPER LOGISTICS", ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, "359, Crumlin Road, Dublin -12, D12E9C7", ln=True, align="C")
        self.set_font("Arial", "", 14)
        self.cell(0, 20, "SHIPMENT INVOICE", ln=True, align="C")
        self.ln(5)

    def add_invoice_details(self, shipment_details):
        self.set_font("Arial", "", 10)  # Set font for the section
        label_width = 60
        line_height = 6
        page_width = 210
        margin = 10
        usable_width = page_width - 2 * margin - label_width  # Adjust usable width for wrapping
    
        fields = [
            ("Shipment ID:", shipment_details.get("shipment_id", "")),
            ("Sender Name:", shipment_details.get("sender_name", "")),
            ("Sender Email:", shipment_details.get("sender_email", "")),
            ("Receiver Name:", shipment_details.get("receiver_name", "")),
            ("Receiver Email:", shipment_details.get("receiver_email", "")),
            ("From Address:", shipment_details.get("from_address", "")),
            ("To Address:", shipment_details.get("to_address", "")),
            ("Status:", shipment_details.get("status", "").title()),
            ("Shipment Date:", shipment_details.get("shipment_date", "")),
            ("Expected Delivery Date:", shipment_details.get("delivery_date", "")),
            ("Weight (Pounds):", str(shipment_details.get("weight", ""))),
            ("Dimensions (Meters):", shipment_details.get("dimensions", "")),
            ("Cost (EUR):", f"{shipment_details.get('cost', '')} EUR"),
            ("Insurance (EUR):", f"{shipment_details.get('insurance', '')} EUR"),
            ("Fragile:", "Yes" if shipment_details.get("fragile") else "No"),
            ("Additional Notes:", shipment_details.get("additional_notes", "")),
            (
                "Uploaded Files:",
                "\n".join([
                    os.path.basename(file) if isinstance(file, str) else os.path.basename(file.get("file_name", ""))
                    for file in shipment_details.get("file_uploads", [])
                ]),  # Extract file names and join with newlines
            ),
        ]
    
        for label, value in fields:
            x_position = margin
            self.set_x(x_position)
    
            # Draw the label
            self.set_text_color(81, 45, 168)  # Dark purple for labels
            self.cell(label_width, line_height, label, border=0)
    
            # Draw the value using multi_cell for wrapping
            self.set_text_color(0, 0, 0)  # Black for values
            current_x = self.get_x()
            current_y = self.get_y()
    
            # Use multi_cell for wrapping long text
            self.multi_cell(usable_width, line_height, str(value), border=0)
    
            # Reset cursor to the next line only if multi_cell was used
            self.set_xy(current_x, max(current_y + line_height, self.get_y()))
            self.ln(2)  # Add spacing between rows

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", "", 8)  # Use Cavolini font for footer
        self.cell(0, 10, "Thank you for choosing Casper Logistics!", 0, 0, "C")


def generate_invoice(shipment_details, logo_path=None):
    # Adjust cost and insurance if the shipment is fragile
    if shipment_details.get("fragile"):
        shipment_details["cost"] = round(float(shipment_details.get("cost", 0)) + 30, 2)
        shipment_details["insurance"] = round(float(shipment_details.get("insurance", 0)) + 10, 2)

    pdf = InvoicePDF(logo_path=logo_path)
    pdf.add_page()
    pdf.add_invoice_details(shipment_details)

    # Return the PDF as a binary stream
    return pdf.output(dest="S").encode("latin1")
