from fpdf import FPDF


class PDF(FPDF):

    def header(self):
        # Logo
        self.image('logo/Gitale ENG Logo - Pink on White-1.png', 10, 8, 45)

        # font
        self.add_font('DejaVu1', '', 'dejavu-fonts-ttf-2.37/ttf/DejaVuSerif.ttf')
        self.set_font('DejaVu1', '', 30)
        self.set_font('DejaVu1', '', 30)

        # Padding
        self.cell(80)

        # Title
        self.cell(34, 40, 'Gitale - Flowers', ln=1, align='C')

        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Set position of the footer
        self.set_y(-15)

        # set font
        self.set_font('Arial', 'I', 8)

        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')
