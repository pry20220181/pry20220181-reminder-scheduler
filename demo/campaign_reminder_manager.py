from appsettings_manager import get_app_settings
import requests #https://realpython.com/python-requests/
from email_sender import EmailSender

#region Models
class Parent:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class HealhCenter:
    def __init__(self, id, name, address):
        """
        :param int id: the ID of the Health Center
        """
        self.id = id
        self.name = name
        self.address = address

class Vaccine:
    def __init__(self, name):
        self.name = name

class VaccinationCampaign:
    def __init__(self, id, name, description, start_date, end_date, health_centers: list, vaccines: list):
        """
        :param list:HealhCenter health_centers: the health centers where the campaign will be
        """
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.health_centers = health_centers
        self.vaccines = vaccines

class CampaignReminder:
    def __init__(self, reminder_id, via, send_date, parent: Parent, vaccination_campaign: VaccinationCampaign):
        """
        :param string via: SMS or Email
        :param string send_date: when must be send the reminder
        """
        self.id = reminder_id
        self.via = via
        self.send_date = send_date
        self.parent = parent
        self.vaccination_campaign = vaccination_campaign


#endregion

class CampaignReminderManager:
    """Class to the process of sending Campaign Reminders"""

    def __init__(self, email_sender: EmailSender):
        app_settings = get_app_settings()
        self.base_url = app_settings['RestApi']['BaseUrl']
        self.path = app_settings['RestApi']['CampaignReminderEndpoint']
        self.email_sender = email_sender


    def get_reminders_for_today(self):
        """Function to get the Campaign Reminders that must be send today"""
        endpoint = f'{self.base_url}{self.path}'

        #TODO: Ver sobre autenticacion, quiza poner una key o algo, pensarlo bien
        response = requests.get(endpoint, verify=False)
        reminders = response.json()['value']['vaccinationCampaignReminders']
       

        reminders_to_return = []
        for reminder in reminders:
            vaccination_campaign_json = reminder['vaccinationCampaign']
            parent_json = reminder['parent']
            parent = Parent(parent_json['parentId'], parent_json['firstname'], parent_json['email'])

            #region Map Health Centers
            health_centers = []
            for health_center in vaccination_campaign_json['healthCenters']:
                health_centers.append(HealhCenter(health_center['healthCenterId'], health_center['name'], health_center['address']))
            #endregion

            #region Map Vaccines
            vaccines = []
            for vaccine in vaccination_campaign_json['vaccines']:
                vaccines.append(Vaccine(vaccine))
            #endregion
            
            vaccination_campaign = VaccinationCampaign(vaccination_campaign_json['vaccinationCampaignId'], vaccination_campaign_json['name'], vaccination_campaign_json['description'], vaccination_campaign_json['startDateTime'], vaccination_campaign_json['endDateTime'], health_centers, vaccines)

            reminders_to_return.append(CampaignReminder(reminder['reminderId'], reminder['via'], reminder['sendDate'], parent, vaccination_campaign))
        
        print(reminders_to_return)
        return reminders_to_return

    def generate_html_email_message(self, reminder: CampaignReminder):
        """Function that generate the HTML Email Message based on the information of the reminder parameter
        :param CampaignReminder reminder: the reminder that contains the info to generate the HTML Email Message
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
        campaign = reminder.vaccination_campaign
        start_date = campaign.start_date[0:10]
        start_time = campaign.start_date[11:16]
        end_date = campaign.end_date[0:10]
        end_time = campaign.end_date[11:16]

        vaccines_list_html = "<ul>"
        for vaccine in campaign.vaccines:
            vaccines_list_html += f"<li>{vaccine.name}</li>"
        vaccines_list_html += "</ul>"

        health_centers_table_html = '''<table style="border: 1px solid black; border-collapse: collapse; padding: 5px; margin-top: 5px;">
        <tr>
            <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">Nombre</th>
            <th style="border: 1px solid black; border-collapse: collapse; padding: 5px;">Dirección</th>
        </tr>'''
        for health_center in campaign.health_centers:
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
                                        <span>Se aproxima la campaña <b>"{campaign.name}"</b>. Inicia el {start_date} a las {start_time}
                                            hasta el {end_date} a las {end_time}</span>
                                        <br>
                                        <br>
                                        <span>En esta campaña de vacunación se pondrán las siguientes vacunas:</span>
                                        <br>
                                        {vaccines_list_html}
                                        <br>
                                        <span>Los centros de salud donde se dará esta campaña de vacunación son los
                                            siguientes:</span>
                                        {health_centers_table_html}
                                        <br>
                                        <br>
                                        <br>
                                        <b>Este es un mensaje del MINSA</b>
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
    
    def generate_sms_message(self, reminder: CampaignReminder):
        """Function that generate the text for the SMS based on the information of the reminder parameter
        :param CampaignReminder reminder: the reminder that contains the info to generate the SMS Message
        """
        sms_to_return = 'Hola, este es un SMS'
        return sms_to_return

    def send_reminders(self, reminders: list):
        """Function that receives a list of reminders and send them one by one
        :param list reminders: the reminders that must be send
        """
        sent_reminders = []
        for reminder in reminders:
            if reminder.id != 1:
                break

            if reminder.via == "Email":
                subject = f"Campaña Vacunación - {reminder.vaccination_campaign.name}"
                message = self.generate_html_email_message(reminder)
                print(f"Se enviara el recordatorio de campaña {reminder.id} al padre {reminder.parent.name} con correo {reminder.parent.email}")
                with open(f'email_{reminder.id}.html', 'w', encoding='utf-8') as file:
                    file.write(message)
                to = "u201810503@upc.edu.pe" #reminder.parent.email
                email_was_sent = self.email_sender.send_email(to, subject, message, "text/html")
                if email_was_sent:
                    sent_reminders.append(reminder)
            elif reminder.via == "SMS":
                message = self.generate_sms_message(reminder)
            else:
                print(f"Invalid via for reminder {reminder.id}")
                continue
            

def test_campaign_reminder_manager():
    email_sender = EmailSender()
    reminder_manager = CampaignReminderManager(email_sender)
    reminders_to_send = reminder_manager.get_reminders_for_today()

    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_campaign_reminder_manager()