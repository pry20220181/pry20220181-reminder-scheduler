from appsettings_manager import get_app_settings
import requests #https://realpython.com/python-requests/

#region Models
class CampaignReminder:
    def __init__(self, reminder_id, via, send_date, health_centers: list):
        """
        :param string via: SMS or Email
        :param string send_date: when must be send the reminder
        :param list:HealhCenter health_centers: the health centers where the campaign will be
        """
        self.id = reminder_id
        self.via = via
        self.send_date = send_date
        self.health_centers = health_centers

class HealhCenter:
    def __init__(self, id, name, address):
        """
        :param int id: the ID of the Health Center
        """
        self.id = id
        self.name = name
        self.address = address
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
            #region Map Health Centers
            vaccination_campaign = reminder['vaccinationCampaign']
            health_centers = []
            for health_center in vaccination_campaign['healthCenters']:
                health_centers.append(HealhCenter(health_center['healthCenterId'], health_center['name'], health_center['address']))
            #endregion
            
            reminders_to_return.append(CampaignReminder(reminder['reminderId'], reminder['via'], reminder['sendDate'], health_centers))
        
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
            print(f'Se enviara el recordatorio de campaña {reminder.id}')

def test_campaign_reminder_manager():
    reminder_manager = CampaignReminderManager()
    reminders_to_send = reminder_manager.get_reminders_for_today()

    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_campaign_reminder_manager()