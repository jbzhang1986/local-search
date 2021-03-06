#!/usr/bin/env python3
# Dan Engbert
# CMSC 471 - Spring 2017


# HOW TO RUN PROGRAM:
# run hill climbing algorithm with value3:
# python3 local_search.py --hill 3
#
# run simulated annealing algorithm with value1:
# python3 local_search.py --anneal 1


import sys
from schedule import Schedule
from copy import deepcopy
from math import exp
from random import choice
from random import randint
from random import random


# generates a random schedule and optimizes it with either the hill climbing
# algorithm or through simulated annealing (depending on command line args)
def main():
    # check command line args
    if len(sys.argv) != 3:
        print("Error: 2 program arguments are required")
        print("       e.g. --hill 3")
        print("       or   --anneal 1")
        return
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    try:
        arg2 = int(arg2)
    except:
        tmp = arg1
        arg1 = arg2
        arg2 = tmp
        try:
            arg2 = int(arg2)
        except:
            arg2 = int(0)
    num = arg2
    if not (num == 1 or num == 2 or num == 3):
        print("Error: valid integer argument required (1, 2, or 3)")
        return
    if not (arg1 == "--anneal" or arg1 == "--hill"):
        print("Error: invalid search type argument")
        print("       use --anneal or --hill")
        return
    hill = True
    if arg1 == "--anneal":
        hill = False

    # generate random parameters for generating a schedule
    numDays = randint(10, 50)
    numEmployees = randint(4, int(numDays * 0.7))
    print("Created schedule with " + str(numDays) + " days and " + str(numEmployees) + " employees.")

    s = Schedule(numEmployees, numDays)
    s.randomize()

    print("initial schedule:")
    print(s.schedule)
    if hill:
        hillClimb(s, num)
    else:
        simAnneal(s, num)
    print("optimized schedule:")
    print(s.schedule)                # print the new schedule


# perform hill climbing to optimize a schedule
# changes a schedule one shift at a time
# a state is changed by changing who works what shift on what day
# (a state is just one instance of a schedule)
# @param sched: schedule object
# @param heur: int (1, 2, or 3) refering to which heurstic to use
def hillClimb(sched, heur):
    print("\n---------Local Search (" + str(heur) + ")----------")
    cur = h(sched, heur)
    print("initial heuristic value: " + str(cur))

    while True:
        cur = h(sched, heur)         # current heuristic value
        val = cur                    # new heuristic value to potentially move to
        print("  cur value: " + str(cur))
        count = 0

        # find a change that increases the heuristic and move to that state
        while val <= cur and count <= 1000:
            count = count + 1

            # perform a random shift in the schedule and see if it improves it
            d = randint(0, sched.num_days-1)
            day = sched.schedule[d]  # note: changing this object will change the schedule class
            oldDay = deepcopy(day)   # deep copy so orginal state will be preserved

            shift = randint(1,3)
            if shift == 1:
                day.morning = choice(sched.workers)
            if shift == 2:
                day.evening = choice(sched.workers)
            if shift == 3:
                day.graveyard = choice(sched.workers)

            val = h(sched, heur)
            if val <= cur:
                # undo changes
                sched.schedule[d] = oldDay

        # alogrithm finishes when no better nearby state is found (after 1000 attempts)
        if count > 1000:
            break
    print("final huerstic value: " + str(cur) + "\n")


# perform simulated annealing to optimize a schedule
# also keeps track of the all time best schedule
# @param sched: schedule object
# @param heur: int (1, 2, or 3) refering to which heurstic to use
def simAnneal(sched, heur):
    print("\n---------Simulated Annealing (" + str(heur) + ")----------")
    best = deepcopy(sched)           # best schedule so far
    cur = h(sched, heur)
    old = cur
    print("initial heuristic value: " + str(cur))

    # temperatue starts at 1.0 and stops at 0.001
    t = 1.0
    k = 0.995
    while t > 0.001:
        old = cur
        cur = h(sched, heur)
        if cur != old:
            print("  cur value: " + str(cur))

        # perform a random shift in the schedule and consider moving there
        d = randint(0, sched.num_days-1)
        day = sched.schedule[d]      # note: changing this object will change the schedule class
        oldDay = deepcopy(day)       # deep copy so orginal state will be preserved

        shift = randint(1,3)
        if shift == 1:
            day.morning = choice(sched.workers)
        if shift == 2:
            day.evening = choice(sched.workers)
        if shift == 3:
            day.graveyard = choice(sched.workers)

        val = h(sched, heur)

        if val > cur:
            # accept the new (better) state
            best = deepcopy(sched)

        else:
            # maybe accept the worse state
            r = random()
            p = prob(cur, val, t)    # acceptance probability
            if not (r <= p):
                # undo changes
                sched.schedule[d] = oldDay
        t = k * t                    # decrease t
    print("final huerstic value: " + str(cur))
    print("all time best huerstic value: " + str(h(best, heur)) + "\n")
    sched = best


# acceptance probability function
# cur is the heuristic value of the current state
# other is the heuristic value of the state we're considering going to
# t is the current temperature
def prob(cur, other, t):
    res = exp(float((other - cur) / t))
    if res > 1.0:
        res = 1.0
    return res


# call the appropriate heuristic function and return the value
def h(sched, heur):
    if heur == 3:
        return sched.value3()
    if heur == 2:
        return sched.value2()
    return sched.value1() # else use heuristic 1


if __name__ == "__main__":
    main()
