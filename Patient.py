import global_vars
class Patient:
    def __init__(self, id, age, city,cityindex,recievingcityindex, bloodgroup, removal_time, kap_score, hospital_name, hospital_type, pra, avg, av_fitsula, time_on_dailysis, pigf, last_time,state):
        self.id = id
        self.age = age
        self.city = city
        self.bloodgroup = bloodgroup
        self.removal_time = float(removal_time)
        self.kap_score = kap_score
        self.hospital_name = hospital_name
        self.hospital_type = hospital_type
        self.pra = pra
        self.avg = avg
        self.av_fitsula = av_fitsula
        self.time_on_dailysis = time_on_dailysis
        self.pigf = pigf
        self.cityindex=cityindex
        self.last_time = last_time
        self.state=state
        self.recievingcityindex=recievingcityindex

    def printPatient(self):
        print("id = ", self.id, "age = ", self.age, "city = ", self.city, "bloodgroup = ",self.bloodgroup,"cityindex=",self.cityindex ,self.bloodgroup, "removal_time = ", self.removal_time, "kap_score = ", self.kap_score, "hospital_name = ", self.hospital_name, "hospital_type = ", self.hospital_type, "pra = ", self.pra, "avg = ", self.avg, "av_fitsula = ", self.av_fitsula, "time_on_dailysis = ", self.time_on_dailysis, "pigf = ", self.pigf, "last_time =", self.last_time,"state =",self.state)
