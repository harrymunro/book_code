import simpy

env = simpy.Environment()


"""
Priority resource
"""

# Create a priority resource with 1 server
priority_teller = simpy.PriorityResource(env, capacity=1)

# Customer with a priority level
def priority_customer(env, name, priority, teller):
    print(f'{name} arrives at the bank at {env.now}')
    with teller.request(priority=priority) as req:
        yield req
        print(f'{name} starts being served at {env.now}')
        yield env.timeout(5)
        print(f'{name} leaves the bank at {env.now}')

# Create a preemptive resource with 1 server
preemptive_teller = simpy.PreemptiveResource(env, capacity=1)

"""
Preemptive resource
"""

# Customer with a priority level
def preemptive_customer(env, name, priority, teller):
    print(f'{name} arrives at the bank at {env.now}')
    with teller.request(priority=priority, preempt=True) as req:
        try:
            yield req
            print(f'{name} starts being served at {env.now}')
            yield env.timeout(5)
            print(f'{name} leaves the bank at {env.now}')
        except simpy.Interrupt as interrupt:
            print(f'{name} was interrupted at {env.now} by {interrupt.cause}')

"""
Containers
"""
# Create a container with an initial level of 100 and a maximum capacity of 200
fuel_tank = simpy.Container(env, init=100, capacity=200)

# A process that consumes fuel
def consume_fuel(env, amount, fuel_tank):
    while True:
        yield fuel_tank.get(amount)
        print(f'Consumed {amount} fuel at {env.now}. Fuel level: {fuel_tank.level}')
        yield env.timeout(10)  # Wait 10 units of time before consuming more fuel
