import xlrd
import simulation # main simulation
import numpy as np
import math
import global_vars ## all the global variables are defined in a seperate file
import Patient #Patient class
import Donor  # donor class
import AddDonor
import AddPatient
import fns # functions
from statistics import mean
from statistics import stdev
import scipy.stats
import pandas as pd
import xlwt
import matplotlib.pyplot as plt
from xlwt import Workbook
import matplotlib.pyplot as plt

city = xlrd.open_workbook("citylist.xls")
citySheet = city.sheet_by_index(0)
city_list_Kerala = []
for i in range(14):
    city_list_Kerala.append(citySheet.cell_value(i+1, 0))

dist = xlrd.open_workbook("DistMatrix1.xls")
distSheet = dist.sheet_by_index(0)
DistanceMatrix_Kerala = []
for i in range(len(city_list_Kerala)):
    temp = []
    for j in range(len(city_list_Kerala)):
        temp.append(distSheet.cell_value(i,j))
    DistanceMatrix_Kerala.append(temp)

dist = xlrd.open_workbook("DistMatrix1.xls")
distSheet = dist.sheet_by_index(1)
DurationMatrix_Kerala = []
for i in range(len(city_list_Kerala)):
    temp = []
    for j in range(len(city_list_Kerala)):
        temp.append(distSheet.cell_value(i,j))
    DurationMatrix_Kerala.append(temp)

# taking the initial waitlist from file, Gonaa be useless because cities names are not consistent with citylist names so I've generated 250 patients prior to each simulations and not included these
# patients = xlrd.open_workbook("init_waitlist.xlsx")Ft
# patientSheet = patients.sheet_by_index(0)
# init_waitlist = []     #init_waitlist me cities badlo

global_vars.TRANSPORT_TIME = 0
global_vars.years = 30
replication=3
global_vars.warmupperiod=12
global_vars.repnumber=0
avg_tranport_time=0
avg_waiting_time=0
global_vars.DIST=[]

avg_bg= [0,0,0,0]
avg_hospital = [0,0]
alloc_hosp_num = [1,2]
avg_patients=0
avg_deaths=0
avg_waste=0
avg_organs=0
avg_bg_a=0
avg_bg_b=0
avg_bg_c=0
avg_bg_o=0
avg_bgp_a=0
avg_bgp_b=0
avg_bgp_c=0
avg_bgp_o=0
wait_hosp_num = [0,0]
wait_bg_num = [0,0,0,0]
total_hosp_num = [0,0]
total_bg_num= [0,0,0,0]
age_alloc=0
age_death=0
age_total=0
avg_awt= np.zeros((replication,global_vars.years))
avg_size= np.zeros((replication,global_vars.years))
A_O=[]
A_P=[]
A_D=[]
a_o=[]
a_p=[]
a_d=[]
A_BG_A=[]
A_BG_B=[]
A_BG_C=[]
A_BG_O=[]
a_bg_a=[]
a_bg_b=[]
a_bg_c=[]
a_bg_o=[]
A_BGP_A=[]
A_BGP_B=[]
A_BGP_C=[]
A_BGP_O=[]
a_bgp_a=[]
a_bgp_b=[]
a_bgp_c=[]
a_bgp_o=[]
A_W=[]
P_T=[]
P_A_A=[]
P_A_B=[]
P_A_C=[]
P_A_O=[]
global_vars.prob_transplant=0
global_vars.prob_transplant_hosp_p=0
global_vars.prob_transplant_hosp_g=0
global_vars.prob_transplant_A=0
global_vars.prob_transplant_B=0
global_vars.prob_transplant_O=0
global_vars.prob_transplant_AB=0

