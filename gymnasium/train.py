import numpy as np
from blackjack_agent import BlackjackAgent
from matplotlib import pyplot as plt
from tqdm import tqdm

import gymnasium as gym


def train_agent(num_episodes=100_000):
    # Create environment and agent
    env = gym.make("Blackjack-v1", sab=False)
    env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=num_episodes)

    # Training hyperparameters
    learning_rate = 0.001  # How fast to learn (higher = faster but less stable)
    start_epsilon = 1.0  # Start with 100% random actions
    epsilon_decay = start_epsilon / (num_episodes / 2)  # Reduce exploration over time
    final_epsilon = 0.1  # Always keep some exploration

    agent = BlackjackAgent(
        env=env,
        learning_rate=learning_rate,
        initial_epsilon=start_epsilon,
        epsilon_decay=epsilon_decay,
        final_epsilon=final_epsilon,
    )

    for _ in tqdm(range(num_episodes)):
        # Start a new hand
        obs, info = env.reset()
        done = False

        # Play one complete hand
        while not done:
            # Agent chooses action (initially random, gradually more intelligent)
            action = agent.get_action(obs)

            # Take action and observe result
            next_obs, reward, terminated, truncated, info = env.step(action)

            # Learn from this experience
            agent.update(obs, action, reward, terminated, next_obs)

            # Move to next state
            done = terminated or truncated
            obs = next_obs

        # Reduce exploration rate (agent becomes less random over time)
        agent.decay_epsilon()

    return agent, env


def analyzing_training_results(env):
    def get_moving_avgs(arr, window, convolution_mode):
        """Compute moving average to smooth noisy data."""
        return (
            np.convolve(
                np.array(arr).flatten(),
                np.ones(window),
                mode=convolution_mode,
            )
            / window
        )

    # Smooth over a 500-episode window
    rolling_length = 500
    fig, axs = plt.subplots(ncols=3, figsize=(12, 5))

    # Episode rewards (win/loss performance)
    axs[0].set_title("Episode rewards")
    reward_moving_average = get_moving_avgs(env.return_queue, rolling_length, "valid")
    axs[0].plot(range(len(reward_moving_average)), reward_moving_average)
    axs[0].set_ylabel("Average Reward")
    axs[0].set_xlabel("Episode")

    # Episode lengths (how many actions per hand)
    axs[1].set_title("Episode lengths")
    length_moving_average = get_moving_avgs(env.length_queue, rolling_length, "valid")
    axs[1].plot(range(len(length_moving_average)), length_moving_average)
    axs[1].set_ylabel("Average Episode Length")
    axs[1].set_xlabel("Episode")

    # Training error (how much we're still learning)
    axs[2].set_title("Training Error")
    training_error_moving_average = get_moving_avgs(agent.training_error, rolling_length, "same")
    axs[2].plot(
        range(len(training_error_moving_average)),
        training_error_moving_average,
    )
    axs[2].set_ylabel("Temporal Difference Error")
    axs[2].set_xlabel("Step")

    plt.tight_layout()
    plt.show()


# Test the trained agent
def test_agent(agent, env, num_episodes=1000):
    """Test agent performance without learning or exploration."""
    total_rewards = []

    # Temporarily disable exploration for testing
    old_epsilon = agent.epsilon
    agent.epsilon = 0.0  # Pure exploitation

    for _ in tqdm(range(num_episodes)):
        obs, info = env.reset()
        episode_reward = 0
        done = False

        while not done:
            action = agent.get_action(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward
            done = terminated or truncated

        total_rewards.append(episode_reward)

    # Restore original epsilon
    agent.epsilon = old_epsilon

    win_rate = np.mean(np.array(total_rewards) > 0)
    average_reward = np.mean(total_rewards)

    print(f"Test Results over {num_episodes} episodes:")
    print(f"Win Rate: {win_rate:.1%}")
    print(f"Average Reward: {average_reward:.3f}")
    print(f"Standard Deviation: {np.std(total_rewards):.3f}")


# Train your agent
agent, env = train_agent(100_000)

# Analyze training results
analyzing_training_results(env)

# Test your agent
test_agent(agent, env, 1000)
