from operator import index
import requests
from appsettings_manager import get_app_settings
from sms_sender import SmsSender #https://realpython.com/python-requests/
from email_sender import EmailSender
from models import DoseReminder, DoseReminderForEmail, Parent, Child, Dose


class DoseReminderManager:
    def __init__(self, email_sender: EmailSender, sms_sender: SmsSender):
        app_settings = get_app_settings()
        self.base_url = app_settings['RestApi']['BaseUrl']
        self.path = app_settings['RestApi']['DoseReminderEndpoint']
        self.email_sender = email_sender
        self.sms_sender = sms_sender

    def get_reminders_for_today(self):
        """Function to get the Doses Reminders that must be send today"""
        endpoint = f'{self.base_url}{self.path}'

        #TODO: Ver sobre autenticacion, quiza poner una key o algo, pensarlo bien
        response = requests.get(endpoint, verify=False)
        reminders = response.json()['value']['dosesReminders']

        reminders_to_return = []
        for reminder in reminders:
            parent_json = reminder['parent']
            parent = Parent(parent_json['parentId'], parent_json['firstname'], parent_json['email'])

            child_json = reminder['child']
            child = Child(child_json['childId'], child_json['name'], child_json['dni'])

            dose_json = reminder['dose']
            dose = Dose(dose_json['doseDetailId'], dose_json['vaccineName'], dose_json['doseNumber'])
            
            #via = reminder['via']
            via = "Email"
            reminders_to_return.append(DoseReminder(reminder['reminderId'], via, reminder['sendDate'], parent, child, dose))
        
        print("Dose Reminders: ", reminders_to_return)
        return reminders_to_return

    def pre_process_doses_reminders(self, doses_reminders):
        """Group the reminder by parent and child"""
        """Key is ParentId-ChildId"""
        keys_processed = []
        doses_reminders_processed = []
        max_doses_to_put_in_email = 5
        for dose_reminder in doses_reminders:
            key = f"{dose_reminder.parent.id}-{dose_reminder.child.id}"
            if key in keys_processed:
                print(f"Key {key} already was processed")
                continue
            else:
                if dose_reminder.via == "Email":
                    print(f"Key {key} is not processed, append it to the list")

                    similar_doses_reminders = list(filter(lambda x: x.parent.id == dose_reminder.parent.id and x.child.id == dose_reminder.child.id and x.id != dose_reminder.id, doses_reminders))

                    print(f"For the Key {key} was found {len(similar_doses_reminders)} similar reminders")

                    doses = []
                    doses.append({
                        "vaccine_name": dose_reminder.dose.vaccine_name,
                        "dose_number": dose_reminder.dose.dose_number 
                    })
                    
                    index_doses = 0
                    for similar_dose_reminder in similar_doses_reminders:
                        if index_doses >= max_doses_to_put_in_email:
                            break
                        doses.append({
                        "vaccine_name": similar_dose_reminder.dose.vaccine_name,
                        "dose_number": similar_dose_reminder.dose.dose_number 
                    })
                        index_doses+=1

                    doses_reminders_processed.append(DoseReminderForEmail(dose_reminder.id, dose_reminder.parent.name, dose_reminder.parent.email, dose_reminder.child.full_name, doses))
                    keys_processed.append(key)
                else:
                    print(f"Via {dose_reminder.via} not configured for Dose Reminders")
        return doses_reminders_processed

    def generate_html_email_message(self, reminder: DoseReminderForEmail):
        """Function that generate the HTML Email Message based on the information of the reminder parameter
        :param DoseReminderForEmail reminder: the reminder that contains the info to generate the HTML Email Message
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

        parent_name = reminder.parent_name
        child_name = reminder.child_name

        # vaccines_list_html = "<ul>"
        # for vaccine in campaign.vaccines:
        #     vaccines_list_html += f"<li>{vaccine.name}</li>"
        # vaccines_list_html += "</ul>"

        prox_vaccines_table_html = '''<table style="border: 1px solid black; border-collapse: collapse; padding: 5px; margin-top: 5px;">
        <tr>
            <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">Vacuna</th>
            <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">Dosis Número</th>
        </tr>'''
        for prox_vaccine in reminder.doses:
            prox_vaccines_table_html += f"""<tr>
                                                <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">{prox_vaccine['vaccine_name']}</th>
                                                <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">{prox_vaccine['dose_number']}</th>
                                            </tr>"""
        prox_vaccines_table_html += "</table>"

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
                                        <span>Hola, {parent_name}.</span>
                                        <br>
                                        <br>
                                        <span>Se aproximan vacunas para tu hijo/a {child_name}</span>
                                        <br>
                                        <br>
                                        <span>A continuación se muestran las próximas vacunas que se debe poner tu hijo/a:</span>
                                        <br>
                                        <br>
                                        {prox_vaccines_table_html}
                                        <br>
                                        <br>
                                        <br>
                                        <b>Este es un mensaje del Ministerio de Salud</b>
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
    
    def generate_sms_message(self, reminder: DoseReminder):
        sms_to_return = 'Hola, este es un SMS'
        return sms_to_return

    def send_reminders(self, reminders: list):
        sent_reminders = []
        for reminder in reminders:
            if reminder.id != 6:
                continue

            if reminder.via == "Email":
                subject = f"Recordatorio de Próximas Dosis para {reminder.child_name}"
                message = self.generate_html_email_message(reminder)
                print(f"Se enviará el recordatorio de próximas dosis {reminder.id} al padre {reminder.parent_name} con correo {reminder.parent_email}")
                with open(f'dose_email_{reminder.id}.html', 'w', encoding='utf-8') as file:
                    file.write(message)
                to = "u201810503@upc.edu.pe" #reminder.parent.email
                email_was_sent = self.email_sender.send_email(to, subject, message, "text/html")
                if email_was_sent:
                    sent_reminders.append(reminder)
                else:
                    print(f"Reminder {reminder.id} was not sent")

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

    def notify_sent_reminders(self, reminders: list):
        print(f'{len(reminders)} reminders has been sent')

def test_dose_reminder_manager():
    email_sender = EmailSender()
    sms_sender = SmsSender()
    reminder_manager = DoseReminderManager(email_sender, sms_sender)
    reminders_to_pre_process = reminder_manager.get_reminders_for_today()
    reminders_to_send = reminder_manager.pre_process_doses_reminders(reminders_to_pre_process)
    print("DR", reminders_to_send)
    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_dose_reminder_manager()