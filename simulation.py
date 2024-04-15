import xlrd
import math
import AddPatient
import random
import RemovePatient
import AddDonor
import global_vars
import numpy as np

# Hospital class
class Hospital:
    def __init__(self, name, city, prob_retrival, prob_waitlist, type,state):
        self.name = name
        self.city = city
        self.prob_retrival = prob_retrival
        self.prob_waitlist = prob_waitlist
        self.type = type
        self.state=state

    def printHospital(self):
        print("name = ", self.name, "city = ", self.city, "prob_retrival = ", self.prob_retrival, "prob_waitlist = ", self.prob_waitlist, "type = ", self.type,"state=",self.state)

# new event class
class NEvent:
    def __init__(self, name, time):
        self.name = name
        self.time = time

# return value of the simulation function as a class
class return_value:
    def __init__(self, awt, size, deaths, total_organs_donated, total_patients_registered, p_15, o_15, d_15):
        self.awt = awt
        self.size = size
        self.deaths = deaths
        self.total_organs_donated = total_organs_donated
        self.total_patients_registered = total_patients_registered
        self.p_15 = p_15
        self.o_15 = o_15
        self.d_15 = d_15

# clock timer function
def ClockTimer():
    import global_vars
    inf = 100000000
    #print("next patient", global_vars.NEXT_PATIENT_ARRIVAL)
    events = [NEvent("PatientArrival",global_vars.NEXT_PATIENT_ARRIVAL),NEvent("OrganArrival",global_vars.NEXT_ORGAN_ARRIVAL),NEvent("RemovalTime",global_vars.NEXT_PATIENT_REMOVAL)]
    events.sort(key=lambda x: x.time)
    Event = events[0].name
    if Event == "PatientArrival":
        NextEvent = 'AddPatient'
        global_vars.CLOCK_SIM = global_vars.NEXT_PATIENT_ARRIVAL
        global_vars.NEXT_PATIENT_ARRIVAL = inf
    elif Event == "OrganArrival":
        NextEvent = 'AddDonor'
        global_vars.CLOCK_SIM = global_vars.NEXT_ORGAN_ARRIVAL
        global_vars.NEXT_ORGAN_ARRIVAL = inf
    elif Event == "RemovalTime":
        NextEvent = "RemovePatient"
        global_vars.CLOCK_SIM = global_vars.NEXT_PATIENT_REMOVAL
        global_vars.NEXT_PATIENT_REMOVAL = inf

    for P in global_vars.WAITLIST:
        months_passed=math.floor((global_vars.CLOCK_SIM-P.id)/(24*30))
        if months_passed-P.last_time>0:
            P.kap_score+=months_passed-P.last_time
        P.last_time=months_passed

    for i in range(len(global_vars.CITYLIST)):
        for P in global_vars.CITY_WAITLIST[i]:
            months_passed=math.floor((global_vars.CLOCK_SIM-P.id)/(24*30))
            if months_passed-P.last_time>0:
                P.kap_score+=months_passed-P.last_time
            P.last_time=months_passed
            
    return NextEvent
