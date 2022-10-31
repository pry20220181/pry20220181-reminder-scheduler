from email_sender import EmailSender
from sms_sender import SmsSender
from appointment_reminder_manager import AppointmentReminderManager
from dose_reminder_manager import DoseReminderManager
from campaign_reminder_manager import CampaignReminderManager

def lambda_handler(event, context):
    appointment_reminder_manager()
    dose_reminder_manager()
    campaign_reminder_manager()

def appointment_reminder_manager():
    email_sender = EmailSender()
    sms_sender = SmsSender()
    reminder_manager = AppointmentReminderManager(email_sender, sms_sender)
    reminders_to_send = reminder_manager.get_reminders_for_today()

    reminder_manager.send_reminders(reminders_to_send)

def dose_reminder_manager():
    email_sender = EmailSender()
    sms_sender = SmsSender()
    reminder_manager = DoseReminderManager(email_sender, sms_sender)
    reminders_to_pre_process = reminder_manager.get_reminders_for_today()
    reminders_to_send = reminder_manager.pre_process_doses_reminders(reminders_to_pre_process)
    print("DR", reminders_to_send)
    reminder_manager.send_reminders(reminders_to_send)

def campaign_reminder_manager():
    email_sender = EmailSender()
    sms_sender = SmsSender()
    reminder_manager = CampaignReminderManager(email_sender, sms_sender)
    reminders_to_send = reminder_manager.get_reminders_for_today()

    reminder_manager.send_reminders(reminders_to_send)