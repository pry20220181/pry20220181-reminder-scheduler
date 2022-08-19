from appsettings_manager import get_app_settings
import requests #https://realpython.com/python-requests/

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

    def __init__(self):
        app_settings = get_app_settings()
        self.base_url = app_settings['RestApi']['BaseUrl']
        self.path = app_settings['RestApi']['CampaignReminderEndpoint']


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
        html_email_to_return = '<h1>HTML Email Message</h1>'
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
        for reminder in reminders:
            print(f"Se enviara el recordatorio de campaña {reminder.id} al padre {reminder.parent.name} con correo {reminder.parent.email}")

def test_campaign_reminder_manager():
    reminder_manager = CampaignReminderManager()
    reminders_to_send = reminder_manager.get_reminders_for_today()

    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_campaign_reminder_manager()