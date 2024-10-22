import numpy as np
from standard import standardize,res, RE1_standard, RE2_standard
from standard import lower, all_lower
import math
from decimal import Decimal
RC_standard = res[50:71]

vcc = int(input('Voltage supply: '))
g = int(input('Total voltage gain: '))
b = int(input('DC Current gain: '))
vbe = float(input('Vbe on: '))
vin = 100*1e-3
vt = 26*1e-3

def recal4None(rc, re, r1, r2):
    rth = (r1*r2)/(r1+r2)
    vth = vcc*r2/(r1+r2)
    icq = b* ((vth-vbe)/(rth + (b+1)*re)) # actual Q point
    icc = vcc/(2*(rc+re)) # desired Q point
    vce = vcc - icq*(rc+re)
    gain = (icq/vt)*rc # actual voltage gain
    vout = vin*gain
    return (icq/icc)*100, gain, vce, vout 

def flat(nested_list):
    return [item for sublist in nested_list for item in sublist]

def recal(rc, re, r1, r2):
    rth = (r1*r2)/(r1+r2)
    vth = vcc*r2/(r1+r2)
    icq = b* ((vth-vbe)/(rth + (b+1)*re)) # actual Q point
    icc = vcc/(2*(rc+re)) # desired Q point
    vce = vcc - icq*(rc+re)
    gain = rc/((vt/icq) + re) # actual voltage gain
    vout = vin*gain
    return (icq/icc)*100, gain, vce, vout 
    """
    return:
        1: ratio between ic require and ic design
        2: actual gain of circuit
        3: 0 if signal generator range vce is not enough for output signal
    """

def recal4Both(rc, re1, re2, r1, r2):
    rth = (r1*r2)/(r1+r2)
    vth = vcc*r2/(r1+r2)
    icq = b* ((vth-vbe)/(rth + (b+1)*(re1 + re2))) # actual Q point
    icc = vcc/(2*(rc+re1 + re2)) # desired Q point
    vce = vcc - icq*(rc+re1 + re2)
    gain = rc/((vt/icq) + re1) # actual voltage gain
    vout = vin*gain
    return (icq/icc)*100, gain, vce, vout 

def combine_and_unpack_elements(RC, RE, R1, R2_below):
    """
    Combine elements from RC and RE arrays with corresponding elements in R1 and R2_below lists,
    and then unpack the combined array back into separate arrays and lists.

    Args:
    RC (numpy.ndarray): 1D array.
    RE (numpy.ndarray): 1D array.
    R1 (list of lists): Each element is a list.
    R2_below (list of lists): Each element is a list.

    Returns:
    tuple: RC, RE (numpy.ndarray), R1, R2_below (list of lists)
    """
    # Combine elements
    combined_list = []
    assert len(RC) == len(RE) == len(R1) == len(R2_below)

    for i in range(len(RC)):
        for j in range(len(R1[i])):
            combined_element = [RC[i], RE[i], R1[i][j], R2_below[i][j]]
            combined_list.append(combined_element)

    # Convert the combined list to a NumPy array
    combined_array = np.array(combined_list)

    # Unpack combined elements back into separate arrays and lists
    RC = combined_array[:, 0]
    RE = combined_array[:, 1]
    R1 = combined_array[:, 2].reshape(-1)  # Flatten R1
    R2_below = combined_array[:, 3].reshape(-1)  # Flatten R2_below

    return (RC), (RE), (R1), (R2_below)

def calc(RC): #calculate RC and RE
    # dimIC = dimRE = dimR2

    IC = (g*(vcc+2*vt))/(2*RC*(1+g))
    RE =  (vcc/(2*IC)) - RC
    RE, _ = standardize(RE, typ='approx') # Return an array that is an array of approximately of RE => dim(RE\approx) = dim(RE)
    R2 = (b*(vbe+IC*RE))/(10*IC)
    vb = vbe + IC*RE
    x = (vcc/vb) - 1
    R2_below = []
    R1 = []
    for i in range(np.shape(R2)[0]):
        newR2 = all_lower(R2[i])
        R2_below.append(list(newR2)) # Return an array that is an array of R2 approx  below R2 => dim R2approx != dim R2
        newR1,_ = standardize(x[i]*newR2, 'approx')
        R1.append(list(newR1))

    RC, RE, R1, R2_below = combine_and_unpack_elements(RC, RE, R1, R2_below)

    return RC,RE,R1,R2_below
    
def combine_and_unpack_elements_with_RE1(RC, RE1, RE2, R1, R2_below):
    """
    Combine elements from RC and RE2 arrays with corresponding elements in R1 and R2_below lists,
    including a constant RE1 value for each combination, and then unpack the combined array
    back into separate arrays and lists.

    Args:
    RC (numpy.ndarray): 1D array.
    RE2 (numpy.ndarray): 1D array.
    R1 (list of lists): Each element is a list.
    R2_below (list of lists): Each element is a list.
    RE1 (int or float): A constant value to include in the output.

    Returns:
    tuple: RC, RE1, RE2 (numpy.ndarray), R1, R2_below (list of lists)
    """
    # Combine elements
    combined_list = []
    assert len(RC) == len(RE2) == len(R1) == len(R2_below)

    for i in range(len(RC)):
        for j in range(len(R1[i])):
            combined_element = [RC[i], RE2[i], R1[i][j], R2_below[i][j]]
            combined_list.append(combined_element)

    # Convert the combined list to a NumPy array
    combined_array = np.array(combined_list)

    # Create RE1 array filled with the constant value
    RE1_array = np.full(combined_array.shape[0], RE1)

    # Unpack combined elements back into separate arrays and lists
    RC = combined_array[:, 0]
    RE2 = combined_array[:, 1]
    R1 = combined_array[:, 2].reshape(-1)  # Flatten R1
    R2_below = combined_array[:, 3].reshape(-1)  # Flatten R2_below

    return RC, RE1_array, RE2, R1, R2_below


