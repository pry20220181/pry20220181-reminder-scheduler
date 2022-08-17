from appsettings_manager import get_app_settings

class DoseReminder:
    def __init__(self, reminder_id):
        self.id = reminder_id

class DoseReminderManager:
    def __init__(self):
        app_settings = get_app_settings()
        self.base_url = app_settings['RestApi']['BaseUrl']
        self.path = app_settings['RestApi']['CampaignReminderEndpoint']

    def get_reminders_for_today(self):
        pass
    
    def generate_html_email_message(self, reminder: DoseReminder):
        html_email_to_return = '<h1>HTML Email Message</h1>'
        return html_email_to_return
    
    def generate_sms_message(self, reminder: DoseReminder):
        sms_to_return = 'Hola, este es un SMS'
        return sms_to_return

    def send_reminders(self, reminders: list):
        for reminder in reminders:
            print(f'Se enviara el recordatorio {reminder.id}')

def test_dose_reminder_manager():
    reminder_manager = DoseReminderManager()
    reminders_to_send = [
        DoseReminder(1),
        DoseReminder(2)
    ]
    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_dose_reminder_manager()