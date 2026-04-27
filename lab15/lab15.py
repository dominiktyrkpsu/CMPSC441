"""
Lab 15: Monte Carlo RL on FrozenLake

Scaffold for implementing a Monte Carlo control agent on FrozenLake-v1.
Fill in the two TODOs in `choose_action` and `update_from_episode`, then run:

    python lab15/rl_agent.py

The script trains the agent and then runs measurement mode, which checks
whether the greedy policy reliably reaches the goal.
"""

from collections import defaultdict

import gymnasium as gym
import random
from tqdm import tqdm

# Hyperparameters
NUM_EPISODES = 5000
MAX_STEPS = 100
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 0.999

# Measurement mode
MEASURE_EPISODES = 100
SUCCESS_THRESHOLD = 0.90

# Q[(state, action)] -> estimated value
Q = defaultdict(float)
# How many returns have been averaged into each (state, action).
returns_count = defaultdict(int)


def choose_action(state, action_space, epsilon):



    if random.random() < epsilon:
        return action_space.sample()
    
    q_values = [Q[(state, a)] for a in range(action_space.n)]
    max_q = max(q_values)


    best_actions = [a for a in range(action_space.n) if Q[(state, a)] == max_q]
    return random.choice(best_actions)


def update_from_episode(episode):
    G = 0
    visited = set()


    for t in reversed(range(len(episode))):
        state, action, reward = episode[t]
        G = reward + GAMMA * G

        if (state, action) not in visited:
            visited.add((state, action))

            returns_count[(state, action)] += 1
            Q[(state, action)] += (G - Q[(state, action)]) / returns_count[(state, action)]


def run_episode(env, epsilon):
    """Roll out one episode using the current policy and return the trajectory."""
    state, _ = env.reset()
    episode = []
    for _ in range(MAX_STEPS):
        action = choose_action(state, env.action_space, epsilon)
        next_state, reward, terminated, truncated, _ = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if terminated or truncated:
            break
    return episode


def train(num_episodes=NUM_EPISODES):
    env = gym.make("FrozenLake-v1", is_slippery=False)
    epsilon = EPSILON_START
    for _ in tqdm(range(num_episodes), desc="training"):
        ep = run_episode(env, epsilon)
        update_from_episode(ep)
        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
    env.close()


def measure(num_episodes=MEASURE_EPISODES, threshold=SUCCESS_THRESHOLD):
    """Run the greedy policy and verify the task is solved."""
    env = gym.make("FrozenLake-v1", is_slippery=False)
    successes = 0
    for ep_idx in range(num_episodes):
        state, _ = env.reset(seed=ep_idx)
        total_reward = 0.0
        for _ in range(MAX_STEPS):
            action = choose_action(state, env.action_space, epsilon=0.0)
            state, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            if terminated or truncated:
                break
        if total_reward >= 1.0:
            successes += 1
    env.close()

    rate = successes / num_episodes
    solved = rate >= threshold
    print(f"\nSuccess rate: {rate:.2%}  (threshold {threshold:.0%})")
    print("Verdict:", "SOLVED" if solved else "NOT SOLVED")
    return solved


if __name__ == "__main__":
    train()
    measure()
