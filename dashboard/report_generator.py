from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_report(df):

    pdf = SimpleDocTemplate(
        "../reports/security_report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Vehicle Security Report",
            styles["Title"]
        )
    )

    pdf.build(content)

