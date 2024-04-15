from random import *
from random import randint
import random
import xlrd
import math
import numpy
import Patient
import fns
import global_vars

def AddPatient():
    import global_vars
    age = calc_age()
    city_index = calc_city()
    city = global_vars.CITYLIST[city_index]
    bgroup=calc_bgroup()
    t_o_d = calc_dailysis()
    av_g = calc_avg()
    av_f = calc_av_fitsula()
    pig_f = calc_pigf()
    pr_a = calc_pra()
    score=calc_score(age,t_o_d,av_g,av_f,pig_f,pr_a)
    rtime = calc_rtime(t_o_d,score)
    hosp_index,hosp,patient_adding_in_hosp_city_index,type = calc_hosp(city_index)
    lasttime = 0
    # type=hosp_type()
    while rtime<0:
        rtime = calc_rtime(t_o_d,score)
    P = Patient.Patient(global_vars.CLOCK_SIM, age,city,city_index,patient_adding_in_hosp_city_index,bgroup,rtime + global_vars.CLOCK_SIM,score,hosp.name,type,pr_a,av_g,av_f,t_o_d,pig_f,lasttime,"Karnataka")
    # print(global_vars.CLOCK_SIM)
    global_vars.WAITLIST.append(P)
    global_vars.PATIENT_LIST.append(P)
    global_vars.WAITLIST.sort(reverse=True,key=lambda x: x.kap_score)

    global_vars.y=0
    # global_vars.i+=1
    global_vars.WAITLIST.sort(key=lambda x: x.removal_time)
    global_vars.NEXT_PATIENT_REMOVAL = global_vars.WAITLIST[0].removal_time
    global_vars.NEXT_PATIENT_ARRIVAL = global_vars.CLOCK_SIM + fns.PatientInterArrivalTime()
    global_vars.CITY_WAITLIST[patient_adding_in_hosp_city_index].append(P)

    for i in range(global_vars.years):
        if (i*365*24)<global_vars.CLOCK_SIM <=((i+1)*365*24):
            global_vars.patient_15[global_vars.repnumber,i]+=1
            global_vars.patient_each_year[global_vars.repnumber,i,:]+=1
            if bgroup=='A':
                global_vars.A_each_year[global_vars.repnumber,i]+=1
                global_vars.patient_A_each_year[global_vars.repnumber,i,:]+=1
            elif bgroup=='B':
                global_vars.B_each_year[global_vars.repnumber,i]+=1
                global_vars.patient_B_each_year[global_vars.repnumber,i,:]+=1
            elif bgroup=='O':
                global_vars.O_each_year[global_vars.repnumber,i]+=1
                global_vars.patient_O_each_year[global_vars.repnumber,i,:]+=1
            else:
                global_vars.AB_each_year[global_vars.repnumber,i]+=1
                global_vars.patient_AB_each_year[global_vars.repnumber,i,:]+=1
            if type=='G':
                global_vars.hosp_g_each_year[global_vars.repnumber,i]+=1
                global_vars.patient_G_hosp_each_year[global_vars.repnumber,i,:]+=1
            elif type=='P':
                global_vars.hosp_p_each_year[global_vars.repnumber,i]+=1
                global_vars.patient_P_hosp_each_year[global_vars.repnumber,i,:]+=1

            if (i*365*24)<global_vars.CLOCK_SIM <=((i+1)*365*24):
                global_vars.WAITLISTEDPATIENT_each_year[global_vars.repnumber,i]=0
                global_vars.WAITLISTEDPATIENT_BG_A_each_year[global_vars.repnumber,i]=0
                global_vars.WAITLISTEDPATIENT_BG_B_each_year[global_vars.repnumber,i]=0
                global_vars.WAITLISTEDPATIENT_BG_O_each_year[global_vars.repnumber,i]=0
                global_vars.WAITLISTEDPATIENT_BG_AB_each_year[global_vars.repnumber,i]=0
                global_vars.WAITLISTEDPATIENT_G_HOS_each_year[global_vars.repnumber,i]=0
                global_vars.WAITLISTEDPATIENT_P_HOS_each_year[global_vars.repnumber,i]=0

                for j in range(len(global_vars.WAITLIST)):
                    global_vars.WAITLISTEDPATIENT_each_year[global_vars.repnumber,i]+=1
                    if global_vars.WAITLIST[j].bloodgroup=='A':
                        global_vars.WAITLISTEDPATIENT_BG_A_each_year[global_vars.repnumber,i]+=1
                    elif global_vars.WAITLIST[j].bloodgroup=='B':
                        global_vars.WAITLISTEDPATIENT_BG_B_each_year[global_vars.repnumber,i]+=1
                    elif global_vars.WAITLIST[j].bloodgroup=='O':
                        global_vars.WAITLISTEDPATIENT_BG_O_each_year[global_vars.repnumber,i]+=1
                    else:
                        global_vars.WAITLISTEDPATIENT_BG_AB_each_year[global_vars.repnumber,i]+=1

                    if global_vars.WAITLIST[j].hospital_type=='G':
                        global_vars.WAITLISTEDPATIENT_G_HOS_each_year[global_vars.repnumber,i]+=1
                    elif global_vars.WAITLIST[j].hospital_type=='P':
                        global_vars.WAITLISTEDPATIENT_P_HOS_each_year[global_vars.repnumber,i]+=1

    if global_vars.CLOCK_SIM>=global_vars.warmupperiod*365*24:
        global_vars.WL[global_vars.i][0] = global_vars.CLOCK_SIM
        global_vars.WL[global_vars.i][1] = age
        global_vars.WL[global_vars.i][2] = patient_adding_in_hosp_city_index
        if bgroup == "O":
            global_vars.WL[global_vars.i][3] = 0
        elif bgroup == "A":
            global_vars.WL[global_vars.i][3] = 1
        elif bgroup == "B":
            global_vars.WL[global_vars.i][3] = 2
        else:
            global_vars.WL[global_vars.i][3] = 3

        global_vars.WL[global_vars.i][4] = rtime
        global_vars.WL[global_vars.i][5] = score

        if type == "G":
            global_vars.WL[global_vars.i][6] = 0
        else:
            global_vars.WL[global_vars.i][6] = 1

        global_vars.WL[global_vars.i][7] = pr_a
        if pr_a in range(1, 21):
            global_vars.WL[global_vars.i][24] = 1
        elif pr_a in range(21, 80):
            global_vars.WL[global_vars.i][24] = 2
        elif pr_a in range(80, 101):
            global_vars.WL[global_vars.i][24] = 3
        else:
            global_vars.WL[global_vars.i][24] = 4

        if av_g < 0.03125:
            global_vars.WL[global_vars.i][8] = 1
        else:
            global_vars.WL[global_vars.i][8] = 0

        if av_f < 0.052:
            global_vars.WL[global_vars.i][9] = 1
        else:
            global_vars.WL[global_vars.i][9] = 0

        global_vars.WL[global_vars.i][10] = t_o_d
        if pig_f < 0.0201:
            global_vars.WL[global_vars.i][11] = 1
        else:
            global_vars.WL[global_vars.i][11] = 0

        global_vars.WLhosp[global_vars.i][0] = hosp.name
        global_vars.WL[global_vars.i][18] = hosp_index

        global_vars.WAITLIST.sort(reverse=True, key=lambda x: x.kap_score)
        k = 0
        while global_vars.WAITLIST[k].id != global_vars.CLOCK_SIM:
            global_vars.y += 1
            k += 1
        global_vars.WL[global_vars.i][12] = global_vars.y + 1
        global_vars.WL[global_vars.i][13] = global_vars.y

        global_vars.WL[global_vars.i][14] = 0
        global_vars.WL[global_vars.i][15] = 0
        global_vars.WL[global_vars.i][16] = 0
        global_vars.WL[global_vars.i][17] = 0

        if global_vars.y == 0:
            global_vars.WL[global_vars.i][14] = 0
            global_vars.WL[global_vars.i][15] = 0
            global_vars.WL[global_vars.i][16] = 0
            global_vars.WL[global_vars.i][17] = 0
        else:
            for i in range(global_vars.y):
                if global_vars.WAITLIST[i].bloodgroup == 'A':
                    global_vars.WL[global_vars.i][14] += 1
                elif global_vars.WAITLIST[i].bloodgroup == 'B':
                    global_vars.WL[global_vars.i][15] += 1
                elif global_vars.WAITLIST[i].bloodgroup == 'O':
                    global_vars.WL[global_vars.i][16] += 1
                else:
                    global_vars.WL[global_vars.i][17] += 1

        global_vars.WL[global_vars.i][19] = len(global_vars.WAITLIST)
        for i in range(len(global_vars.WAITLIST)):
            if global_vars.WAITLIST[i].bloodgroup == 'A':
                global_vars.WL[global_vars.i][20] += 1
            elif global_vars.WAITLIST[i].bloodgroup == 'B':
                global_vars.WL[global_vars.i][21] += 1
            elif global_vars.WAITLIST[i].bloodgroup == 'O':
                global_vars.WL[global_vars.i][22] += 1
            else:
                global_vars.WL[global_vars.i][23] += 1

        global_vars.y=0
        global_vars.i+=1

