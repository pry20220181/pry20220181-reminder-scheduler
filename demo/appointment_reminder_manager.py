class AppointmentReminder:
    def __init__(self, reminder_id):
        self.id = reminder_id

class AppointmentReminderManager:
    def __init__(self):
        pass

    def get_reminders_for_today(self):
        pass

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