global_vars.WAITLISTEDPATIENT_each_year=np.zeros((replication,global_vars.years))
global_vars.WAITLISTEDPATIENT_BG_A_each_year=np.zeros((replication,global_vars.years))
global_vars.WAITLISTEDPATIENT_BG_B_each_year=np.zeros((replication,global_vars.years))
global_vars.WAITLISTEDPATIENT_BG_O_each_year=np.zeros((replication,global_vars.years))
global_vars.WAITLISTEDPATIENT_BG_AB_each_year=np.zeros((replication,global_vars.years))
global_vars.WAITLISTEDPATIENT_G_HOS_each_year=np.zeros((replication,global_vars.years))
global_vars.WAITLISTEDPATIENT_P_HOS_each_year=np.zeros((replication,global_vars.years))
global_vars.DEATH_each_year=np.zeros((replication,global_vars.years))

global_vars.UNALLOCATED_ORGANS_each_year=np.zeros((replication,global_vars.years))

global_vars.A_each_year=np.zeros((replication,global_vars.years))
global_vars.B_each_year=np.zeros((replication,global_vars.years))
global_vars.O_each_year=np.zeros((replication,global_vars.years))
global_vars.AB_each_year=np.zeros((replication,global_vars.years))
global_vars.hosp_p_each_year=np.zeros((replication,global_vars.years))
global_vars.hosp_g_each_year= np.zeros((replication,global_vars.years))

avg_p_15=np.zeros((replication,global_vars.years))
avg_o_15=np.zeros((replication,global_vars.years))
avg_d_15=np.zeros((replication,global_vars.years))


global_vars.donor=np.zeros((replication,global_vars.years))
global_vars.Organ_BG_AB=np.zeros((replication,global_vars.years))
global_vars.Organ_BG_A=np.zeros((replication,global_vars.years))
global_vars.Organ_BG_B=np.zeros((replication,global_vars.years))
global_vars.Organ_BG_O=np.zeros((replication,global_vars.years))
global_vars.Organ_from_P_Hosp=np.zeros((replication,global_vars.years))
global_vars.Organ_from_G_Hosp=np.zeros((replication,global_vars.years))

global_vars.patient_each_year=np.zeros((replication,global_vars.years,5))

global_vars.patient_B_each_year=np.zeros((replication,global_vars.years,5))

global_vars.patient_O_each_year=np.zeros((replication,global_vars.years,5))

global_vars.patient_A_each_year=np.zeros((replication,global_vars.years,5))

global_vars.patient_AB_each_year=np.zeros((replication,global_vars.years,5))

global_vars.patient_P_hosp_each_year=np.zeros((replication,global_vars.years,5))
global_vars.patient_G_hosp_each_year=np.zeros((replication,global_vars.years,5))

global_vars.ALLOCATED=np.zeros((replication,global_vars.years-global_vars.warmupperiod-5,5))
global_vars.ALLOCATED_hosp_p=np.zeros((replication,global_vars.years-global_vars.warmupperiod-5,5))
global_vars.ALLOCATED_hosp_g=np.zeros((replication,global_vars.years-global_vars.warmupperiod-5,5))
global_vars.ALLOCATED_bg_A=np.zeros((replication,global_vars.years-global_vars.warmupperiod-5,5))
global_vars.ALLOCATED_bg_B=np.zeros((replication,global_vars.years-global_vars.warmupperiod-5,5))
global_vars.ALLOCATED_bg_O=np.zeros((replication,global_vars.years-global_vars.warmupperiod-5,5))
global_vars.ALLOCATED_bg_AB=np.zeros((replication,global_vars.years-global_vars.warmupperiod-5,5))

global_vars.patient_each_year=np.zeros((replication,global_vars.years,5))

global_vars.patient_15=np.zeros((replication,global_vars.years))
global_vars.alloc_15=np.zeros((replication,global_vars.years))
global_vars.death_15=np.zeros((replication,global_vars.years))
global_vars.donor=np.zeros((replication,global_vars.years))
global_vars.patients_alloc_each_year=np.zeros((replication,global_vars.years))

