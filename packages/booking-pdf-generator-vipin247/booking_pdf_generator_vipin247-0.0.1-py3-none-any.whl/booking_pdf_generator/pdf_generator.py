from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_booking_pdf(booking_details):
    # Define the file path for the PDF
    file_name = f"booking_{booking_details['bookingId']}.pdf"
    file_path = os.path.join(os.getcwd(), file_name)

    # Create a canvas object to generate the PDF
    c = canvas.Canvas(file_path, pagesize=letter)

    # Add content to the PDF
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 750, "Booking Confirmation")

    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Booking ID: {booking_details['bookingId']}")
    c.drawString(50, 680, f"Flight Number: {booking_details['flightNumber']}")
    c.drawString(50, 660, f"Departure Time: {booking_details['departureTime']}")
    c.drawString(50, 640, f"Route: {booking_details['origin']} → {booking_details['destination']}")

    # Save the PDF
    c.save()

    return file_path