# def both(RC, re1):
#     RC = np.array([rc for rc in RC if rc>g*re1])
#     if (np.shape(RC)[0]) == 0:
#         print('No value of RC')
#         return None
#     # print(RC)
#     ic = (g*vt)/(RC-g*re1)
#     # print(ic)
#     RE2 = (vcc/(2*ic)) - re1 - RC
#     # print(re2)
#     RE2,_ = standardize(RE2, typ='approx')
#     # print(RE2)
#     # print(np.shape(ic))
#     R2 = (b*(vbe+ic*(re1 + RE2)))/(10*ic)
#     # print(R2)
#     vb = vbe + ic*(re1 + RE2)
#     x = (vcc/vb) - 1
#     R2_below = []
#     R1 = []
#     for i in range(np.shape(R2)[0]):
#         # print(R2[i])
#         newR2 = all_lower(R2[i])
#         # print(newR2)
#         R2_below.append(list(newR2)) # Return an array that is an array of R2 approx  below R2 => dim R2approx != dim R2
#         newR1,_ = standardize(x[i]*newR2, 'approx')
#         R1.append(list(newR1))
#     RC, RE1_arr, RE2, R1, R2_below = combine_and_unpack_elements_with_RE1(RC, re1, RE2, R1, R2_below)
#     # print(RC)
#     return RC, RE1_arr, RE2, R1, R2_below

def both(RC, re2):
    ic = (vt - vcc/2)/((RC/g)+ RC+ re2)
    re1 = (vcc/2*ic) - RC - re2
    

def iterator(RE1):
    RC_arr = []
    RE1_arr = []
    RE2_arr = []
    R1_arr = []
    R2_arr =[]
    
    # Iteration for all valid value of R2
    for re1 in RE1:
        value = both(RC_standard, re1)
        if value != None:
            rc, re1_arr, re2, r1, r2 = value[0],value[1],value[2],value[3],value[4]
            # print(np.shape(rc))
            RC_arr.append(rc)
            RE1_arr.append(re1_arr)
            RE2_arr.append(re2)
            R1_arr.append(r1)
            R2_arr.append(r2)
        else:
            continue

    RC_arr = np.array(flat(RC_arr))
    # print(np.shape(RC_arr))
    RE1_arr = np.array(flat(RE1_arr))
    # print(np.shape(RE1_arr))
    RE2_arr = np.array(flat(RE2_arr))
    R1_arr = np.array(flat(R1_arr))
    R2_arr = np.array(flat(R2_arr))

    ratio, gain, vce, vout = recal4Both(RC_arr, RE1_arr, RE2_arr, R1_arr, R2_arr)
    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {}".format("RC", "RE1", "RE2", "R1", "R2", "Precision", "Gain", "Linear"))
    for i in range(0, np.shape(RC_arr)[0]):
        t='ok'
        if vce[i] < vout[i]:
            t = 'not'
        if np.abs(ratio[i] - 100) < 1:
            print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {}".format(RC_arr[i], RE1_arr[i], RE2_arr[i], R1_arr[i], R2_arr[i], round(ratio[i]), round(gain[i]), t))
            # print(RC[i], '\t', RE[i], '\t', R1[i], '\t', R2[i])
    # return RC_arr
    
        
# Method with RE bypass
def noRE(RC):
    IC = (g*vt)/RC
    RE = (vcc/(2*IC)) - RC
    RE, _ = standardize(RE, typ='approx') # Return an array that is an array of approximately of RE => dim(RE\approx) = dim(RE)
    R2 = (b*(vbe+IC*RE))/(10*IC)
    vb = vbe + IC*RE
    x = (vcc/vb) - 1
    R2_below = []
    R1 = []
    for i in range(np.shape(R2)[0]):
        newR2 = all_lower(R2[i])
        R2_below.append(list(newR2)) # Return an array that is an array of R2 approx  below R2 => dim R2approx != dim R2
        newR1,_ = standardize(x[i]*newR2, 'approx')
        R1.append(list(newR1))

    RC, RE, R1, R2_below = combine_and_unpack_elements(RC, RE, R1, R2_below)

    return RC,RE,R1,R2_below


# iterator(RE1_standard)






RC, RE, R1, R2 = calc(RC_standard)
ratio, gain, vce, vout = recal(RC, RE, R1, R2)


print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {}".format("RC", "RE", "R1", "R2", "Precision", "Gain", "Linear"))
for i in range(0, np.shape(RC)[0]):
    t='ok'
    if vce[i] < vout[i]:
        t = 'not'
    if np.abs(ratio[i] - 100) < 6:
        print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {}".format(RC[i], RE[i], R1[i], R2[i], round(ratio[i]), round(gain[i]), t))
        # print(RC[i], '\t', RE[i], '\t', R1[i], '\t', R2[i])