global_vars.transport_time=np.zeros((replication,global_vars.years))
global_vars.avg_transport_time=np.zeros((replication,global_vars.years))
global_vars.time_to_alloc=np.zeros((replication,global_vars.years))
global_vars.avg_time_to_alloc=np.zeros((replication,global_vars.years))
global_vars.alloc_for_prob=np.zeros((replication,global_vars.years))
global_vars.time_by_hosp_p=np.zeros((replication,global_vars.years))
global_vars.time_by_hosp_g=np.zeros((replication,global_vars.years))
global_vars.avg_time_by_hosp_p=np.zeros((replication,global_vars.years))
global_vars.avg_time_by_hosp_g=np.zeros((replication,global_vars.years))
global_vars.patients_donated_hosp_p=np.zeros((replication,global_vars.years))
global_vars.patients_donated_hosp_g=np.zeros((replication,global_vars.years))
global_vars.A_alloc_per_year=np.zeros((replication,global_vars.years))
global_vars.B_alloc_per_year=np.zeros((replication,global_vars.years))
global_vars.O_alloc_per_year=np.zeros((replication,global_vars.years))
global_vars.AB_alloc_per_year=np.zeros((replication,global_vars.years))
global_vars.time_by_bgA=np.zeros((replication,global_vars.years))
global_vars.time_by_bgB=np.zeros((replication,global_vars.years))
global_vars.time_by_bgO=np.zeros((replication,global_vars.years))
global_vars.time_by_bgAB=np.zeros((replication,global_vars.years))
global_vars.avg_time_by_bgA=np.zeros((replication,global_vars.years))
global_vars.avg_time_by_bgB=np.zeros((replication,global_vars.years))
global_vars.avg_time_by_bgO=np.zeros((replication,global_vars.years))
global_vars.avg_time_by_bgAB=np.zeros((replication,global_vars.years))

global_vars.unalloc_organs_per_year=np.zeros((replication,global_vars.years))


global_vars.Donor=np.zeros((replication,global_vars.years))
global_vars.Donor_BG_AB=np.zeros((replication,global_vars.years))
global_vars.Donor_BG_A=np.zeros((replication,global_vars.years))
global_vars.Donor_BG_B=np.zeros((replication,global_vars.years))
global_vars.Donor_BG_O=np.zeros((replication,global_vars.years))
global_vars.Donor_from_P_Hosp=np.zeros((replication,global_vars.years))
global_vars.Donor_from_G_Hosp=np.zeros((replication,global_vars.years))

print('Simulation started!')
print('Number of replications completed:')



clock=0

p_arrival=fns.PatientInterArrivalTime()

d_arrival=fns.DonorInterArrivalTime()
##Stabilising the patient interarrival and donor interarrival by taking radom values for a year and then subtracting a year
while clock<365*24:
   if p_arrival<d_arrival:
       clock=p_arrival
       p_arrival=clock+fns.PatientInterArrivalTime()
   else:
       clock=d_arrival
       d_arrival=clock+fns.DonorInterArrivalTime()

p_arrival=p_arrival-365*24
d_arrival=d_arrival-365*24
steady=[p_arrival,d_arrival]

