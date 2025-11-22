"""
Simulation Environment
======================

Defines a toy environment for agents.  Tasks are simple strings and
rewards are constant; this can be extended to implement more realistic
scenarios.
"""


def create_simple_tasks(n):
    """Create a list of ``n`` simple tasks with dummy data."""
    from evo_ai.agents.agent import Task
    tasks = []
    for i in range(n):
        tasks.append(Task(id=str(i), data=f"task_{i}"))
    return tasks


def run_tasks(agent, tasks):
    """Have an agent attempt each task and receive a reward."""
    from evo_ai.economy.rewards import default_reward_function, distribute_reward
    for task in tasks:
        result = agent.attempt_task(task)
        reward = default_reward_function(result, task)
        distribute_reward(agent, reward, task)
