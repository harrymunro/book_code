import simpy
import random

# Data collection for multiple runs
monte_carlo_results = []


# Factory process with randomised processing times
def factory_process(env, machine):
    start_time = env.now

    # Machine processing with random times
    with machine.request() as req:
        yield req
        yield env.timeout(random.uniform(5, 15))  # Random processing time between 5 and 15 units

    total_time = env.now - start_time
    return total_time


# Monte Carlo simulation runner
def run_monte_carlo(env, machine, num_runs):
    for _ in range(num_runs):
        total_time = yield env.process(factory_process(env, machine))
        monte_carlo_results.append(total_time)


# Set up the simulation environment
env = simpy.Environment()

# Create a machine resource
machine = simpy.Resource(env, capacity=1)

# Run Monte Carlo simulation with 100 runs
env.process(run_monte_carlo(env, machine, num_runs=100))
env.run()

# Output the distribution of results
print(f'Average factory processing time: {sum(monte_carlo_results) / len(monte_carlo_results):.2f}')