wb3= xlwt.Workbook()
wb3ws2=wb3.add_sheet("Probability")
# wb3ws3=wb3.add_sheet(f"ML{r+1}")
##main loop
for x in range(replication):
    print("replication: ", x)
    global_vars.repnumber=x
    value = simulation.simulation(global_vars.years,city_list_Kerala, DurationMatrix_Kerala,steady,replication)

    print(f'Replication {x+1} Completed!')

    global_vars.ALLOCATED_LIST_P.sort(key=lambda x: x.id)
    global_vars.ALLOCATED_LIST.sort(key=lambda x: x.Pid)
    global_vars.REMOVED_LIST.sort(key=lambda x: x.id)
    global_vars.DL= global_vars.DL[~np.all(global_vars.DL == 0, axis=1)]
    global_vars.RL= global_vars.RL[~np.all(global_vars.RL == 0, axis=1)]
    global_vars.WL = global_vars.WL[~np.all(global_vars.WL == 0, axis=1)]
    # #Next sheet, Sheet number
    wb3ws3=wb3.add_sheet(f"ML{x+1}")


    wb3ws3.write(0,0,'id')
    wb3ws3.write(0,1,'age')
    wb3ws3.write(0,2,'city_index')
    wb3ws3.write(0,3,'bloodgroup')
    wb3ws3.write(0,4,'rtime')
    wb3ws3.write(0,5,'kap_score')
    wb3ws3.write(0,6,'hosp_name')
    wb3ws3.write(0,7,'hosp_type')
    wb3ws3.write(0,8,'pra')
    wb3ws3.write(0,9,'avg')
    wb3ws3.write(0,10,'av_fitsula')
    wb3ws3.write(0,11,'time_on_dailysis')
    wb3ws3.write(0,12,'pigf')
    wb3ws3.write(0,13,'position on waitlist')
    wb3ws3.write(0,14,'patients aboove this patient')
    wb3ws3.write(0,15,'A patients above')
    wb3ws3.write(0,16,'B patients above')
    wb3ws3.write(0,17,'O patients above')
    wb3ws3.write(0,18,'AB patients above')
    wb3ws3.write(0,19,'Time to allocation')
    wb3ws3.write(0,20,'total patients on waitlist')
    wb3ws3.write(0,21,'total A patients')
    wb3ws3.write(0,22,'total B patients')
    wb3ws3.write(0,23,'total O patients')
    wb3ws3.write(0,24,'total AB patients')
    wb3ws3.write(0,25,'pra type')
    wb3ws3.write(0,26,'status')
    wb3ws3.write(0,27,'5th year status')
    wb3ws3.write(0,28,'2nd year status')
    wb3ws3.write(0,29,'1st year status')

    for i in range(len(global_vars.WL)):
        wb3ws3.write(i+1,6,global_vars.WL[i][18])
        wb3ws3.write(i+1,7,global_vars.WL[i][6])
        wb3ws3.write(i+1,0,global_vars.WL[i][0])
        wb3ws3.write(i+1,1,global_vars.WL[i][1])
        wb3ws3.write(i+1,2,global_vars.WL[i][2])
        wb3ws3.write(i+1,3,global_vars.WL[i][3])
        wb3ws3.write(i+1,4,global_vars.WL[i][4])
        wb3ws3.write(i+1,5,global_vars.WL[i][5])
        wb3ws3.write(i+1,8,global_vars.WL[i][7])
        wb3ws3.write(i+1,9,global_vars.WL[i][8])
        wb3ws3.write(i+1,10,global_vars.WL[i][9])
        wb3ws3.write(i+1,11,global_vars.WL[i][10])
        wb3ws3.write(i+1,12,global_vars.WL[i][11])
        wb3ws3.write(i+1,13,global_vars.WL[i][12])
        wb3ws3.write(i+1,14,global_vars.WL[i][13])
        wb3ws3.write(i+1,15,global_vars.WL[i][14])
        wb3ws3.write(i+1,16,global_vars.WL[i][15])
        wb3ws3.write(i+1,17,global_vars.WL[i][16])
        wb3ws3.write(i+1,18,global_vars.WL[i][17])
        wb3ws3.write(i+1,20,global_vars.WL[i][19])
        wb3ws3.write(i+1,21,global_vars.WL[i][20])
        wb3ws3.write(i+1,22,global_vars.WL[i][21])
        wb3ws3.write(i+1,23,global_vars.WL[i][22])
        wb3ws3.write(i+1,24,global_vars.WL[i][23])
        wb3ws3.write(i+1,25,global_vars.WL[i][24])

    for i in range(len(global_vars.WL)):
        for j in range(len(global_vars.DL)):
            if global_vars.WL[i][0] == global_vars.DL[j][1]:
                wb3ws3.write(i + 1, 26, 'Y')
                wb3ws3.write(i + 1, 19, global_vars.DL[j][2])
                break

    for i in range(len(global_vars.WL)):
        for j in range(len(global_vars.DL1)):
            if global_vars.WL[i][0] == global_vars.DL1[j][0]:
                wb3ws3.write(i + 1, 29, 'Y')
                break

    for i in range(len(global_vars.WL)):
        for j in range(len(global_vars.DL2)):
            if global_vars.WL[i][0] == global_vars.DL2[j][0]:
                wb3ws3.write(i + 1, 28, 'Y')
                break

    for i in range(len(global_vars.WL)):
        for j in range(len(global_vars.DL5)):
            if global_vars.WL[i][0] == global_vars.DL5[j][0]:
                wb3ws3.write(i + 1, 27, 'Y')
                break

    for i in range(len(global_vars.WL)):
        for j in range(len(global_vars.RL)):
            if global_vars.WL[i][0] == global_vars.RL[j][0]:
                wb3ws3.write(i + 1, 26, 'N')
                break


