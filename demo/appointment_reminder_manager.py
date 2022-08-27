from appsettings_manager import get_app_settings
import requests
from sms_sender import SmsSender #https://realpython.com/python-requests/
from email_sender import EmailSender
from models import AppointmentReminder, HealhCenter, Parent, VaccinationCampaign, Vaccine

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
            vaccination_appoinment_id = reminder['vaccinationAppointmentId']
            appoinment_datetime = reminder['appointmentDateTime']

            vaccination_appointment_json = reminder['VaccinationAppointment']
            parent_json = reminder['parent']
            parent = Parent(parent_json['parentId'], parent_json['firstname'], parent_json['email'])

            #region Map Health Centers
            health_centers = []
            for health_center in vaccination_appointment_json['healthCenters']:
                health_centers.append(HealhCenter(health_center['healthCenterId'], health_center['name'], health_center['address']))
            #endregion

            #region Map Vaccines
            vaccines = []
            for vaccine in vaccination_appointment_json['vaccines']:
                vaccines.append(Vaccine(vaccine))
            #endregion
            
            vaccination_campaign = VaccinationCampaign(vaccination_campaign_json['vaccinationCampaignId'], vaccination_campaign_json['name'], vaccination_campaign_json['description'], vaccination_campaign_json['startDateTime'], vaccination_campaign_json['endDateTime'], health_centers, vaccines)

            reminders_to_return.append(CampaignReminder(reminder['reminderId'], reminder['via'], reminder['sendDate'], parent, vaccination_campaign))
        
        print("Reminders: ", reminders_to_return)
        return reminders_to_return

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