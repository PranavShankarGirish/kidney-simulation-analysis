import Donor
import random
from random import *
from random import randint
import numpy as np
import math
import fns
import xlrd
import global_vars

global_vars.transportation_time=0
global_vars.Patient_id=0
global_vars.Patient_hostpital_type=0
global_vars.Patient_bloodgroup=0
global_vars.found=0

def AddDonor():
    import global_vars
    recieving_city_index,hosp = calc_recieving_city()
    bgroup = calc_bgroup()
    age = calc_age()
    global_vars.transportation_time = 0
    global_vars.Patient_id = 0
    global_vars.Patient_hostpital_type = 0
    global_vars.Patient_bloodgroup = 0
    global_vars.found = 0
    Number_of_kidney_retrived_per_donor=pronumkidney()
    global_vars.WAITLIST.sort(reverse=True,key=lambda x: x.kap_score)
    global_vars.found = False
    global_vars.c=0
    global_vars.b=0
    global_vars.Patient_id=0

    def PatientRecievingKidney(Hospital_type, patient_age_limit, CURRENTWAITLISTTYPE):
        global_vars.CITY_WAITLIST[recieving_city_index].sort(reverse=True,key=lambda x: x.kap_score)
        if CURRENTWAITLISTTYPE=="District":
            for P in global_vars.CITY_WAITLIST[recieving_city_index]:
                if P.hospital_type==Hospital_type and (check_bg_compatibility(bgroup, P.bloodgroup))  and P.age<patient_age_limit:
                    global_vars.transplantation_time=math.ceil(random()*3)
                    global_vars.ALLOCATED_LIST.append(Donor.Donor(global_vars.CLOCK_SIM,P.id,P.bloodgroup, hosp, P.hospital_name,P.hospital_type, P.age, bgroup, age, recieving_city_index, recieving_city_index, 0, global_vars.transplantation_time, global_vars.transplantation_time,"Kerala"))
                    global_vars.ALLOCATED_LIST_P.append(P)
                    global_vars.CITY_WAITLIST[recieving_city_index].remove(P)
                    global_vars.c=1
                    global_vars.Patient_id=P.id
                    global_vars.Patient_hostpital_type=P.hospital_type
                    global_vars.Patient_bloodgroup=P.bloodgroup
                    global_vars.Patient_recieving_city_index=P.recievingcityindex
                    print("hey")
                    break
            if global_vars.c==1:
                for P in global_vars.WAITLIST:
                    if global_vars.Patient_id==P.id:
                        global_vars.WAITLIST.remove(P)
                        global_vars.b=1
                        break
            if global_vars.b==1 and global_vars.c==1:
                print("District")
                global_vars.found=True
        if CURRENTWAITLISTTYPE=="State":
            for P in global_vars.WAITLIST:
                if P.hospital_type==Hospital_type and (check_bg_compatibility(bgroup, P.bloodgroup))  and P.age<patient_age_limit :
                    global_vars.transplantation_time=math.ceil(random()*3)
                    global_vars.transportation_time=global_vars.DURATION[recieving_city_index][P.recievingcityindex]
                    global_vars.ALLOCATED_LIST.append(Donor.Donor(global_vars.CLOCK_SIM,P.id,P.bloodgroup, hosp, P.hospital_name,P.hospital_type, P.age, bgroup, age, recieving_city_index, P.recievingcityindex, global_vars.transportation_time, global_vars.transplantation_time, global_vars.transplantation_time+global_vars.transportation_time,"Karnataka"))
                    global_vars.ALLOCATED_LIST_P.append(P)
                    global_vars.WAITLIST.remove(P)
                    global_vars.c=1
                    global_vars.Patient_id=P.id
                    global_vars.Patient_recieving_city_index=P.recievingcityindex
                    global_vars.Patient_hostpital_type=P.hospital_type
                    global_vars.Patient_bloodgroup=P.bloodgroup
                    print("hoy")
                    break
            if global_vars.c==1:
                global_vars.CITY_WAITLIST[global_vars.Patient_recieving_city_index].sort(reverse=True,key=lambda x: x.kap_score)
                for P in global_vars.CITY_WAITLIST[global_vars.Patient_recieving_city_index]:
                    if global_vars.Patient_id==P.id:
                        global_vars.CITY_WAITLIST[global_vars.Patient_recieving_city_index].remove(P)
                        global_vars.b=1
                        break
            if global_vars.b==1 and global_vars.c==1:
                print("State")
                global_vars.found=True
    g=0
    while g<2:
        global_vars.c=0
        global_vars.b=0
        global_vars.transportation_time=0
        global_vars.Patient_id=0
        global_vars.Patient_hostpital_type=0
        global_vars.Patient_bloodgroup=0
        global_vars.Patient_recieving_city_index=0
        global_vars.found=False
        if len(global_vars.CITY_WAITLIST[recieving_city_index])!=0:
            if hosp=="G":
                if age<18:
                    PatientRecievingKidney("G",18, "District")
                    print("Patient ,age<18,G  Donor,age<18,G  ,District")
                    if global_vars.found==False:
                        PatientRecievingKidney("G",1000, "District")
                        print("Patient ,age any ,G  Donor,age<18,G  ,District")
                if age>18:
                    PatientRecievingKidney("G",1000, "District")
                    print("Patient ,age any ,G  Donor,age>18,G  ,District")

                if global_vars.found==False:
                    if age<18:
                        PatientRecievingKidney("G",18, "State")
                        print("Patient ,age<18,G  Donor,age<18,G  ,Statet")
                        if global_vars.found==False:
                            PatientRecievingKidney("G",1000, "State")
                            print("Patient ,age any ,G  Donor,age<18,G  ,State")
                    if age>18:
                        PatientRecievingKidney("G",1000, "State")
                        print("Patient ,age any ,G  Donor,age>18,G  ,State")

                if global_vars.found==False:

                    if age<18:
                        PatientRecievingKidney("P",18, "District")
                        print("Patient ,age<18,P  Donor,age<18,G  ,District")
                        if global_vars.found==False:
                            PatientRecievingKidney("P",1000, "District")
                            print("Patient ,age any ,P  Donor,age<18,G  ,District")
                    if age>18:
                        PatientRecievingKidney("P",1000, "District")
                        print("Patient ,age any ,P  Donor,age>18,G  ,District")

                if global_vars.found==False:
                    if age<18:
                        PatientRecievingKidney("P",18, "State")
                        print("Patient ,age<18,P  Donor,age<18,G  ,Statet")
                        if global_vars.found==False:
                            PatientRecievingKidney("P",1000, "State")
                    if age>18:
                        PatientRecievingKidney("P",1000, "State")
                        print("Patient ,age any ,P  Donor,age>18,G  ,State")
                if global_vars.found==False:
                    global_vars.ORGAN_WASTE = global_vars.ORGAN_WASTE + 1
                    print('organ_waste')

            if hosp=="P":
                if age<18:
                    PatientRecievingKidney("P",18, "District")
                    print("Patient ,age<18,P  Donor,age<18,P  ,District")
                    if global_vars.found==False:
                        PatientRecievingKidney("P",1000, "District")
                        print("Patient ,age any ,P  Donor,age<18,P  ,District")

                if age>18:
                    PatientRecievingKidney("P",1000, "District")
                    print("Patient ,age any ,P  Donor,age>18,P  ,District")

                if global_vars.found==False:
                    if age<18:
                        PatientRecievingKidney("P",18, "State")
                        print("Patient ,age<18,P  Donor,age<18,P  ,Statet")
                        if global_vars.found==False:
                            PatientRecievingKidney("P",1000, "State")
                            print("Patient ,age any ,P  Donor,age<18,P  ,State")
                    if age>18:
                        PatientRecievingKidney("P",1000, "State")
                        print("Patient ,age any ,P  Donor,age>18,  P,State")
                if global_vars.found==False:
                    if age<18:
                        PatientRecievingKidney("G",18, "District")
                        print("Patient ,age<18,G  Donor,age<18,P  ,District")
                        if global_vars.found==False:
                            PatientRecievingKidney("G",1000, "District")
                            print("Patient ,age any ,G  Donor,age<18,P  ,District")
                    if age>18:
                        PatientRecievingKidney("G",1000, "District")
                        print("Patient ,age any ,G  Donor,age>18,P  ,District")
                if global_vars.found==False:
                    if age<18:
                        PatientRecievingKidney("G",18, "State")
                        print("Patient ,age<18,G  Donor,age<18,P  ,Statet")
                        if global_vars.found==False:
                            PatientRecievingKidney("G",1000, "State")
                            print("Patient ,age any ,G  Donor,age<18,P  ,Statet")
                    if age>18:
                        PatientRecievingKidney("G",1000, "State")
                        print("Patient ,age any ,G  Donor,age>18,P  ,Statet")
                if global_vars.found==False:
                    global_vars.ORGAN_WASTE = global_vars.ORGAN_WASTE + 1
                    print('organ_waste')
        else:
            if hosp=="G":
                if age<18:
                    PatientRecievingKidney("G",18, "State")
                    if global_vars.found==False:
                        PatientRecievingKidney("G",1000, "State")
                if age>18:
                    PatientRecievingKidney("G",1000, "State")

                if global_vars.found==False:
                    if age<18:
                        PatientRecievingKidney("P",18, "State")
                        if global_vars.found==False:
                            PatientRecievingKidney("P",1000, "State")
                    if age>18:
                        PatientRecievingKidney("P",1000, "State")

                if global_vars.found==False:
                    global_vars.ORGAN_WASTE = global_vars.ORGAN_WASTE + 1
                    print('organ_waste')

            if hosp=="P":
                if age<18:
                    PatientRecievingKidney("P",18, "State")
                    if global_vars.found==False:
                        PatientRecievingKidney("P",1000, "State")
                if age>18:
                    PatientRecievingKidney("P",1000, "State")

                if global_vars.found==False:
                    if age<18:
                        PatientRecievingKidney("G",18, "State")
                        if global_vars.found==False:
                            PatientRecievingKidney("G",1000, "State")
                    if age>18:
                        PatientRecievingKidney("G",1000, "State")

                if global_vars.found==False:
                    global_vars.ORGAN_WASTE = global_vars.ORGAN_WASTE + 1
                    print('organ_waste')

        if global_vars.found == False:
            for i in range(global_vars.years):
                if global_vars.CLOCK_SIM in range((i*365*24),((i+1)*365*24)):
                    global_vars.UNALLOCATED_ORGANS_each_year[global_vars.repnumber,i]+=1

        if global_vars.found == True:
            if global_vars.CLOCK_SIM >= global_vars.warmupperiod*24*365:
                global_vars.DL[global_vars.x][0] = global_vars.CLOCK_SIM
                global_vars.DL[global_vars.x][1] = global_vars.Patient_id
                global_vars.DL[global_vars.x][2] = global_vars.CLOCK_SIM - global_vars.Patient_id
                global_vars.DL[global_vars.x][3] = global_vars.transportation_time
                rep=global_vars.repnumber
                for i in range(global_vars.years):
                    if global_vars.Patient_id in range((i * 365 * 24), ((i + 1) * 365 * 24)):
                        global_vars.alloc_15[rep][i] += 1
                        if global_vars.CLOCK_SIM in range((i * 365 * 24), ((i + 1) * 365 * 24)):
                            global_vars.alloc_for_prob[rep][i] += 1
                        if global_vars.CLOCK_SIM in range(global_vars.Patient_id,
                                                          global_vars.Patient_id + (1 * 365 * 24)):
                            global_vars.DL1[global_vars.x][0] = global_vars.Patient_id
                        if global_vars.CLOCK_SIM in range(global_vars.Patient_id,
                                                          global_vars.Patient_id + (2 * 365 * 24)):
                            global_vars.DL2[global_vars.x][0] = global_vars.Patient_id
                        if global_vars.CLOCK_SIM in range(global_vars.Patient_id,
                                                          global_vars.Patient_id + (5 * 365 * 24)):
                            global_vars.DL5[global_vars.x][0] = global_vars.Patient_id
                global_vars.x += 1
            global_vars.patients_alloc_each_year

            for i in range(global_vars.years):
                if (i*365*24)<global_vars.CLOCK_SIM <=((i+1)*365*24):
                    global_vars.patients_alloc_each_year[global_vars.repnumber,i]+=1
                    global_vars.transport_time[global_vars.repnumber,i]+=global_vars.transportation_time
                    global_vars.time_to_alloc[global_vars.repnumber,i]+=global_vars.CLOCK_SIM-global_vars.Patient_id
                    if global_vars.Patient_hostpital_type=='G':
                        global_vars.time_by_hosp_g[global_vars.repnumber,i]+=global_vars.CLOCK_SIM-global_vars.Patient_id
                        global_vars.patients_donated_hosp_g[global_vars.repnumber,i]+=1
                    if global_vars.Patient_hostpital_type=='P':
                        global_vars.time_by_hosp_p[global_vars.repnumber,i]+=global_vars.CLOCK_SIM-global_vars.Patient_id
                        global_vars.patients_donated_hosp_p[global_vars.repnumber,i]+=1
                    if global_vars.Patient_bloodgroup=='A':
                        global_vars.A_alloc_per_year[global_vars.repnumber,i]+=1
                        global_vars.time_by_bgA[global_vars.repnumber,i]+=global_vars.CLOCK_SIM-global_vars.Patient_id
                    elif global_vars.Patient_bloodgroup=='B':
                        global_vars.B_alloc_per_year[global_vars.repnumber,i]+=1
                        global_vars.time_by_bgB[global_vars.repnumber,i]+=global_vars.CLOCK_SIM-global_vars.Patient_id
                    elif global_vars.Patient_bloodgroup=='O':
                        global_vars.O_alloc_per_year[global_vars.repnumber,i]+=1
                        global_vars.time_by_bgO[global_vars.repnumber,i]+=global_vars.CLOCK_SIM-global_vars.Patient_id
                    else:
                        global_vars.AB_alloc_per_year[global_vars.repnumber,i]+=1
                        global_vars.time_by_bgAB[global_vars.repnumber,i]+=global_vars.CLOCK_SIM-global_vars.Patient_id

            for i in range(global_vars.warmupperiod,global_vars.years-5):
                if i*365*24< global_vars.Patient_id <=(i+1)*365*24:
                    # print(global_vars.Patient_id)
                    for j in range(5):
                        if global_vars.Patient_id+(0*365*24)<global_vars.CLOCK_SIM <=global_vars.Patient_id+(j+1)*365*24:
                            global_vars.ALLOCATED[global_vars.repnumber,(i-global_vars.warmupperiod),j]+=1
                            if global_vars.Patient_hostpital_type=='G':
                                global_vars.ALLOCATED_hosp_g[global_vars.repnumber,(i-global_vars.warmupperiod),j]+=1
                            else:
                                global_vars.ALLOCATED_hosp_p[global_vars.repnumber,(i-global_vars.warmupperiod),j]+=1
                            if global_vars.Patient_bloodgroup=='A':
                                global_vars.ALLOCATED_bg_A[global_vars.repnumber,(i-global_vars.warmupperiod),j]+=1
                            elif global_vars.Patient_bloodgroup=='B':
                                global_vars.ALLOCATED_bg_B[global_vars.repnumber,(i-global_vars.warmupperiod),j]+=1
                            elif global_vars.Patient_bloodgroup=='O':
                                global_vars.ALLOCATED_bg_O[global_vars.repnumber,(i-global_vars.warmupperiod),j]+=1
                            else:
                                global_vars.ALLOCATED_bg_AB[global_vars.repnumber,(i-global_vars.warmupperiod),j]+=1

            global_vars.x+=1

        for i in range(global_vars.years):
            if (i*365*24)<global_vars.CLOCK_SIM<= ((i+1)*365*24):
                global_vars.donor[global_vars.repnumber,i]+=1
                if bgroup == 'AB':
                    global_vars.Organ_BG_AB[global_vars.repnumber,i]+=1
                elif bgroup == 'A':
                    global_vars.Organ_BG_A[global_vars.repnumber,i]+=1
                elif bgroup == 'B':
                    global_vars.Organ_BG_B[global_vars.repnumber,i]+=1
                else:
                    global_vars.Organ_BG_O[global_vars.repnumber,i]+=1
                if hosp=='P':
                    global_vars.Organ_from_P_Hosp[global_vars.repnumber,i]+=1
                else:
                    global_vars.Organ_from_G_Hosp[global_vars.repnumber,i]+=1

        if Number_of_kidney_retrived_per_donor==1:
            g=2
            # print("donor donating 1 kidney")
        else:
            g+=1

    global_vars.NEXT_ORGAN_ARRIVAL = global_vars.CLOCK_SIM + fns.DonorInterArrivalTime()

    for i in range(global_vars.years):
        if (i * 365 * 24) < global_vars.CLOCK_SIM <= ((i + 1) * 365 * 24):
            global_vars.Donor[global_vars.repnumber, i] += 1
            if bgroup == 'AB':
                global_vars.Donor_BG_AB[global_vars.repnumber, i] += 1
            elif bgroup == 'A':
                global_vars.Donor_BG_A[global_vars.repnumber, i] += 1
            elif bgroup == 'B':
                global_vars.Donor_BG_B[global_vars.repnumber, i] += 1
            else:
                global_vars.Donor_BG_O[global_vars.repnumber, i] += 1
            if hosp == 'P':
                global_vars.Donor_from_P_Hosp[global_vars.repnumber, i] += 1
            else:
                global_vars.Donor_from_G_Hosp[global_vars.repnumber, i] += 1



