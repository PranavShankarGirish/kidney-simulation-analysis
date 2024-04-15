
class Donor:
    def __init__(self, id, Pid, blood_patient, hospital_type, hospital_name_allocated, hospital_type_allocated, age_alloc, bloodgroup, age, city_recieved, city_allocated, transportation_time, transplantation_time, total_time,state):
        self.id = id
        self.Pid = Pid
        self.blood_patient = blood_patient
        self.hospital_type = hospital_type
        self.hospital_name_allocated = hospital_name_allocated
        self.hospital_type_allocated  = hospital_type_allocated
        self.age_alloc = age_alloc
        self.bloodgroup = bloodgroup
        self.age = age
        self.city_recieved = city_recieved
        self.city_allocated = city_allocated
        self.transportation_time = transportation_time
        self.transplantation_time = transplantation_time
        self.total_time = total_time
        self.state=state
    def printDonor(self):
        print("id = ", self.id, "Pid = ",self.Pid, "blood_patient = ", self.blood_patient, "hospital_type = ", self.hospital_type, "hospital_name_allocated = ", self.hospital_name_allocated, "hospital_type_allocated = ", self.hospital_type_allocated, "age_alloc = ", self.age_alloc, "bloodgroup = ", self.bloodgroup, "age = ", self.age, "city_recieved = ", self.city_recieved, "city_allocated = ", self.city_allocated, "transportation_time = ", self.transportation_time, "transplantation_time =  ", self.transplantation_time, "total_time", self.total_time,"state=",self.sate)

