import requests
from appsettings_manager import get_app_settings
from sms_sender import SmsSender #https://realpython.com/python-requests/
from email_sender import EmailSender
from models import DoseReminder, Parent, Child, Dose


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
        for dose_reminder in doses_reminders:
            key = f"{dose_reminder.parent.id}-{dose_reminder.child.id}"
            if key in keys_processed:
                print(f"Key {key} already was processed")
                continue
            else:
                print(f"Key {key} is not processed, append it to the list")

                similar_doses_reminders = list(filter(lambda x: x.parent.id == dose_reminder.parent.id and x.child.id == dose_reminder.child.id and x.id != dose_reminder.id, doses_reminders))

                print(f"For the Key {key} was found {len(similar_doses_reminders)} similar reminders")

                keys_processed.append(key)

    def generate_html_email_message(self, reminder: DoseReminder):
        html_email_to_return = '<h1>HTML Email Message</h1>'
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
                subject = f"Recordatorio de Próximas Dosis para {reminder.child.full_name}"
                message = self.generate_html_email_message(reminder)
                print(f"Se enviará el recordatorio de próximas dosis {reminder.id} al padre {reminder.parent.name} con correo {reminder.parent.email}")
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

        self.notify_sent_reminders(reminders)
        return reminders

    def notify_sent_reminders(self, reminders: list):
        print(f'{len(reminders)} reminders has been sent')

def test_dose_reminder_manager():
    email_sender = EmailSender()
    sms_sender = SmsSender()
    reminder_manager = DoseReminderManager(email_sender, sms_sender)
    reminders_to_pre_process = reminder_manager.get_reminders_for_today()
    #ACA SE PROCESARAN LOS RECORDATORIOS PARA AGRUPARLOS
    reminders_to_send = reminder_manager.pre_process_doses_reminders(reminders_to_pre_process)

    #reminder_manager.send_reminders(reminders_to_pre_process)

if __name__ == '__main__':
    test_dose_reminder_manager()