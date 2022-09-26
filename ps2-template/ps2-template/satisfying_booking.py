import time
"""
Sort the requests
Keep a sorted list of ending timings
Keep a sorted list of start timings

"""
def combine_schedules(B_1, B_2):
    if len(B_1) == 0:
        return B_2
    elif len(B_2) == 0:
        return B_1
    
    (k_1, s_1, t_1) = B_1[-1]
    (k_2, s_2, t_2) = B_2[-1]


    if (s_2 >= s_1):
        b_i = B_2.pop()
    else:
        b_i = B_1.pop()

    (k_i, s_i, t_i) = b_i

    B = combine_schedules(B_1, B_2)
    b_j = B.pop()
    (k_j, s_j, t_j) = b_j

    # adjacent schedule
    if (t_j == s_i):
        # print("adjacent detected", b_j, b_i)
        if (k_i == k_j):
            B.append((k_i, s_i, t_j))
        else:
            B.append(b_j)
            B.append(b_i)
    elif (t_j < s_i):
    # disjoint schedule
        B.append(b_j)
        B.append(b_i)
    else:
    # intersecting schedule
        b_x = None
        b_y = None
        b_z = None
        # if j starts earlier than i
        if (s_j < s_i):
            b_x = (k_j, s_j, s_i)
            # if j ends later than i
            if (t_j > t_i):
                b_y = (k_i + k_j, s_i, t_i)
                b_z = (k_j, t_i, t_j)
            # if j ends together with i
            elif(t_j == t_i):
                b_y = (k_i + k_j, s_i, t_i)
            # if j ends earlier than i
            else:
                b_y = (k_i + k_j, s_i, t_j)
                b_z = (k_i, t_j, t_i)
        # if j starts together with i
        else:
            # if j ends later than i
            if (t_j > t_i):
                b_x = (k_i + k_j, s_i, t_i)
                b_y = (k_j, t_i, t_j)
            # if j ends together with i
            elif(t_j == t_i):
                b_x = (k_i + k_j, s_i, t_i)
            # if j ends earlier than i
            else:
                b_x = (k_i + k_j, s_i, t_j)
                b_y = (k_i, t_j, t_i)

        if b_x != None:
            # check if previous booking is adjacent and have same no. of rooms
            if (len(B) != 0): 
                b_prev = B.pop()
                (k_prev, s_prev, t_prev) = b_prev
                (k_x, s_x, t_x) = b_x

                if k_prev == k_x and t_prev == s_x:
                    B.append((k_prev, s_prev, t_x))
                else:
                    B.append(b_prev)
                    B.append(b_x)
            else:
                B.append(b_x)

        if b_y != None: B.append(b_y)
        if b_z != None:B.append(b_z)

    return B

def sorted_request_to_booking(R, level=0):
    if len(R) == 0:
        return []
    elif len(R) == 1:
        (s,t) = R[-1]
        return [(1, s, t)]

    R_1 = R[:len(R)//2]
    R_2 = R[len(R)//2:]
    B_1 = sorted_request_to_booking(R_1, level+1)
    B_2 = sorted_request_to_booking(R_2, level+1)

    B = combine_schedules(B_1, B_2)
    return B


def satisfying_booking(R):
    '''
    Input:  R | Tuple of |R| talk request tuples (s, t)
    Output: B | Tuple of room booking triples (k, s, t)
              | that is the booking schedule that satisfies R
    '''
    requests_list = list(R)
    requests_list.sort(key=lambda x: x[0])

    bookings_list = sorted_request_to_booking(requests_list)

    return tuple(bookings_list)
