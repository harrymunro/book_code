"""
This is a simple example of a car parking and driving using SimPy.

Car parks for 5 units of time and drives for 2 units of time.
"""

import simpy

def car(env):
    """
    Car parking and driving process using SimPy.
    """
    while True:
        print(f'Car parks at {env.now}')
        yield env.timeout(5) # Car is parked for 5 units of time
        print(f'Car drives at {env.now}')
        yield env.timeout(2) # Car drives for 2 units of time

env = simpy.Environment()

env.process(car(env))