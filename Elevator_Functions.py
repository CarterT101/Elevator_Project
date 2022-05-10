import random

# this initial program starts the elevator program, it runs the lines of code to get the program start
# such as taking user input to see how many people should be created for this program
def start_elevator():

    # dictionary that contains the person and what values they have, IE what floor they are on and want to go to
    person_list = dict()
    # a dictionary that contains the original key and values inside to see who is on the elevator
    elevator_dict = dict()
    # a list to keep track of the keys to delete from original list so they don't get picked up again
    people_del_list = []
    # keeps track of indices to delete from elevator dictionary
    ele_del_list = []
    # keeps track of how many people have been dropped off
    floor_list = []
    people_amount = input("How many people should be in this building?: if not, press 'enter.'\n")
    # if the user enters a number, it will create a list and input the number into the create_people function
    # if not, if the user just hits 'enter' then it will default to 10 people created
    if people_amount:
        create_people(person_list, int(people_amount))
    else:
        create_people(person_list)
    # for each key value pair, print a string
    for i, k in person_list.items():
        print("Person: {}".format(i) + "\tCurrent Floor: {}".format(k[0]) + "\tDesired Floor: {}".format(k[1]))
    print("")
    # these lines of code find the max value the elevator needs to travel to.
    temp_max_floor = list([m, n] for m, n in person_list.values())
    max_floor = set(item for sublist in temp_max_floor for item in sublist)
    # grabs original length of person_list to keep track of when to stop the program
    origin_len = len(person_list)
    # input all parameters and start program
    going_up(person_list, elevator_dict, max_floor, people_del_list, ele_del_list, floor_list, origin_len)

# this function makes a list that takes in a number that it can't be (the floor the person is currently on), and
# end, which will always be six in this function as there are only 5 floors.
def random_floor(n, end, start=1):  # n being the number it can't be
    return [*range(start, n), *range(n+1, end)]  # makes a list within a range and a restriction

# creates a variable amount of people depending on user input, creates their values, and returns the dictionary
def create_people(person_list, n=10):
    # elevator that has 5 floors, so 1,6 makes that true
    for i in range(1, n+1):
        person_list[i] = [random.randrange(1, 6), 0]
        # add values to iterated person with random choice of floor and temp number, '0'
        go_to = random_floor(person_list[i][0], 6)
        # makes a new random list with restriction
        person_list[i][1] = random.choice(go_to)
        # replaces temp number with another random number that is NOT the floor they are currently on


def going_up(person_list, ele_list, maximum_floor, deleted_list, ele_del_list, floor_list, origin_len):
    print("Going up...\n")

    """
    for each floor they need to go to, from level 1 to max floor, check for each key-value pair
    in person_list and if the first value equals the current floor, and the floor they want to go to is above the
    current floor, and the elevator is NOT full, continue
    for the ele_list section: for each key-value pair it will check if the second index (floor they want to go to) is 
    equal to the current floor, if it is, append the index to the ele_del_list, and then for each index it saved in the
    ele_del_list, it will iterate through to delete the item from the ele_list, showing that they got off the elevator.
    if the length of the elevator list (ele_list) is greater than 5, meaning there are 5 people on the elevator, the 
    elevator is full and it will skip this iteration so no one else will get added to the elevator.
    """

    for current_floor in range(1, max(maximum_floor) + 1):
        if len(ele_list) > 0:
            for m, n in ele_list.items():
                if n[1] == current_floor:
                    print("Dropping off {} on floor {}\n".format(m, n[1]))
                    # adds key to new list to delete it from elevator list, signalling that they left the elevator
                    ele_del_list.append(m)
        for k, v in person_list.items():
            if v[0] == current_floor and v[1] > v[0] and len(ele_list) < 6:
                # adds key value pair to elevator dictionary to keep track of who is in elevator
                ele_list[k] = v
                # this adds the key to a new list to keep track of whom to delete from person_list, if
                # we deleted it in this loop it would mess with the iterations
                deleted_list.append(k)
                print("Picking up person {} from floor {}\n".format(k, v[0]))

    # for each item in del_list, clear the saved index from person_list, so we know who got picked up already
    # and then clear list for next use. same goes for ele_del_list
    for item in deleted_list:
        del person_list[item]
    deleted_list.clear()
    for item in ele_del_list:
        del ele_list[item]
        floor_list.append(item)
    ele_del_list.clear()
    # calls next function
    if len(floor_list) == origin_len:
        # if the length of the floor_list that keeps track of everyone that was
        # dropped off, is equal to the original length of the person_list, then that means everyone was dropped off
        # therefore the program should end
        print("Everyone got to where they are supposed to be!")
        return
    going_down(person_list, ele_list, maximum_floor, deleted_list, ele_del_list, floor_list, origin_len)


def going_down(person_list, ele_list, maximum_floor, deleted_list, ele_del_list, floor_list, origin_len):
    print("Going down...\n")
    # for range of maximum floor going down in intervals of 1, all the way to floor 1
    for current_floor in range(max(maximum_floor) + 1, 1, -1):
        # if there are people in the elevator, continue
        if len(ele_list) > 0:
            # for each key-value pair, if the second value (floor they want to go to) is equal to the current floor,
            # they need to get dropped off and takes needed steps to do so. same as last function
            for m, n in ele_list.items():
                if n[1] == current_floor:
                    ele_del_list.append(m)
                    print("Dropping off {} on floor {}\n".format(m, n[1]))
        for k, v in person_list.items():
            if v[0] == current_floor and v[1] < v[0] and len(ele_list) < 6:
                ele_list[k] = v
                deleted_list.append(k)
                print("Picking up person {} from floor {}\n".format(k, v[0]))
    for item in deleted_list:
        del person_list[item]
    deleted_list.clear()
    for item in ele_del_list:
        del ele_list[item]
        floor_list.append(item)
    ele_del_list.clear()
    if len(floor_list) == origin_len:
        print("Everyone got to where they are supposed to be!")
        return
    going_up(person_list, ele_list, maximum_floor, deleted_list, ele_del_list, floor_list, origin_len)


