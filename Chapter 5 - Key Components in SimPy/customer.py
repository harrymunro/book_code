import simpy

def customer(env, name, counter):
    print(f'{name} arrives at time {env.now}')
    with counter.request() as req: # Request the service counter
        yield req # Wait until the counter is available
        print(f'{name} is being served at time {env.now}')
        yield env.timeout(5) # Simulate service # time
        print(f'{name} leaves at time {env.now}')

env = simpy.Environment()
counter = simpy.Resource(env, capacity=1) # Only one service counter available

# Create 3 customers arriving at different times
env.process(customer(env, 'Customer 1', counter))
env.process(customer(env, 'Customer 2', counter))
env.process(customer(env, 'Customer 3', counter))

env.run(until=15) # Run the simulation for 15 time units