# the simulation function
def simulation(years,city_list, DurationMatrix,steady,rep):
    import global_vars

    global_vars.CLOCK_SIM = 0
    global_vars.NEXT_PATIENT_ARRIVAL = 100000000
    global_vars.NEXT_ORGAN_ARRIVAL = 100000000
    global_vars.NEXT_PATIENT_REMOVAL = 100000000
    global_vars.CITYLIST = city_list
    global_vars.DURATION = DurationMatrix
    global_vars.CITY_WAITLIST = []
    global_vars.ALLOCATED_LIST = []
    global_vars.ALLOCATED_LIST_P = []
    global_vars.NEXT_PATIENT_ARRIVAL = steady[0]
    global_vars.NEXT_ORGAN_ARRIVAL = steady[1]
    global_vars.HOSPITAL_LIST = []
    global_vars.WL=np.zeros((200000,25))
    global_vars.WLhosp=np.empty((200000,1),dtype='S64')
    global_vars.DL=np.zeros((200000,4))
    global_vars.DL5=np.zeros((200000,1))
    global_vars.DL2=np.zeros((200000,1))
    global_vars.DL1=np.zeros((200000,1))
    global_vars.RL=np.zeros((200000,1))
    global_vars.i=0
    global_vars.x=0
    global_vars.y=0
    global_vars.z=0
    global_vars.A=0
    global_vars.B=0
    global_vars.O=0
    global_vars.AB=0
    global_vars.m=0
    global_vars.hosp_index=0

    index=len(global_vars.CITYLIST)
    for i in range(index):
        waitlist = []
        global_vars.CITY_WAITLIST.append(waitlist)

    hospitalSheet = xlrd.open_workbook("hospital_list.xls")
    hospitalList = hospitalSheet.sheet_by_index(0)

    index = len(global_vars.CITYLIST)

    for i in range(index):
        waitlist1 = []
        global_vars.HOSPITAL_LIST.append(waitlist1)
    for i in range(29):
        hosp_index = 0
        for j in range(index):
            if hospitalList.cell_value(i+1, 1) == global_vars.CITYLIST[j]:
                hosp_index = j
                break

        type=""
        name = hospitalList.cell_value(i+1, 0)
        city = hospitalList.cell_value(i+1, 1)
        prob_retrival = hospitalList.cell_value(i+1, 2)
        prob_waitlist = hospitalList.cell_value(i+1, 3)

        if random.uniform(0, 1) < 0.5:
            type = 'P'
        else:
            type = 'G'
        # # type =  'G' #hospitalList.cell_value(i+1, 4)
        hosp = Hospital(name,city ,prob_retrival, prob_waitlist, type,"Kerala")
        global_vars.HOSPITAL_LIST[hosp_index].append(hosp)

    # for i in range(32):
    #     for j in range(len(global_vars.HOSPITAL_LIST[i])):
    #         global_vars.HOSPITAL_LIST[i][j].printHospital()
    print(global_vars.CITY_WAITLIST[3])
    global_vars.WAITLIST = []
    global_vars.PATIENT_LIST=[]
    global_vars.ORGAN_WASTE = 0
    print(global_vars.WAITLIST)
    global_vars.REMOVED_LIST = []
    global_vars.dailysis_months = 0
    global_vars.BG_A = np.zeros((rep,0))
    global_vars.BG_B = np.zeros((rep,0))
    global_vars.BG_O = np.zeros((rep,0))
    global_vars.BG_AB = np.zeros((rep,0))
    global_vars.BGP_A = np.zeros((rep,0))
    global_vars.BGP_B = np.zeros((rep,0))
    global_vars.BGP_AB = np.zeros((rep,0))
    global_vars.BGP_O = np.zeros((rep,0))
    LAST_TIME = 0
    total_patients_registered = 0
    total_organs_donated = 0
    death = 0
    year = years
    time = year*365*24
    awt = [0]*year
    size = [0]*year
    flag = [0]*year
    p_15 = [0]*year
    o_15 = [0]*year
    d_15 = [0]*year
    global_vars.LAST_TIME = 0
 # just so that we don't run out of patients if randomly organ donors come before patients
    # simulation loop
    index=len(global_vars.CITYLIST)

    while global_vars.CLOCK_SIM < time:
        d=global_vars.CLOCK_SIM
        NextEvent = ClockTimer()
        if global_vars.CLOCK_SIM<d:
            print(NextEvent)
            raise ValueError
        if NextEvent == 'AddPatient':
            print("patient added")
            AddPatient.AddPatient()
            total_patients_registered += 1
        elif NextEvent == 'AddDonor':
            print("donor added")
            AddDonor.AddDonor()
            total_organs_donated += 1
        elif NextEvent == 'RemovePatient':
            if len(global_vars.WAITLIST)!=0:
                print("patient removed")
                RemovePatient.RemovePatient()
                death += 1
            else:
                continue
        #
        # if global_vars.CLOCK_SIM in range(0,(1*365*24)):
        #     global_vars.m=0
        # elif global_vars.CLOCK_SIM in range((1*365*24),(2*365*24)):
        #     global_vars.m=1
        # elif global_vars.CLOCK_SIM in range((2*365*24),(3*365*24)):
        #     global_vars.m=2
        # elif global_vars.CLOCK_SIM in range((3*365*24),(4*365*24)):
        #     global_vars.m=3
        # elif global_vars.CLOCK_SIM in range((4*365*24),(5*365*24)):
        #     global_vars.m=4
        # elif global_vars.CLOCK_SIM in range((5*365*24),(6*365*24)):
        #     global_vars.m=5
        # elif global_vars.CLOCK_SIM in range((6*365*24),(7*365*24)):
        #     global_vars.m=6
        # elif global_vars.CLOCK_SIM in range((7*365*24),(8*365*24)):
        #     global_vars.m=7
        # elif global_vars.CLOCK_SIM in range((8*365*24),(9*365*24)):
        #     global_vars.m=8
        # elif global_vars.CLOCK_SIM in range((9*365*24),(10*365*24)):
        #     global_vars.m=9
        # elif global_vars.CLOCK_SIM in range((10*365*24),(11*365*24)):
        #     global_vars.m=10
        # elif global_vars.CLOCK_SIM in range((11*365*24),(12*365*24)):
        #     global_vars.m=11
        # elif global_vars.CLOCK_SIM in range((12*365*24),(13*365*24)):
        #     global_vars.m=12
        # elif global_vars.CLOCK_SIM in range((13*365*24),(14*365*24)):
        #     global_vars.m=13
        # elif global_vars.CLOCK_SIM in range((14*365*24),(15*365*24)):
        #     global_vars.m=14
        # elif global_vars.CLOCK_SIM in range((15*365*24),(16*365*24)):
        #     global_vars.m=15
        # elif global_vars.CLOCK_SIM in range((16*365*24),(17*365*24)):
        #     global_vars.m=16
        # elif global_vars.CLOCK_SIM in range((17*365*24),(18*365*24)):
        #     global_vars.m=17
        # elif global_vars.CLOCK_SIM in range((18*365*24),(19*365*24)):
        #     global_vars.m=18
        # elif global_vars.CLOCK_SIM in range((19*365*24),(20*365*24)):
        #     global_vars.m=19
        # elif global_vars.CLOCK_SIM in range((20*365*24),(21*365*24)):
        #     global_vars.m=20
        # elif global_vars.CLOCK_SIM in range((21*365*24),(22*365*24)):
        #     global_vars.m=21
        # elif global_vars.CLOCK_SIM in range((22*365*24),(23*365*24)):
        #     global_vars.m=22
        # elif global_vars.CLOCK_SIM in range((23*365*24),(24*365*24)):
        #     global_vars.m=23
        # elif global_vars.CLOCK_SIM in range((24*365*24),(25*365*24)):
        #     global_vars.m=24

        print("LIST LENGTH", len(global_vars.WAITLIST))

