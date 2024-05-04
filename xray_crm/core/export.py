# create a pdf for a record

from .models import Patient, Doctor, Record, PatientFile, ReportFile
from fpdf import FPDF

def generate_pdf(record_id):
    record = Record.objects.get(id=record_id)
    patient = record.patient
    doctor = record.doctor
    
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    # add a table
    pdf.cell(200, 10, f'Patient Record - {record.created_at}', 0, 1, 'C')
    pdf.cell(200, 10, '', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, 'Patient', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, f'Name: {patient.user.first_name} {patient.user.last_name}', 0, 1, 'L')
    pdf.cell(200, 10, f'Email: {patient.user.email}', 0, 1, 'L')

    # doctor info
    pdf.cell(200, 10, '', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, 'Doctor', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, f'Name: {doctor.user.first_name} {doctor.user.last_name}', 0, 1, 'L')
    pdf.cell(200, 10, f'Email: {doctor.user.email}', 0, 1, 'L')
    pdf.cell(200, 10, '', 0, 1, 'C')
    pdf.cell(200, 10, 'Doctor Note', 0, 1, 'L')

    # add a line
    pdf.line(10, 70, 200, 70)
    pdf.cell(200, 10, record.doctor_note, 0, 1, 'L')

    for patient_file in record.patientfile_set.all():
        pdf.cell(200, 10, '', 0, 1, 'C')
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 10, f'Patient File {patient_file.id}', 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        #pdf.cell(200, 10, f'File: {patient_file.file}', 0, 1, 'L')
        # add an image to the pdf
        pdf.image(patient_file.file.path, x = None, y = None, w = 100, h = 100, type = '', link = '')
        for report_file in patient_file.reportfile_set.all():
            label = ReportFile.LABEL_CHOICES[report_file.label - 1][1]
            pdf.cell(200, 10, f'Label: {label}', 0, 1, 'L')
            pdf.cell(200, 10, f'Member: {report_file.member}', 0, 1, 'L')
            pdf.cell(200, 10, f'Hardware: {report_file.hardware}', 0, 1, 'L')
            pdf.cell(200, 10, f'Modified At: {report_file.modified_at}', 0, 1, 'L')


    filename = f'patient_files/{record_id}.pdf'   
    pdf.output(filename)
    print(f'PDF generated: {filename}')
    return filename