avg_transport_time=global_vars.transport_time/global_vars.patients_alloc_each_year
avg_time_to_alloc=global_vars.time_to_alloc/global_vars.patients_alloc_each_year
avg_time_by_hosp_p=global_vars.time_by_hosp_p/global_vars.patients_donated_hosp_p
avg_time_by_hosp_g=global_vars.time_by_hosp_g/global_vars.patients_donated_hosp_g
avg_time_by_bgA=global_vars.time_by_bgA/global_vars.A_alloc_per_year
avg_time_by_bgB=global_vars.time_by_bgB/global_vars.B_alloc_per_year
avg_time_by_bgO=global_vars.time_by_bgO/global_vars.O_alloc_per_year
avg_time_by_bgAB=global_vars.time_by_bgAB/global_vars.AB_alloc_per_year
unalloc_organs=global_vars.donor-global_vars.patients_alloc_each_year


# wb3= xlwt.Workbook()
# wb3ws2=wb3.add_sheet("Probability")
# # wb3ws3=wb3.add_sheet(f"ML{r+1}")

# for r in range(replication):
#     wb3ws=wb3.add_sheet(f"replication{r+1}")

#     wb3ws.write(0,0,"Years")
#     wb3ws.write(1,0,"Average deaths")
#     wb3ws.write(2,0,"Average organs allocated")
#     wb3ws.write(3,0,"Average wait to allocation")
#     wb3ws.write(4,0,"Average time to transportation")
#     wb3ws.write(5,0,"Allocation in government hospital")
#     wb3ws.write(6,0,"Allocation in private hsopital")
#     wb3ws.write(7,0,"Blood group A allocations")
#     wb3ws.write(8,0,"Blood group AB allocations")
#     wb3ws.write(9,0,"Blood group B allocations")
#     wb3ws.write(10,0,"Blood group O allocations")
#     wb3ws.write(11,0,"Average unallocated organs")
#     wb3ws.write(12,0,"Waitlisted patients")
#     wb3ws.write(13,0,"Waitlisted patient in government hospital")
#     wb3ws.write(14,0,"Waitlisted patient in private hospital")
#     wb3ws.write(15,0,"Waitlisted patient in BG A")
#     wb3ws.write(16,0,"Waitlisted patient in BG AB")
#     wb3ws.write(17,0,"Waitlisted patient in BG B")
#     wb3ws.write(18,0,"Waitlisted patient in BG O")
#     wb3ws.write(19,0,"Total patients")
#     wb3ws.write(20,0,"patients in BG A")
#     wb3ws.write(21,0,"patients in BG AB")
#     wb3ws.write(22,0,"patients in BG B")
#     wb3ws.write(23,0,"patients in BG O")
#     wb3ws.write(24,0,"Patients in govt hosp")
#     wb3ws.write(25,0,"Patients in pvt hosp")
#     wb3ws.write(26,0,"Total Organs arrived")
#     wb3ws.write(27,0,"Total Organs of BG A")
#     wb3ws.write(28,0,"Total Organs of BG AB")
#     wb3ws.write(29,0,"Total Organs of BG O")
#     wb3ws.write(30,0,"Total Organs of BG B")
#     wb3ws.write(31,0,"Total Ograns from Private Hosp")
#     wb3ws.write(32,0,"Total Organs from Gov Hosp")
#     wb3ws.write(33,0,"Average time to alloc in gov hosp")
#     wb3ws.write(34,0,"Average time to alloc in pvt hosp")
#     wb3ws.write(35,0,"Average time to alloc BG A")
#     wb3ws.write(36,0,"Average time to alloc BG B")
#     wb3ws.write(37,0,"Average time to alloc BG AB")
#     wb3ws.write(38,0,"Average time to alloc BG O")
#     wb3ws.write(39,0,"Donor arrived")
#     wb3ws.write(40,0,"Donor arrived AB")
#     wb3ws.write(41,0,"Donor arrived A")
#     wb3ws.write(42,0,"Donor arrived B")
#     wb3ws.write(43,0,"Donor arrived O")
#     wb3ws.write(44,0,"Donor arrived P")
#     wb3ws.write(45,0,"Donor arrived G")

