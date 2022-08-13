from appsettings_manager import get_app_settings
import requests #https://realpython.com/python-requests/

class CampaignReminder:
    def __init__(self, reminder_id):
        self.id = reminder_id

class CampaignReminderManager:
    def __init__(self):
        pass

    def get_reminders_for_today(self):
        app_settings = get_app_settings()
        base_url = app_settings['RestApi']['BaseUrl']
        path = app_settings['RestApi']['CampaignReminderEndpoint']
        endpoint = f'{base_url}{path}'

        #TODO: Ver sobre autenticacion, quiza poner una key o algo, pensarlo bien
        print(f'Se obtendra la info del endpoint {endpoint}')
        response = requests.get(endpoint, verify=False)

        print(response.json())

    def send_reminders(self, reminders: list):
        for reminder in reminders:
            print(f'Se enviara el recordatorio de campaña {reminder.id}')

def test_campaign_reminder_manager():
    reminder_manager = CampaignReminderManager()
    reminder_manager.get_reminders_for_today()
    # reminders_to_send = [
    #     CampaignReminder(1),
    #     CampaignReminder(2)
    # ]
    # reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_campaign_reminder_manager()