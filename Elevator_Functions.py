import random
import time

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
    # input to see if the user wants to edit the values of the people
    people_input = input("If you want to edit their values, type 'yes'. \nIf not, hit 'enter'.\n")
    if people_input.lower() == 'yes':
        edit_people(person_list)
    # if user hits enter, continue with this elif
    elif people_input == "":
        print("Skipping input, creating random values")
        pass
    # if the user enters something wrong, it will skip letting them put input
    else:
        print("You did not enter correct value, skipping input")
        pass
    print("")
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

def edit_people(person_list):
    # keeps track of index, if user every enters a wrong value, it will restart,
    # or if they ever want to stop, they can just hit 'enter'
    i = 1
    while i < len(person_list)+1:
        line = input("Input the floor person {} is on and the floor they want to go to separated by ',': "
                     "\nValues have to be greater than 0, less than 6, and the values can not be the same."
                     "\nIf not, hit 'enter'.\n".format(i))
        if line == "":
            return person_list
        # splits the entered values into two different variables
        a, b = line.split(',')
        # makes sure the variables are within the building boundaries and not equal to each other
        if 6 > int(a) > 0 and int(b) != int(a) and 6 > int(b) > 0:
            person_list[i] = [int(a), int(b)]
            i += 1
        else:
            # if the user enters something wrong it will restart the while loop, making them input values again
            print("Did not enter correct value, restarting input.")
            i = 1
    return person_list


def going_up(person_list, ele_list, maximum_floor, deleted_list, ele_del_list, floor_list, origin_len):
    print("Going up to floor {}...\n".format(max(maximum_floor)))
    time.sleep(.7)
    """
    for each floor they need to go to, from level 1 to maximum_floor, check for each key-value pair
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
                    time.sleep(.7)
                    # adds key to new list to delete it from elevator list, signalling that they left the elevator
                    ele_del_list.append(m)
        for k, v in person_list.items():
            # if length of ele_list is 5, meaning the elevator is full, it should not continue with this loop
            if len(ele_list) == 5:
                break
            if v[0] == current_floor and v[1] > v[0] and len(ele_list) < 5:

                # adds key value pair to elevator dictionary to keep track of who is in elevator
                ele_list[k] = v
                # this adds the key to a new list to keep track of whom to delete from person_list.
                # if we deleted it in this loop it would mess with the iterations
                deleted_list.append(k)
                print("Picking up person {} from floor {}\n".format(k, v[0]))
                time.sleep(.7)

    # for each item in del_list, clear the saved index from person_list, so we know who got picked up already
    # and then clear list for next use. same goes for ele_del_list
    for item in deleted_list:
        del person_list[item]
    deleted_list.clear()
    for item in ele_del_list:
        del ele_list[item]
        floor_list.append(item)
    ele_del_list.clear()
    # if the length of the floor_list is equal to the original length of the person_list,
    # then that means everyone got dropped off and the program should end, so continue with this if statement
    if len(floor_list) == origin_len:
        # if the length of the floor_list that keeps track of everyone that was
        # dropped off, is equal to the original length of the person_list, then that means everyone was dropped off
        # therefore the program should end
        print("Everyone got to where they are supposed to be!")
        return
    # calls next function
    going_down(person_list, ele_list, maximum_floor, deleted_list, ele_del_list, floor_list, origin_len)


def going_down(person_list, ele_list, maximum_floor, deleted_list, ele_del_list, floor_list, origin_len):
    print("Going down to floor {}...\n".format(min(maximum_floor)))
    # for range of maximum floor going down in intervals of 1, all the way to floor 1
    for current_floor in range(max(maximum_floor) + 1, 0, -1):
        # if there are people in the elevator, continue
        if len(ele_list) > 0:
            # for each key-value pair, if the second value (floor they want to go to) is equal to the current floor,
            # they need to get dropped off and takes needed steps to do so. same as last function
            for m, n in ele_list.items():
                if n[1] == current_floor:
                    ele_del_list.append(m)
                    print("Dropping off {} on floor {}\n".format(m, n[1]))
                    time.sleep(.7)
        for k, v in person_list.items():
            # if length of ele_list is 5, meaning the elevator is full, it should not continue with this loop
            if len(ele_list) == 5:
                break
            # if first value (floor they are on) is equal to the current floor
            # and the second value (floor they want to go to) is less than the floor they are currently on,
            # and the elevator isn't at max capacity, pick them up and add it to the elevator list with their values
            if v[0] == current_floor and v[1] < v[0] and len(ele_list) < 5:
                ele_list[k] = v
                # add index to delete list to make sure it will delete it from the original person_list to keep track
                # of who got onto the elevator
                deleted_list.append(k)
                print("Picking up person {} from floor {}\n".format(k, v[0]))
                time.sleep(.7)
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