#     for i in range(global_vars.years):
#         wb3ws.write(1,i+1,global_vars.DEATH_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(2,i+1,global_vars.patients_alloc_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(3,i+1,avg_time_to_alloc[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(4,i+1,avg_transport_time[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(5,i+1,global_vars.patients_donated_hosp_g[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(6,i+1,global_vars.patients_donated_hosp_p[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(7,i+1,global_vars.A_alloc_per_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(8,i+1,global_vars.AB_alloc_per_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(9,i+1,global_vars.B_alloc_per_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(10,i+1,global_vars.O_alloc_per_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(11,i+1,unalloc_organs[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(12,i+1,global_vars.WAITLISTEDPATIENT_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(13,i+1,global_vars.WAITLISTEDPATIENT_G_HOS_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(14,i+1,global_vars.WAITLISTEDPATIENT_P_HOS_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(15,i+1,global_vars.WAITLISTEDPATIENT_BG_A_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(16,i+1,global_vars.WAITLISTEDPATIENT_BG_AB_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(17,i+1,global_vars.WAITLISTEDPATIENT_BG_B_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(18,i+1,global_vars.WAITLISTEDPATIENT_BG_O_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(19,i+1,global_vars.patient_15[r][i])

#     for i in range(global_vars.years):
#         wb3ws.write(20,i+1,global_vars.A_each_year[r][i])

#     for i in range(global_vars.years):
#         wb3ws.write(21,i+1,global_vars.AB_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(22,i+1,global_vars.B_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(23,i+1,global_vars.O_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(24,i+1,global_vars.hosp_g_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(25,i+1,global_vars.hosp_p_each_year[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(26,i+1,global_vars.donor[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(27,i+1,global_vars.Organ_BG_A[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(28,i+1,global_vars.Organ_BG_AB[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(29,i+1,global_vars.Organ_BG_O[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(30,i+1,global_vars.Organ_BG_B[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(31,i+1,global_vars.Organ_from_P_Hosp[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(32,i+1,global_vars.Organ_from_G_Hosp[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(33,i+1,avg_time_by_hosp_g[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(34,i+1,avg_time_by_hosp_p[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(35,i+1,avg_time_by_bgA[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(36,i+1,avg_time_by_bgB[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(37,i+1,avg_time_by_bgAB[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(38,i+1,avg_time_by_bgO[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(39,i+1,global_vars.Donor[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(40,i+1,global_vars.Donor_BG_AB[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(41,i+1,global_vars.Donor_BG_A[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(42,i+1,global_vars.Donor_BG_B[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(43,i+1,global_vars.Donor_BG_O[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(44,i+1,global_vars.Donor_from_P_Hosp[r][i])
#     for i in range(global_vars.years):
#         wb3ws.write(45,i+1,global_vars.Donor_from_G_Hosp[r][i])

