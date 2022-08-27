from appsettings_manager import get_app_settings
import requests
from models import Child
from sms_sender import SmsSender #https://realpython.com/python-requests/
from email_sender import EmailSender
from models import AppointmentReminder, HealhCenter, Parent, VaccinationAppointment, Vaccine

class AppointmentReminderManager:
    def __init__(self, email_sender: EmailSender, sms_sender: SmsSender):
        app_settings = get_app_settings()
        self.base_url = app_settings['RestApi']['BaseUrl']
        self.path = app_settings['RestApi']['AppointmentReminderEndpoint']
        self.notify_sent_reminders_path = app_settings['RestApi']['NotifySentRemindersEndpoint']
        self.email_sender = email_sender
        self.sms_sender = sms_sender

    def get_reminders_for_today(self):
        """Function to get the Appointment Reminders that must be send today"""
        endpoint = f'{self.base_url}{self.path}'

        #TODO: Ver sobre autenticacion, quiza poner una key o algo, pensarlo bien
        response = requests.get(endpoint, verify=False)
        reminders = response.json()['value']['vaccinationAppointmentReminders']
       

        reminders_to_return = []
        for reminder in reminders:
            vaccination_appointment_json = reminder['vaccinationAppointment']
            parent_json = reminder['parent']
            child_json = vaccination_appointment_json['child']
            health_center_json = vaccination_appointment_json['healthCenter']
            #parent = Parent(parent_json['parentId'], parent_json['firstname'], parent_json['email'])
            parent = Parent(parent_json['parentId'], None, None)
            health_center = HealhCenter(health_center_json['healthCenterId'], health_center_json['name'], None)
            child = Child(child_json['childId'], child_json['fullname'], child_json['dni'])

            #region Map Vaccines
            vaccines = []
            for vaccine in vaccination_appointment_json['vaccines']:
                vaccines.append(Vaccine(vaccine))
            #endregion
            
            vaccination_appoinment = VaccinationAppointment(vaccination_appointment_json['vaccinationAppointmentId'], vaccination_appointment_json['appointmentDateTime'], child, health_center, vaccines)

            reminders_to_return.append(AppointmentReminder(reminder['reminderId'], reminder['via'], reminder['sendDate'], parent, vaccination_appoinment))
        
        print("Reminders: ", reminders_to_return)
        return reminders_to_return

    def generate_html_email_message(self, reminder: AppointmentReminder):
        """Function that generate the HTML Email Message based on the information of the reminder parameter
        :param AppointmentReminder reminder: the reminder that contains the info to generate the HTML Email Message
        """
        style = """<style>
        table,
        td,
        div,
        h1,
        p {
            font-family: Arial, sans-serif;
        }

        .table-health-centers, .table-health-centers > td, .table-health-centers > th {
            border: 1px solid black;
        }
    </style>"""

        parent = reminder.parent
        appointment = reminder.vaccination_appointment
        start_date = appointment.appointment_datetime[0:10]
        start_time = appointment.appointment_datetime[11:16]

        vaccines_list_html = "<ul>"
        for vaccine in appointment.vaccines:
            vaccines_list_html += f"<li>{vaccine.name}</li>"
        vaccines_list_html += "</ul>"

        health_centers_table_html = '''<table style="border: 1px solid black; border-collapse: collapse; padding: 5px; margin-top: 5px;">
        <tr>
            <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">Nombre</th>
            <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">Dirección</th>
        </tr>'''
        for health_center in [appointment.health_center]:
            health_centers_table_html += f"""<tr>
                                                <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">{health_center.name}</th>
                                                <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">{health_center.address}</th>
                                            </tr>"""
        health_centers_table_html += "</table>"

        html_email_to_return = f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <title></title>
    <!--[if mso]>
    <noscript>
      <xml>
        <o:OfficeDocumentSettings>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
      </xml>
    </noscript>
    <![endif]-->
    {style}
</head>

