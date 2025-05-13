import simpy

def task(env, worker, task_id):
    with worker.request() as req:
        yield req # Wait until the worker is available
        print(f'Task {task_id} starts at {env.now}')
        yield env.timeout(2) # Task takes 2 time units
        print(f'Task {task_id} finishes at {env.now}')

env = simpy.Environment()
worker = simpy.Resource(env, capacity=1) # Only one worker available

# Start multiple tasks
for i in range(3):
    env.process(task(env, worker, i))

env.run(until=10)