import math
import numpy as np

def PatientInterArrivalTime():
    return math.ceil(np.random.exponential(1.382)*24)

def DonorInterArrivalTime():
    # return round(np.random.exponential(4.071)*24,5) #return round(24*np.random.exponential(1/52));
    return math.ceil(np.random.exponential(11.17)*24) #return round(24*np.random.exponential(1/52));
