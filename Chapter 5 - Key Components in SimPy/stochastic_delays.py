import simpy
import numpy as np

def customer(env, name, counter):
    print(f'{name} arrives at time {env.now}')
    with counter.request() as req:
        yield req
        print(f'{name} is being served at time {env.now}')
        yield env.timeout(5) # Service time
        print(f'{name} leaves at time {env.now}')

def customer_generator(env, counter, mean_interarrival_time):
    for i in range(5):
        interarrival_time = np.random.exponential(mean_interarrival_time)
        yield env.timeout(interarrival_time) # Stochastic delay between arrivals
        env.process(customer(env, f'Customer {i + 1}', counter))

env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)  # Only one service counter available

# Generate customers with stochastic delays between arrivals
mean_interarrival_time = 3 # Mean of the exponential distribution
env.process(customer_generator(env, counter, mean_interarrival_time))
env.run(until=20)