#     for i in range(year):
#         if global_vars.CLOCK_SIM>i*365*24 and flag[i] == 0 and len(global_vars.ALLOCATED_LIST) > 0:
#             awt[i] = sum(c.total_time for c in global_vars.ALLOCATED_LIST)/len(global_vars.ALLOCATED_LIST)
#             size[i] = len(global_vars.ALLOCATED_LIST)
#             flag[i] = 1
#             p_15[i] = total_patients_registered
#             o_15[i] = total_organs_donated
#             d_15[i] = death
# return return_value(awt, size, death, total_organs_donated, total_patients_registered, p_15, o_15, d_15)
#
# return_value.avg_transport_time=sum([global_vars.ALLOCATED_LIST.transportation_time])/size(global_vars.ALLOCATED_LIST,2);
# return_value.avg_waiting_time=sum([global_vars.ALLOCATED_LIST.waiting_time])/size(global_vars.ALLOCATED_LIST,2);
# bg_list=[global_vars.ALLOCATED_LIST.blood_patient];
# blood_a=strfind(bg_list,'A');
# blood_b=strfind(bg_list,'B');
# blood_ab=strfind(bg_list,'C');
# blood_o=strfind(bg_list,'O');
# return_value.bg=[size(blood_a,2),size(blood_b,2),size(blood_ab,2),size(blood_o,2)];
# if(return_value.bg(1)==0):
#     return_value.avg_bg_a=365*initilization;
# else:
#     return_value.avg_bg_a=sum([global_vars.ALLOCATED_LIST(blood_a).waiting_time])/size(bg_list(blood_a),2);
# # end
# if(return_value.bg(2)==0):
#     return_value.avg_bg_b=365*initilization;
# else:
#     return_value.avg_bg_b=sum([global_vars.ALLOCATED_LIST(blood_b).waiting_time])/size(bg_list(blood_b),2);
# # end
# if(return_value.bg(3)==0):
#     return_value.avg_bg_ab=365*initilization;
# else:
#     return_value.avg_bg_ab=sum([global_vars.ALLOCATED_LIST(blood_ab).waiting_time])/size(bg_list(blood_ab),2);
# # end
# if(return_value.bg(4)==0):
#     return_value.avg_bg_o=365*initilization;
# else:
#     return_value.avg_bg_o=sum([global_vars.ALLOCATED_LIST(blood_o).waiting_time])/size(bg_list(blood_o),2);
# # end
# #
# x=find([global_vars.ALLOCATED_LIST.hospital_type_allocated]=='G');
# y=find([global_vars.ALLOCATED_LIST.hospital_type_allocated]=='P');
# w=sum([global_vars.ALLOCATED_LIST(x).waiting_time])/size(x,2);
# v=sum([global_vars.ALLOCATED_LIST(y).waiting_time])/size(y,2);
# return_value.hospital=[w/24,v/24];
# return_value.alloc_hosp_num=[size(x,2),size(y,2)];
# #
# #
# #
# return_value.organs=size(global_vars.ALLOCATED_LIST,2);
# return_value.patients=total_patients_registered;
# return_value.deaths=death;
# return_value.waste=global_vars.ORGAN_WASTE;
# #
# wait_hosp_g=find([global_vars.WAITLIST.hospital_type]=='G');
# wait_hosp_p=find([global_vars.WAITLIST.hospital_type]=='P');
# return_value.wait_hosp_num=[size(wait_hosp_g,2), size(wait_hosp_p,2)];
#
# wait_bg_a=find([global_vars.WAITLIST.bloodgroup]=='A');
# wait_bg_b=find([global_vars.WAITLIST.bloodgroup]=='B');
# wait_bg_ab=find([global_vars.WAITLIST.bloodgroup]=='C');
# wait_bg_o=find([global_vars.WAITLIST.bloodgroup]=='O');
# return_value.wait_bg_num=[size(wait_bg_a,2) size(wait_bg_b,2) size(wait_bg_ab,2) size(wait_bg_o,2)];
#
# total_hosp_g=find([global_vars.PATIENT_LIST.hospital_type]=='G');
# total_hosp_p=find([global_vars.PATIENT_LIST.hospital_type]=='P');
# return_value.total_hosp_num=[size(total_hosp_g,2) size(total_hosp_p,2)];
#
# total_bg_a=find([global_vars.PATIENT_LIST.bloodgroup]=='A');
# total_bg_b=find([global_vars.PATIENT_LIST.bloodgroup]=='B');
# total_bg_ab=find([global_vars.PATIENT_LIST.bloodgroup]=='C');
# total_bg_o=find([global_vars.PATIENT_LIST.bloodgroup]=='O');
# return_value.total_bg_num=[size(total_bg_a,2) size(total_bg_b,2) size(total_bg_ab,2) size(total_bg_o,2)];
# #
# #
# alloc_age=find([global_vars.ALLOCATED_LIST.age_alloc]<18);
# return_value.age_alloc=size(alloc_age,2);
# total_age=find([global_vars.PATIENT_LIST.age]<18);
# return_value.age_total=size(total_age,2);
# death_age=find([global_vars.REMOVED_LIST.age]<18);
# return_value.age_death=size(death_age,2);
# #
# end