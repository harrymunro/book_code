import simpy
import itertools

# Function to simulate the factory process
def factory_process(env, machine, processing_time):
    start_time = env.now
    with machine.request() as request:
        yield request
        yield env.timeout(processing_time)
    total_time = env.now - start_time
    return total_time

# Parameters for the analysis
machine_capacities = [1, 2]
processing_times = [5, 10, 15]

# Function to run the factory process with given parameters
def factory_with_params(env, machine_capacity, processing_time):
    machine = simpy.Resource(env, capacity=machine_capacity)
    total_time = yield env.process(factory_process(env, machine, processing_time))
    return total_time

# Run full factorial analysis
results = []
for capacity, time in itertools.product(machine_capacities, processing_times):
    env = simpy.Environment()
    total_time = env.process(factory_with_params(env, capacity, time))
    env.run()
    results.append((capacity, time, total_time))

# Analysing the results
for capacity, time, total_time in results:
    print(f"Capacity: {capacity}, Processing Time: {time}, Total Time: {total_time}")