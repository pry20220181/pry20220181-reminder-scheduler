from appsettings_manager import get_app_settings
import requests #https://realpython.com/python-requests/

class CampaignReminder:
    def __init__(self, reminder_id):
        self.id = reminder_id

class CampaignReminderManager:
    def __init__(self):
        app_settings = get_app_settings()
        self.base_url = app_settings['RestApi']['BaseUrl']
        self.path = app_settings['RestApi']['CampaignReminderEndpoint']

    def get_reminders_for_today(self):
        endpoint = f'{self.base_url}{self.path}'

        #TODO: Ver sobre autenticacion, quiza poner una key o algo, pensarlo bien
        response = requests.get(endpoint, verify=False)
        reminders = response.json()['value']['vaccinationCampaignReminders']
        print(reminders)
        reminders_to_return = []
        for reminder in reminders:
            reminders_to_return.append(CampaignReminder(reminder['reminderId']))
        
        return reminders_to_return

    def generate_html_email_message(self, reminder: CampaignReminder):
        html_email_to_return = '<h1>HTML Email Message</h1>'
        return html_email_to_return
    
    def generate_sms_message(self, reminder: CampaignReminder):
        sms_to_return = 'Hola, este es un SMS'
        return sms_to_return

    def send_reminders(self, reminders: list):
        for reminder in reminders:
            print(f'Se enviara el recordatorio de campaña {reminder.id}')

def test_campaign_reminder_manager():
    reminder_manager = CampaignReminderManager()
    reminders_to_send = reminder_manager.get_reminders_for_today()

    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_campaign_reminder_manager()