def calc_recieving_city():
    x = random()
    type=""
    x = random()
    if x < 0.0244:
        recieving_city_index = 13
    elif x>0.0244 and x<0.0576:
        recieving_city_index = 2
    elif x>0.0576 and x<0.0934:
        recieving_city_index = 10
    elif x>0.0934 and x<0.1324:
        recieving_city_index = 4
    elif x>0.1324 and x<0.1917:
        recieving_city_index = 6
    elif x>0.1917 and x<0.2553:
        recieving_city_index = 0
    elif x>0.2553 and x<0.3309:
        recieving_city_index = 3
    elif x>0.3309 and x<0.4097:
        recieving_city_index = 5
    elif x>0.4097 and x<0.4938:
        recieving_city_index = 9
    elif x>0.4938 and x<0.5864:
        recieving_city_index = 7
    elif x>0.5864 and x<0.6795:
        recieving_city_index = 12
    elif x>0.6795 and x<0.7778:
        recieving_city_index = 1
    elif x>0.7778 and x<0.8768:
        recieving_city_index = 11
    else:
        recieving_city_index = 8

    y=random()
    if y<0.5:
        type='P'
    else: type='G'

    # if recieving_city_index==11:
    #     y=random()
    #     if y<0.8571:
    #         type='P'
    #     else:
    #         type='G'
    # elif recieving_city_index==7:
    #     y=random()
    #     if y<0.8:
    #         type='P'
    #     else:
    #         type='G'
    # elif recieving_city_index==6:
    #     type='G'
    # else:
    #     type='P'
    
    return recieving_city_index,type
    # Population fraction districtwise cumulative prob_city=[0.0376821430000000,0.0912818920000000,0.117504007000000,0.135341831000000,0.173325936000000,0.210503472000000,0.245639547000000,0.280125191000000,0.296331337000000,0.318860487000000,0.348613857000000,0.372456982000000,0.390057909000000,0.410314418000000,0.439041083000000,0.464930688000000,0.561594862000000,0.571367791000000,0.598045715000000,0.618631582000000,0.649807274000000,0.703596466000000,0.724869715000000,0.753331546000000,0.801585644000000,0.831310216000000,0.843970578000000,0.860843275000000,0.880326593000000,0.919384128000000,0.934502577000000,1]

def pronumkidney():
    x=random()
    if x<=0.777:
        h=2
    else:
        h=1
    return h

def calc_bgroup():
    x = random()
    bgroup = ""
    if(x<=0.069):
        bgroup='AB'
    elif(x>0.069 and x<=0.261):
        bgroup='A'
    elif(x>0.261 and x<=0.515):
        bgroup='B'
    else:
        bgroup='O'
    return  bgroup

def calc_age():
    x=random()
    val =  math.ceil(3.298*np.random.exponential(3.176*x))
    if(val<=1):
        age_return=1
    elif(val>=75):
        age_return=75
    else:
        age_return=val
    return age_return

def check_bg_compatibility(bgd, bgr):
    if bgd == "A":
        if bgr == "A":
            return True
        elif bgr == "AB":
            return True
    elif bgd == "B":
        if bgr == "B" :
            return True
        elif bgr == "AB":
            return True
    elif bgd == "AB":
        if bgr == "AB":
            return True
    elif bgd == "O":
        if bgr == "O":
            return True
        elif bgr == "A":
            return True
        elif bgr == "B":
            return True
        elif bgr == "AB":
            return True