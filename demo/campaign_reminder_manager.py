class CampaignReminder:
    def __init__(self, reminder_id):
        self.id = reminder_id

class CampaignReminderManager:
    def __init__(self):
        pass

    def get_reminders_for_today(self):
        pass

    def send_reminders(self, reminders: list):
        for reminder in reminders:
            print(f'Se enviara el recordatorio de campaña {reminder.id}')

def test_campaign_reminder_manager():
    reminder_manager = CampaignReminderManager()
    reminders_to_send = [
        CampaignReminder(1),
        CampaignReminder(2)
    ]
    reminder_manager.send_reminders(reminders_to_send)

if __name__ == '__main__':
    test_campaign_reminder_manager()