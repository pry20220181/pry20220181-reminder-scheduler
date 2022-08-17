from appsettings_manager import get_app_settings

class AppointmentReminder:
    def __init__(self, reminder_id):
        self.id = reminder_id

class AppointmentReminderManager:
    def __init__(self):
        app_settings = get_app_settings()
        self.base_url = app_settings['RestApi']['BaseUrl']
        self.path = app_settings['RestApi']['CampaignReminderEndpoint']

    def get_reminders_for_today(self):
        pass

    def generate_html_email_message(self, reminder: AppointmentReminder):
        html_email_to_return = '<h1>HTML Email Message</h1>'
        return html_email_to_return
    
    def generate_sms_message(self, reminder: AppointmentReminder):
        sms_to_return = 'Hola, este es un SMS'
        return sms_to_return

    def send_reminders(self, reminders: list):
        for reminder in reminders:
            print(f'Se enviara el recordatorio de cita {reminder.id}')

def test_appointment_reminder_manager():
    reminder_manager = AppointmentReminderManager()
    reminders_to_send = [
        AppointmentReminder(1),
        AppointmentReminder(2)
    ]
    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_appointment_reminder_manager()