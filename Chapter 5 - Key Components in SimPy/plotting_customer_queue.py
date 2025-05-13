import simpy
import matplotlib.pyplot as plt
import numpy as np

# Define the customer process
def customer(env, name, counter, wait_times, queue_lengths):
    arrival_time = env.now
    with counter.request() as req:
        queue_lengths.append((env.now, len(counter.queue)))  # Track the queue length
        yield req
        wait_times.append(env.now - arrival_time)  # Track how long the customer waited
        yield env.timeout(5)  # Service time

# Generate customers over time
def customer_generator(env, counter, wait_times, queue_lengths):
    for i in range(10):
        env.process(customer(env, f'Customer {i}', counter, wait_times, queue_lengths))
        yield env.timeout(2)  # Customer arrival every 2 units of time

# Create the simulation environment
env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)  # Resource with a single server

# Lists to track wait times and queue lengths
wait_times = []
queue_lengths = []

# Start the customer generation process
env.process(customer_generator(env, counter, wait_times, queue_lengths))
env.run(until=20)

"""
Plot the number of customers in the queue over time.
"""

# Extract the time points and queue lengths for plotting
times, queue_sizes = zip(*queue_lengths)

# Plot the number of customers in the queue over time
plt.plot(times, queue_sizes, marker='o')
plt.title('Queue Size Over Time')
plt.xlabel('Time')
plt.ylabel('Number of Customers in Queue')
plt.grid(True)
plt.show()


"""
Plot the number of customers in the queue over time with a moving average.
"""
# Plot the number of customers in the queue over time
plt.plot(times, queue_sizes, marker='o', label='Queue Size')

# Calculate and plot the moving average
window_size = 3
moving_avg = np.convolve(queue_sizes, np.ones(window_size) / window_size, mode='valid')

# Adjust the x-axis times to align the moving average with the correct starting point
adjusted_times = times[window_size - 1:]  # Times for the moving average plot
plt.plot(adjusted_times, moving_avg, label='Moving Average', linestyle='--', color='red')

# Identify times and sizes where the queue is overloaded (queue size > 3)
overload_times = [t for t, q in zip(times, queue_sizes) if q > 3]
overload_sizes = [q for q in queue_sizes if q > 3]

# Highlight the overloaded queue points on the plot
plt.scatter(overload_times, overload_sizes, color='red', label='Overloaded Queue', zorder=5)

avg_queue_size = sum(queue_sizes) / len(queue_sizes)
plt.axhline(avg_queue_size, color='green', linestyle='--', label=f'Avg Queue Size: {avg_queue_size:.2f}')

# Add titles and labels
plt.title('Queue Size Over Time with Moving Average')
plt.xlabel('Time')
plt.ylabel('Number of Customers in Queue')

# Add legend and grid
plt.legend()
plt.grid(True)

# Ensure layout is tight and show the plot
plt.tight_layout()
plt.show()