<body style="margin:0;padding:0;">
    <table role="presentation"
        style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
        <tr>
            <td align="center" style="padding:0;">
                <table role="presentation"
                    style="width:800px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
                    <tr id="banner_image_section">
                        <td align="center" style="background:#277BC0;">
                            <h1 style="color: white;">MINSA</h1>
                        </td>
                    </tr>
                    <tr id="main_message_section">
                        <td style="padding:36px 30px 42px 30px;">
                            <table role="presentation"
                                style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                                <tr>
                                    <td style="padding:0 0 6px 0;color:#153643;">
                                        <span>Hola, {parent.name}.</span>
                                        <br>
                                        <br>
                                        <span>Se aproxima tu cita programada para el {start_date} a las {start_time}</span>
                                        <br>
                                        <br>
                                        <span>En esta cita de vacunación se han elegido las siguientes vacunas:</span>
                                        <br>
                                        {vaccines_list_html}
                                        <br>
                                        <span>El centro de salud donde se dará esta cita de vacunación es el
                                            siguiente:</span>
                                        {health_centers_table_html}
                                        <br>
                                        <br>
                                        <br>
                                        <b>Este es un recordatorio del Ministerio de Salud</b>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr id="preguntas_frecuentes_consulta_chat_online_section">
                        <td style="padding:20px;background:#277BC0;">
                            <table role="presentation"
                                style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                                <tr>
                                    <td style="padding:0;width:50%;" align="center">
                                        <p
                                            style="margin:0;font-size:14px;line-height:16px;font-family:Arial,sans-serif;color:#ffffff;">
                                            ¿Necesitas ayuda o tienes alguna duda? Consulta la página de <a
                                                href="https://www.google.com"
                                                style="color:white;text-decoration:underline;">Preguntas frecuentes</a>,
                                            escribenos a <a href="mailto:minsa@gob.pe"
                                                style="color:white;text-decoration:underline;">minsa@gob.pe</a> o
                                            ingresa a nuestro <a
                                                href="https://www.google.com"
                                                style="color:white;text-decoration:underline;">chat en línea.</a>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>"""
        return html_email_to_return
    
    
    def generate_sms_message(self, reminder: AppointmentReminder):
        sms_to_return = 'Hola, este es un SMS'
        return sms_to_return

    def send_reminders(self, reminders: list):
        """Function that receives a list of reminders and send them one by one
        :param list reminders: the reminders that must be send
        """
        sent_reminders = []
        for reminder in reminders:
            # if reminder.id != 1:
            #     break

            if reminder.via == "Email":
                subject = f"Próxima Cita de Vacunación"
                message = self.generate_html_email_message(reminder)
                print(f"Se enviará el recordatorio de cita de vacunación {reminder.id} al padre {reminder.parent.name} con correo {reminder.parent.email}")
                with open(f'email_appointmnent_{reminder.id}.html', 'w', encoding='utf-8') as file:
                    file.write(message)
                to = "u201810503@upc.edu.pe" #reminder.parent.email
                email_was_sent = self.email_sender.send_email(to, subject, message, "text/html")
                if email_was_sent:
                    sent_reminders.append(reminder)
            elif reminder.via == "SMS":
                message = self.generate_sms_message(reminder)
                phone_number = "1523625415" #reminder.parent.email
                print(f"Se enviará el recordatorio de campaña {reminder.id} al padre {reminder.parent.name} a su telefono {phone_number}")
                sms_was_sent = self.sms_sender.send_sms(phone_number, message)
                if sms_was_sent:
                    sent_reminders.append(reminder)
            else:
                print(f"Invalid via for reminder {reminder.id}")
                continue

        #self.notify_sent_reminders(reminders)
        return reminders
      

def test_appointment_reminder_manager():
    email_sender = EmailSender()
    sms_sender = SmsSender()
    reminder_manager = AppointmentReminderManager(email_sender, sms_sender)
    reminders_to_send = reminder_manager.get_reminders_for_today()

    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_appointment_reminder_manager()