def calc_dailysis():
    dailysis_time=numpy.random.exponential(260.3)
    dailysis_months = math.ceil((dailysis_time/30))
    return dailysis_months

def calc_avg():
    avg = random.uniform(0,1)
    return avg

def calc_av_fitsula():
    avf = random.uniform(0, 1)
    return avf

def calc_pigf():
    pigf = random.uniform(0, 1)
    return pigf

def calc_pra():
    y = random.uniform(0,1)
    if y<= 0.056:
        pra = randint(1, 20)
    elif y<=0.192:
        pra=randint(21,79)
    elif y<=0.35:
        pra= randint(80,100)
    else:
        pra=0
    return pra
    

#function score=calc_score(age)
def calc_score(age,t_o_d,av_g,av_f,pig_f,pr_a):    #why taking age as parameter

    value=0
    value=value+t_o_d                         #dialyis points added

    if age<6:
        value=value+3
    elif age>=6 and age<12:
        value=value+2
    elif age>=12 and age<18:
        value=value+1                               #age points added

    if av_f<0.052:
        value=value+2         # points for with failed all AV fistual sites added

    if av_g<0.03125:
        value=value+4         #points for with failed av graft after all failed avf sites  added

    if pig_f<0.0201:
        value=value+3        # points for prev immonological graft fail added

