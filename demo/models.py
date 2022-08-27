#region Models
class Parent:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class HealhCenter:
    def __init__(self, id, name, address):
        """
        :param int id: the ID of the Health Center
        """
        self.id = id
        self.name = name
        self.address = address

class Vaccine:
    def __init__(self, name):
        self.name = name

class VaccinationCampaign:
    def __init__(self, id, name, description, start_date, end_date, health_centers: list, vaccines: list):
        """
        :param list:HealhCenter health_centers: the health centers where the campaign will be
        """
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.health_centers = health_centers
        self.vaccines = vaccines

class VaccinationAppointment:
    def __init__(self):
        pass

class CampaignReminder:
    def __init__(self, reminder_id, via, send_date, parent: Parent, vaccination_campaign: VaccinationCampaign):
        """
        :param string via: SMS or Email
        :param string send_date: when must be send the reminder
        """
        self.id = reminder_id
        self.via = via
        self.send_date = send_date
        self.parent = parent
        self.vaccination_campaign = vaccination_campaign

class AppointmentReminder:
    def __init__(self, reminder_id):
        self.id = reminder_id
#endregion