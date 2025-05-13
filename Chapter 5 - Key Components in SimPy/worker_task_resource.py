import simpy

def task(env, worker):
    with worker.request() as req:
        yield req # Wait until the worker is available
        print(f'Task starts at {env.now}')
        yield env.timeout(3) # Task takes 3 time units
        print(f'Task finishes at {env.now}')

env = simpy.Environment()
worker = simpy.Resource(env, capacity=1) # Only one worker available
env.process(task(env, worker))
env.run(until=10)