#region Models
class Parent:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class Child:
    def __init__(self, id, full_name, dni):
        self.id = id
        self.full_name = full_name
        self.dni = dni

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

class Dose:
    def __init__(self, dose_id, vaccine_name, dose_number):
        self.dose_id = dose_id
        self.vaccine_name = vaccine_name
        self.dose_number = dose_number

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
    def __init__(self, id, appointment_datetime, child: Child, health_center: HealhCenter, vaccines: list):
        self.id = id
        self.appointment_datetime = appointment_datetime
        self.child = child
        self.health_center = health_center
        self.vaccines = vaccines

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
    def __init__(self, reminder_id, via, send_date, parent: Parent, vaccination_appointment: VaccinationAppointment):
        self.id = reminder_id
        self.via = via
        self.send_date = send_date
        self.parent = parent
        self.vaccination_appointment = vaccination_appointment

class DoseReminder:
    def __init__(self, reminder_id, via, send_date, parent: Parent, child: Child, dose: Dose):
        self.id = reminder_id
        self.via = via
        self.send_date = send_date
        self.parent = parent
        self.child = child
        self.dose = dose
#endregion