#----------------------------------------------pra points calculatino below

    # y = random.uniform(0,1)
    # if y<=0.65:
    #     pra=rand(1)
    # elif y<=0.706:
    #     pra=(20-1)*random()+1
    # elif y<=0.842:
    #     pra=(79-21)*random()+21
    # else:
    #     pra=(100-80)*random()+80
    #
    # if pra>20:
    #     val= math.ceil((pra-20)/10)
    #     value=value+0.5*val
    #
    # score=value

    pra_point=0
    if (pr_a == 0):
        pra_point = 0
    if (pr_a >=1 and pr_a<= 20):
        pra_point = 0
    elif (pr_a>=21 and pr_a<=30):
        pra_point = 0.5
    elif (pr_a>=30 and pr_a<=40):
        pra_point = 1
    elif (pr_a>=41 and pr_a<=50):
        pra_point = 1.5
    elif (pr_a>=51 and pr_a<=60):
        pra_point = 2
    elif (pr_a>=61 and pr_a<=70):
        pra_point = 2.5
    elif (pr_a>=71 and pr_a<=80):
        pra_point = 3
    elif (pr_a>=81 and pr_a<=90):
        pra_point = 3.5
    elif (pr_a>=91 and pr_a<=100):
        pra_point = 4

    value = value + pra_point
    score = value
    return score

#-------------------------------------------------------




# function age_return = calc_age()
#
#     val= math.ceil(normrnd(43,19.66))
#     if(val<=1)
#         age_return=1;
#     elseif(val>=75)
#         age_return=75;
#     else
#         age_return=val;

def calc_age():

    val =  math.ceil(numpy.random.normal(49.74, 7.423))
    if (val<=1):
        age_return = 1
    elif (val >=75):
        age_return = 75
    else:
        age_return = val
    return age_return



# function bgroup = calc_bgroup()
#     x = random()
#     if x<=0.054:
#         bgroup='C'
#     elif x>0.054 and x<=0.226:
#         bgroup='A'
#     elif x>0.226 and x<=0.548:
#         bgroup='B'
#     else:
#         bgroup='O'

