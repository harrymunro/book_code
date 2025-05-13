import simpy

def event_scheduler(env):
    print(f'Starting at {env.now}')
    yield env.timeout(5) # Schedule an event 5 units from now
    print(f'Event occurred at {env.now}')

env = simpy.Environment()
env.process(event_scheduler(env))
env.run(until=10)