# global_vars.prob_transplant=global_vars.ALLOCATED/global_vars.patient_each_year[:,global_vars.warmupperiod:global_vars.years-5,:]
# global_vars.prob_transplant_hosp_p=global_vars.ALLOCATED_hosp_p/global_vars.patient_P_hosp_each_year[:,global_vars.warmupperiod:global_vars.years-5,:]
# global_vars.prob_transplant_hosp_g=global_vars.ALLOCATED_hosp_g/global_vars.patient_G_hosp_each_year[:,global_vars.warmupperiod:global_vars.years-5,:]
# global_vars.prob_transplant_A=global_vars.ALLOCATED_bg_A/global_vars.patient_A_each_year[:,global_vars.warmupperiod:global_vars.years-5,:]
# global_vars.prob_transplant_B=global_vars.ALLOCATED_bg_B/global_vars.patient_B_each_year[:,global_vars.warmupperiod:global_vars.years-5,:]
# global_vars.prob_transplant_O=global_vars.ALLOCATED_bg_O/global_vars.patient_O_each_year[:,global_vars.warmupperiod:global_vars.years-5,:]
# global_vars.prob_transplant_AB=global_vars.ALLOCATED_bg_AB/global_vars.patient_AB_each_year[:,global_vars.warmupperiod:global_vars.years-5,:]
# k=0
# o=0

# for j in range(replication):
#     k=global_vars.prob_transplant[j,:,:]
#     o=np.mean(k,axis=0)
#     for i in range(5):
#         wb3ws2.write(j+2,i+1,o[i])

# for j in range(replication):
#     k=global_vars.prob_transplant_hosp_p[j,:,:]
#     o=np.mean(k,axis=0)
#     for i in range(len(o)):
#         wb3ws2.write(j+2,i+7,o[i])

# for j in range(replication):
#     k=global_vars.prob_transplant_hosp_g[j,:,:]
#     o=np.mean(k,axis=0)
#     for i in range(5):
#         wb3ws2.write(j+2,i+14,o[i])

# for j in range(replication):
#     k=global_vars.prob_transplant_A[j,:,:]
#     o=np.mean(k,axis=0)
#     for i in range(5):
#         wb3ws2.write(j+2,i+21,o[i])

# for j in range(replication):
#     k=global_vars.prob_transplant_B[j,:,:]
#     o=np.mean(k,axis=0)
#     for i in range(5):
#         wb3ws2.write(j+2,i+28,o[i])
# for j in range(replication):
#     k=global_vars.prob_transplant_AB[j,:,:]
#     o=np.mean(k,axis=0)
#     for i in range(5):
#         wb3ws2.write(j+2,i+35,o[i])
# for j in range(replication):
#     k=global_vars.prob_transplant_O[j,:,:]
#     o=np.mean(k,axis=0)
#     for i in range(5):
#         wb3ws2.write(j+2,i+42,o[i])



# global_vars.DL= global_vars.DL[~np.all(global_vars.DL == 0, axis=1)]
# global_vars.RL= global_vars.RL[~np.all(global_vars.RL == 0, axis=1)]
# global_vars.WL = global_vars.WL[~np.all(global_vars.WL == 0, axis=1)]
# #Next sheet, Sheet number
# wb3ws3=wb3.add_sheet("ML")


# wb3ws3.write(0,0,'id')
# wb3ws3.write(0,1,'age')
# wb3ws3.write(0,2,'city_index')
# wb3ws3.write(0,3,'bloodgroup')
# wb3ws3.write(0,4,'rtime')
# wb3ws3.write(0,5,'kap_score')
# wb3ws3.write(0,6,'hosp_name')
# wb3ws3.write(0,7,'hosp_type')
# wb3ws3.write(0,8,'pra')
# wb3ws3.write(0,9,'avg')
# wb3ws3.write(0,10,'av_fitsula')
# wb3ws3.write(0,11,'time_on_dailysis')
# wb3ws3.write(0,12,'pigf')
# wb3ws3.write(0,13,'position on waitlist')
# wb3ws3.write(0,14,'patients aboove this patient')
# wb3ws3.write(0,15,'A patients above')
# wb3ws3.write(0,16,'B patients above')
# wb3ws3.write(0,17,'O patients above')
# wb3ws3.write(0,18,'AB patients above')
# wb3ws3.write(0,19,'Time to allocation')
# wb3ws3.write(0,20,'total patients on waitlist')
# wb3ws3.write(0,21,'total A patients')
# wb3ws3.write(0,22,'total B patients')
# wb3ws3.write(0,23,'total O patients')
# wb3ws3.write(0,24,'total AB patients')
# wb3ws3.write(0,25,'pra type')
# wb3ws3.write(0,26,'status')
# wb3ws3.write(0,27,'5th year status')
# wb3ws3.write(0,28,'2nd year status')
# wb3ws3.write(0,29,'1st year status')

