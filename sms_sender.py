class SmsSender:
    def __init__(self):
        pass

    def send_sms(self, to, message):
        print(f"Send the message '{message}' to {to}")
        return False

if __name__ == '__main__':
    print('This is the SmsSender module for PRY20220181 Reminder Scheduler Lambda')