import numpy as np

# Define the states and actions
states = ['Hostel', 'AB', 'Canteen']
actions = ['Class', 'Eat']

# Rewards for states
rewards = {'Hostel': -1, 'AB': 3, 'Canteen': 1}

# Transition probabilities for each state-action pair
transition_probs = {
    'Hostel': {
        'Class': {'Hostel': 0.5, 'AB': 0.5},
        'Eat': {'Canteen': 1.0}
    },
    'AB': {
        'Class': {'AB': 0.7, 'Canteen': 0.3},
        'Eat': {'AB': 0.2, 'Canteen': 0.8}
    },
    'Canteen': {
        'Class': {'AB': 0.6, 'Hostel': 0.3, 'Canteen': 0.1},
        'Eat': {'Canteen': 1.0}
    }
}

# Initialize variables
gamma = 0  # Discount factor
theta = 1e-6  # Convergence threshold
V = np.zeros(len(states))  # Initial value function
policy = np.zeros(len(states), dtype=int)  # Initial policy

state_indices = {state: i for i, state in enumerate(states)}

def compute_value(state, action):
    next_states = transition_probs[state][action]
    return sum(prob * (rewards[next_state] + gamma * V[state_indices[next_state]])
               for next_state, prob in next_states.items())

# Value Iteration
iteration = 0
while True:
    delta = 0
    for state in states:
        v = V[state_indices[state]]
        V[state_indices[state]] = rewards[state] + gamma * max(compute_value(state, action) for action in actions)
        delta = max(delta, abs(v - V[state_indices[state]]))
    iteration += 1
    if delta < theta:
        break

# Extract policy
for state in states:
    state_index = state_indices[state]
    policy[state_index] = np.argmax([compute_value(state, action) for action in actions])

# Print results
print("Value Iteration Results:")
print("Values:")
for state, value in zip(states, V):
    print(f"Value for {state}: {value:.2f}")

print("\nPolicy:")
for i, state in enumerate(states):
    print(f"Best action for {state}: {actions[policy[i]]}")