# for i in range(len(global_vars.WL)):
#     wb3ws3.write(i+1,6,global_vars.WL[i][18])
#     wb3ws3.write(i+1,7,global_vars.WL[i][6])
#     wb3ws3.write(i+1,0,global_vars.WL[i][0])
#     wb3ws3.write(i+1,1,global_vars.WL[i][1])
#     wb3ws3.write(i+1,2,global_vars.WL[i][2])
#     wb3ws3.write(i+1,3,global_vars.WL[i][3])
#     wb3ws3.write(i+1,4,global_vars.WL[i][4])
#     wb3ws3.write(i+1,5,global_vars.WL[i][5])
#     wb3ws3.write(i+1,8,global_vars.WL[i][7])
#     wb3ws3.write(i+1,9,global_vars.WL[i][8])
#     wb3ws3.write(i+1,10,global_vars.WL[i][9])
#     wb3ws3.write(i+1,11,global_vars.WL[i][10])
#     wb3ws3.write(i+1,12,global_vars.WL[i][11])
#     wb3ws3.write(i+1,13,global_vars.WL[i][12])
#     wb3ws3.write(i+1,14,global_vars.WL[i][13])
#     wb3ws3.write(i+1,15,global_vars.WL[i][14])
#     wb3ws3.write(i+1,16,global_vars.WL[i][15])
#     wb3ws3.write(i+1,17,global_vars.WL[i][16])
#     wb3ws3.write(i+1,18,global_vars.WL[i][17])
#     wb3ws3.write(i+1,20,global_vars.WL[i][19])
#     wb3ws3.write(i+1,21,global_vars.WL[i][20])
#     wb3ws3.write(i+1,22,global_vars.WL[i][21])
#     wb3ws3.write(i+1,23,global_vars.WL[i][22])
#     wb3ws3.write(i+1,24,global_vars.WL[i][23])
#     wb3ws3.write(i+1,25,global_vars.WL[i][24])

# for i in range(len(global_vars.WL)):
#     for j in range(len(global_vars.DL)):
#         if global_vars.WL[i][0] == global_vars.DL[j][1]:
#             wb3ws3.write(i + 1, 26, 'Y')
#             wb3ws3.write(i + 1, 19, global_vars.DL[j][2])
#             break

# for i in range(len(global_vars.WL)):
#     for j in range(len(global_vars.DL1)):
#         if global_vars.WL[i][0] == global_vars.DL1[j][0]:
#             wb3ws3.write(i + 1, 29, 'Y')
#             break

# for i in range(len(global_vars.WL)):
#     for j in range(len(global_vars.DL2)):
#         if global_vars.WL[i][0] == global_vars.DL2[j][0]:
#             wb3ws3.write(i + 1, 28, 'Y')
#             break

# for i in range(len(global_vars.WL)):
#     for j in range(len(global_vars.DL5)):
#         if global_vars.WL[i][0] == global_vars.DL5[j][0]:
#             wb3ws3.write(i + 1, 27, 'Y')
#             break

# for i in range(len(global_vars.WL)):
#     for j in range(len(global_vars.RL)):
#         if global_vars.WL[i][0] == global_vars.RL[j][0]:
#             wb3ws3.write(i + 1, 26, 'N')
#             break

print("SIMULATION END")
wb3.save("Results_Kerala_2611_equaldonorprob.xls")