import simpy
import matplotlib.pyplot as plt


# Define the customer process
def customer(env, name, counter, wait_times, queue_lengths, active_servers):
    arrival_time = env.now
    print(f'{name} arrives at time {env.now}')  # Traceability: arrival time

    with counter.request() as req:
        queue_lengths.append((env.now, len(counter.queue)))  # Track queue length
        active_servers.append((env.now, counter.count))  # Track active servers
        yield req  # Wait for resource to become available

        wait_times.append(env.now - arrival_time)  # Track wait time
        print(f'{name} is being served at time {env.now}')  # Traceability: start of service

        yield env.timeout(5)  # Simulate service time
        print(f'{name} leaves at time {env.now}')  # Traceability: end of service


# Generate customers over time
def customer_generator(env, counter, wait_times, queue_lengths, active_servers):
    for i in range(15):  # Simulate more customers
        env.process(customer(env, f'Customer {i}', counter, wait_times, queue_lengths, active_servers))
        yield env.timeout(2)  # Customer arrival every 2 units of time


# Create the simulation environment
env = simpy.Environment()

# Define a resource with a capacity of 3 (e.g., 3 service desks)
counter = simpy.Resource(env, capacity=2)

# Lists to track wait times, queue lengths, and active servers
wait_times = []
queue_lengths = []
active_servers = []

# Start the customer generation process
env.process(customer_generator(env, counter, wait_times, queue_lengths, active_servers))
env.run(until=30)

# Extract the time points and queue lengths for plotting
times, queue_sizes = zip(*queue_lengths)
times_servers, server_counts = zip(*active_servers)

# Plot the number of customers in the queue over time
plt.plot(times, queue_sizes, marker='o', label='Queue Size')

# Plot the number of active servers (resource utilisation) over time
plt.plot(times_servers, server_counts, marker='s', linestyle='--', color='red', label='Active Servers')

# Add titles, labels, legend, and grid
plt.title('Queue Size and Resource Utilisation Over Time')
plt.xlabel('Time')
plt.ylabel('Count')
plt.legend()
plt.grid(True)

# Ensure the layout is tight and show the plot
plt.tight_layout()
plt.show()