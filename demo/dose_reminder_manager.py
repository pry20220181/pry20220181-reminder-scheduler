class DoseReminder:
    def __init__(self, reminder_id):
        self.id = reminder_id

class DoseReminderManager:
    def __init__(self):
        pass

    def get_reminders_for_today(self):
        pass

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