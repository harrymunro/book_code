import simpy

env = simpy.Environment()

def process_example(env):
    print(f"Process starts at time {env.now}")
    yield env.timeout(5)
    print(f"Process resumes at time {env.now}")

def machine(env):
    print(f"Machine starts at {env.now}")
    yield env.timeout(3) # Machine works for 3 units of time
    print(f"Machine stops at {env.now}")

    resource = simpy.Resource(env, capacity=1)
    with resource.request() as req:
        yield req # Wait until the resource is available
        yield env.timeout(5) # Use the resource for 5 units of time

def process_with_explicit_request(env, resource):
    """
    Process that explicitly requests a resource and releases it manually after use.
    """
    # Request the resource
    req = resource.request()
    yield req # Wait until the resource is
    print(f"Resource acquired at {env.now}")

    # Simulate using the resource
    yield env.timeout(5)
    print(f"Process using resource at {env.now}")

    # Release the resource manually
    resource.release(req)
    print(f"Resource released at {env.now}")

# Simulation setup
env = simpy.Environment()
resource = simpy.Resource(env, capacity=1)
env.process(process_with_explicit_request(env, resource))
env.run(until=10)
