# Dynamic Team Maker

### Definition:

#### Initial State - Individual member teams

#### Cost Function - It returns the cost of the particular team assignment for given constraints of staff time

#### Goal State - It returns the optimal solution with least amount of assignment cost

#### Algorithm Used for Searching - Local Search


### Approach for building the code:

1. As heap data structure provides an efficient implementation of priority queue, I used Priority Queue (heapq as implementation, built-in library in python) as data structure in constructing the base of the program.

2. The successor function is then building all the teams using the combination function (reffered from python documentation website, citation added in the code). 
    a. The combination function then makes all individual members as one team
    b. This individual member team is then combined with other teams with all the constraints considered by individual user.
    For example, 
        + A user suggests the size of his/her team member
        + A user suggests to whom they want to work with
        + A user might suggest to whom they don't want to work with
    c. Considering the staff time function, the teams will be merged having the lowest cost value

3. The staff time function considers all the following scenario to calculate the Assignment Cost - 
    a. requested_people - This will take all the requested people as team member by that individual member as a list
    b. dont_want_people - This will take all the requested exclusion list given by that individual member as a list
    c. Removing the 'zzz' | 'xxx' | '_' from the given list as they are unnecessary characters

    ##### Cost Consideration Constraints -

    + if a student requested for a specific team size and doesn't receivethe same team size, we add 2 minutes in the assignment cost
    + We add 5 minutes to grade each assignment (number of team)  
    + if a student is assigned a teammate on their exclusion list, we add 10 minutes in the assignment cost
    + if a student requested for a team member and if he/she  isn't in the same team. There is a 5% probability that they will share codes, and it takes 60 mins for the instructor to review the code (ie. .05 * 60)


### EXAMPLE :

#### INPUT - 

> python .\assign.py .\test1.txt

This file (test1.txt) has the given users and their requested team members and requested exclusion members

djcran djcran-vkvats-nthakurd sahmaini
sahmaini sahmaini _
sulagaop sulagaop-xxx-xxx _
fanjun fanjun-xxx nthakurd
nthakurd nthakurd djcran,fanjun
vkvats vkvats-sahmaini _


#### OUTPUT - 

// --[ Initial Solution has all teams as individual member  ]--

----- Latest solution:
djcran<br>
sahmaini<br>
sulagaop<br>
fanjun<br>
nthakurd<br>
vkvats<br>

Assignment cost: 26 

// --[ This will continue till the program gets optimal solution with least assignment amount, like this input value (test1.txt) gets the optimal solution as 4 teams and the assignment cost is 24]--

----- Latest solution:
sahmaini<br>
fanjun<br>
nthakurd<br>
sulagaop-djcran-vkvats<br>

Assignment cost: 24
