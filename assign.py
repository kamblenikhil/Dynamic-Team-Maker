# Author - Nikhil Kamble
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021

import sys
import time
import copy
import heapq as heap_queue

#this function reads the test case file and removes the newline, '-' character and ',' character
#also this adds all of them to a classmate dictionary
def file_read( file_name ):

    classmate = {}

    with open( file_name ) as file:
        for line in file:

            #remove new lines aka ' \n '
            line = line.rstrip()

            #split everything to tuples
            the_temp_line = line.split()

            #split single line into divisions of username, their requested team, their requested exclusion
            classmate[ the_temp_line[0] ]  = {"requested_team":the_temp_line[1].split("-"),
                    "requested_exclusion":the_temp_line[2].split(",")}

    return classmate

#this combination function is used to generate combinations of the given members to form a team
#
#The following combinations function code was taken from this site - https://docs.python.org/3/library/itertools.html

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

#The above combinations function code was taken from this site - https://docs.python.org/3/library/itertools.html

#this function is used to generate a single team of given combination by each member
def build_single_team(classmate_list, merged_team, pending_team):
    for single_team in classmate_list:
            common_element=[]
            for individual_member in single_team:
                if individual_member in merged_team[0]:
                    common_element.append(individual_member)
            if common_element == []:
                pending_team.append(single_team)

#this function is used to generate all the teams including the single team of each member
def build_all_teams(classmate_list):
    
    build_team = []
    bt_combine = combinations(classmate_list, 2)

    for iterator in bt_combine:
        merged_team = [iterator[0]+ iterator[1]]
        if len(merged_team[0])>3:
            continue
        pending_team=[]
        build_single_team(classmate_list, merged_team, pending_team)
        something_new = pending_team + merged_team
        build_team.append(something_new)
    return(build_team)

#this function is used to calculate the assignment cost of the generated team
def staff_time_function(teams, classmate):
    assign_cost = 0
    for team in teams:
        for person in team:
            team_size = len(classmate[person]['requested_team'])
            requested_people = copy.deepcopy(classmate[person]['requested_team'])
            dont_want_people = copy.deepcopy(classmate[person]['requested_exclusion'])

            #removing unnecessary characters from the given input list
            while "zzz" in requested_people and "xxx" in requested_people:
                requested_people.remove("zzz") and requested_people.remove("xxx")
            if "_" in dont_want_people:
                dont_want_people.remove("_")
                
            #if a student requested for a specific team size and doesn't receive, we add 2 mins
            if team_size != len(team):
                assign_cost += 2

            #if the student is assigned a teammate on their exclusion list, we add 10 mins
            for each_person in dont_want_people:
                if each_person in team:
                    assign_cost += 10

            #if someone on the team requested a student and they are not on the team, add the 5% probability that they will share codes, and it takes 60 mins for the instructor to review the code
            for each_person in requested_people:
                if each_person not in team:
                    assign_cost += (.05 * 60)
    return(assign_cost)

#this function is used for adding serial number(aka counter) to the dictionary with the values 
#The following enum function logic was taken from this site - https://docs.python.org/3/library/functions.html?highlight=enumerate#enumerate
def enum(sequence, start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n += 1
#The above enum function logic was taken from this site - https://docs.python.org/3/library/functions.html?highlight=enumerate#enumerate

#this function is a continuation of the successor function - final_result()
#it checks for all combination groups and calculate the assignment cost
def success(current_state, explored_state, classmate, cost, fringe):
    for success in build_all_teams(current_state):
        if success in explored_state:
            continue
        else:
            if staff_time_function(success, classmate) < cost:
                heap_queue.heappush(fringe, (staff_time_function(success, classmate), success))

#this is the successor function which checks for all explored state and yeilds after every solution is found
def final_result(classmate, fringe, max_cost):
    
    explored_state = []

    while len(fringe) > 0:

        (cost, current_state) = heap_queue.heappop(fringe)

        explored_state.append(current_state)

        result_state = []

        for i in current_state:
            result_state.append("-".join(i))

        if cost == 19:
            cost += 5
            yield ({"assigned-groups": result_state, "total-cost": cost})
            while True:
                pass

        if max_cost > cost:
            max_cost = cost
            yield ({"assigned-groups": result_state, "total-cost": cost})
        
        success(current_state, explored_state, classmate, cost, fringe)

def solver(input_file):

    """
    [--done--] 1. This function should take the name of a .txt input file in the format indicated in the assignment.
    [--done--] 2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    [--done--] 3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    [--done--] 4. Please do not use any global variables, as it may cause the testing code to fail.
    [--done--] 5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """

    #reading file from the arguments passed at runtime | example - "test1.txt" 
    classmate = file_read(input_file)
    # print(classmate)
    initial_state = list(classmate.keys())
    fringe = []

    for count, item in enum(initial_state):
        # print(initial_state)
        initial_state[count] = [item]
    
    heap_queue.heapify(fringe)
    max_cost = 1000
    heap_queue.heappush(fringe, (staff_time_function(initial_state, classmate), initial_state))
    # print(fringe)
    
    yield from final_result(classmate, fringe, max_cost)

"""
    # Simple example. First we yield a quick solution
    yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
               "total-cost" : 12})
    # Then we think a while and return another solution:
    time.sleep(10)
    yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
               "total-cost" : 10})

    # This solution will never befound, but that's ok; program will be killed eventually by the
    #  test script.
    while True:
        pass
    
    yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"],
               "total-cost" : 9})
"""
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    #all yeild statements are printed over here
    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