def calc_bgroup():
    x = random.uniform(0,1)
    if (x <=0.0795):
        bgroup = "AB"
        global_vars.BGP_AB+=1
    elif  x > 0.0795 and x <= 0.303:
        bgroup = 'B'
        global_vars.BGP_B+=1
    elif x > 0.303 and x <= 0.54166:
        bgroup = 'A'
        global_vars.BGP_A+=1
    else:
        bgroup = 'O'
        global_vars.BGP_O+=1
    return bgroup


def calc_city():
    x = random.uniform(0, 1)
    if x < 0.0137:
        city_index = 13
    elif x>0.0137 and x<0.0319:
        city_index = 4
    elif x>0.0319 and x<0.0548:
        city_index = 2
    elif x>0.0548 and x<0.0959:
        city_index = 3
    elif x>0.0959 and x<0.146:
        city_index = 9
    elif x>0.146 and x<0.201:
        city_index = 10
    elif x>0.201 and x<0.265:
        city_index = 6
    elif x>0.265 and x<0.3287:
        city_index = 7
    elif x>0.3287 and x<0.42:
        city_index = 8
    elif x>0.42 and x<0.5114:
        city_index = 12
    elif x>0.5114 and x<0.6073:
        city_index = 1
    elif x>0.6073 and x<0.7077:
        city_index = 5
    elif x>0.7077 and x<0.8356:
        city_index = 0
    else:
        city_index = 11

    return city_index

# function rtme_return = calc_rtime()
# def calc_rtime():
#     x=betarnd(1.1939,2.4097)*3650;
#     rtime_return=ceil(x); % Here it is in days.    #?????
# end

from scipy.stats import beta
def kap_percentile(kap_score):
    kap_dist=beta(0.89, 33.99)
    score=(kap_score-1)/371.65
    return kap_dist.cdf(score) #percentile of score





def calc_rtime(t_o_d,kap_score):

    y = t_o_d * 24 * 30
    x = beta(4.38,3.51)   #removal time mean = 40.31, SD = 26.69 in months, ALSO In paper, BETA DISTN GIVEN?? but orgianl lakshmi doc says nothing about beta distn
    kap_score_percentile=kap_percentile(kap_score)
    mn=3+x.ppf(kap_score_percentile)*64
    a=mn-0.33*mn
    b=mn+0.33*mn
    m=mn
    alpha=2*(b+4*m-5*a)/(3*(b-a))*(1+4*(m-a)*(b-m)/((b-a)**2))
    betaa= 2*(5*b-4*m-a)/(3*(b-a))*(1+4*(m-a)*(b-m)/((b-a)**2))
    z=a+numpy.random.beta(alpha,betaa)*(b-a)

    return (math.ceil(z * 24*30)) #removal time now in hours because arrival time taken in hours

def calc_hosp(city_index):
    import global_vars
    x=random.uniform(0,1)
    rc=city_index
    L = len(global_vars.HOSPITAL_LIST[city_index])
    if L == 0:
        if city_index == 0:
            rc = 11
            L = len(global_vars.HOSPITAL_LIST[11])
        elif city_index == 2:
            rc = 6
            L = len(global_vars.HOSPITAL_LIST[6])
        elif city_index == 3:
            rc = 7
            L = len(global_vars.HOSPITAL_LIST[7])
        elif city_index == 4:
            rc = 7
            L = len(global_vars.HOSPITAL_LIST[7])
        elif city_index == 9:
            rc = 12
            L = len(global_vars.HOSPITAL_LIST[12])
        elif city_index == 13:
            rc = 7
            L = len(global_vars.HOSPITAL_LIST[7])
    r = randrange(0, L)
    # if rc==1:
    if city_index==11:
        y=random.uniform(0,1)
        if y<0.8571:
            type='P'
        else:
            type='G'
    elif city_index==7:
        y=random.uniform(0,1)
        if y<0.8:
            type='P'
        else:
            type='G'
    elif city_index==6:
        type='G'
    else:
        type='P'

    # y=random.uniform(0,1)    
    # if y<0.5:
    #     type = "G"
    # else:
    #     type = "P"
    return r,global_vars.HOSPITAL_LIST[rc][r],rc,type

