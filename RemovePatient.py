def RemovePatient():
    import global_vars
    global_vars.WAITLIST.sort(key=lambda x: x.removal_time)
    removedPatient = global_vars.WAITLIST[0]
    global_vars.REMOVED_LIST.append(removedPatient)
    city_return = global_vars.WAITLIST[0].recievingcityindex
    city_index = 0

    for i in range(len(global_vars.CITYLIST)):
        if city_return == i:
            city_index = i
            break

    pid = global_vars.WAITLIST[0].id        # patient id
    global_vars.CITY_WAITLIST[city_index].sort(key=lambda x: x.removal_time)
    global_vars.CITY_WAITLIST[city_index].pop(0)
    global_vars.WAITLIST.pop(0)

    for i in range(global_vars.years):
        if (i*365*24)<global_vars.CLOCK_SIM <=((i+1)*365*24):
            global_vars.DEATH_each_year[global_vars.repnumber,i]+=1

    global_vars.WAITLIST.sort(key=lambda x: x.removal_time)
    global_vars.NEXT_PATIENT_REMOVAL = global_vars.WAITLIST[0].removal_time
    if global_vars.CLOCK_SIM >= global_vars.warmupperiod:
        global_vars.RL[global_vars.z][0]=pid
        global_vars.z+=1
