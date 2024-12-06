from typing import Dict, List, Literal
import json
import os
from pathlib import Path
import yaml
from zyk import LM
from craftaxlm import CraftaxACI, CraftaxClassicACI
from dev.testing.craftax.agent import SimpleReActLanguageAgent
from synth_sdk.tracing.upload import upload
from synth_sdk.tracing.abstractions import Dataset, TrainingQuestion, RewardSignal
import pytest
from asyncio import gather
from tqdm.asyncio import tqdm_asyncio

# Load config
config_path = Path("dev/testing/craftax/react.yaml")
with open(config_path, "r") as f:
    react_config = yaml.safe_load(f)


async def generate_single_episode(
    agent: SimpleReActLanguageAgent,
    mode: Literal["classic", "full"],
    seed: int,
    max_steps: int,
    output_dir: Path = None,
):
    """Generate a single episode"""
    # Initialize environment
    if mode == "classic":
        env = CraftaxClassicACI(seed=seed, verbose=False)
    else:
        env = CraftaxACI(seed=seed, verbose=False)

    # Store episode data
    episode_data = {"mode": mode, "seed": seed, "steps": [], "final_achievements": None}

    # Initial observation
    initial_obs = {"state": env.starting_obs}
    await agent.add_observations([initial_obs])
    episode_data["steps"].append(
        {
            "observation": initial_obs,
            "action": None,
            "reward": 0.0,
            "done": False,
            "achievements": [],
        }
    )

    # Run episode
    for step in range(max_steps):
        actions = await agent.get_actions()
        step_infos = []
        for action in actions:
            step_info = env._step(env.map_action_string_to_int(action))
            step_infos.append(step_info)
            episode_data["steps"].append(
                {
                    "observation": step_info,
                    "action": action,
                    "reward": step_info["reward"],
                    "done": step_info["done"],
                    "achievements": env.achievement_deltas[-1],
                }
            )
            if step_info["done"]:
                break

        await agent.add_observations(step_infos)
        if step_info["done"]:
            break

    # Store final achievements
    raw_achievements = env.terminate()
    episode_data["final_achievements"] = {
        k: bool(v) for k, v in raw_achievements.items()
    }
    return episode_data


async def generate_episodes(
    agent: SimpleReActLanguageAgent,
    mode: Literal["classic", "full"] = "classic",
    seeds: List[int] = [0],
    max_steps: int = 200,
    output_dir: Path = None,
):
    """Generate multiple episodes using the provided agent"""
    # Create tasks for all episodes
    tasks = [
        generate_single_episode(agent, mode, seed, max_steps, output_dir)
        for seed in seeds
    ]
    
    # Run episodes concurrently with progress bar
    all_episodes_data = await tqdm_asyncio.gather(*tasks, desc=f"Running {mode} episodes")

    # Process results
    total_achievements_list = []
    for episode_data in all_episodes_data:
        total_achievements = sum(1 for v in episode_data["final_achievements"].values() if v)
        total_achievements_list.append(total_achievements)
        print(f"Final achievements for seed {episode_data['seed']}: {episode_data['final_achievements']} (Total: {total_achievements})")

        # Save episode data if output directory provided
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"episode_{mode}_{episode_data['seed']}.json"
            with open(output_file, "w") as f:
                json.dump(episode_data["final_achievements"], f, indent=2)

    # Calculate and upload results
    avg_achievements = sum(total_achievements_list) / len(total_achievements_list)
    print(f"\nAverage achievements across {len(seeds)} episodes: {avg_achievements:.2f}")

    # Upload results with average reward
    results = await upload(
        dataset=Dataset(
            questions=[
                TrainingQuestion(
                    intent=" ",
                    criteria="Got as many achievements as possible across multiple episodes",
                    question_id="default",
                )
            ],
            reward_signals=[
                RewardSignal(
                    question_id="default",
                    system_id=agent.system_id,
                    reward=avg_achievements,
                    annotation=f"Average achievements across {len(seeds)} episodes: {avg_achievements:.2f}",
                )
            ],
        )
    )
    print("Results: ", results)
    print("Uploaded")
    assert_compute_inputs_not_empty(results)
    return all_episodes_data


def assert_compute_inputs_not_empty(results):
    """Assert that compute inputs in traces are not empty"""
    response, payload, traces, dataset = results
    found_compute_steps = False

    # Look for traces in the payload
    if isinstance(payload, dict) and "traces" in payload:
        for trace in payload["traces"]:
            if "partition" not in trace:
                continue

            for partition in trace["partition"]:
                if "events" not in partition:
                    continue

                for event in partition["events"]:
                    if "agent_compute_steps" in event:
                        found_compute_steps = True
                        for step in event["agent_compute_steps"]:
                            assert step[
                                "compute_input"
                            ], f"Empty compute_input in agent step: {step}"
                            assert (
                                not isinstance(step["compute_input"], list)
                                or len(step["compute_input"]) > 0
                            ), "Agent compute_input is an empty list"

                    if "environment_compute_steps" in event:
                        found_compute_steps = True
                        for step in event["environment_compute_steps"]:
                            assert step[
                                "compute_input"
                            ], f"Empty compute_input in environment step: {step}"
                            assert (
                                not isinstance(step["compute_input"], list)
                                or len(step["compute_input"]) > 0
                            ), "Environment compute_input is an empty list"

    assert found_compute_steps, "No compute steps found in traces"
    return True


@pytest.mark.asyncio
async def test_craftax_episode():
    """Test generating multiple Craftax episodes"""
    # Use config values
    max_steps = react_config["agent"]["max_agent_steps"]
    model_name = react_config["language_model"]["name"]
    
    # Initialize LLM
    lm = LM(
        model_name=model_name,
        formatting_model_name="gpt-4o-mini",
        temperature=react_config["language_model"]["temperature"],
        synth_logging=True,
    )

    # Setup test output directory
    output_dir = Path("tests/iteration/craftax/generate_data/records")
    
    # Create agent
    agent = SimpleReActLanguageAgent(
        lm=lm,
        mode=react_config["agent"]["mode"],
        config={
            "max_history": react_config["agent"]["max_history"],
            "max_agent_steps": react_config["agent"]["max_agent_steps"],
        },
    )

    # Run episodes with multiple seeds
    seeds = range(0,10)  # You can modify this list to run more or fewer episodes
    episodes_data = await generate_episodes(
        agent=agent, 
        mode="classic", 
        seeds=seeds,
        output_dir=output_dir, 
        max_steps=max_steps
    )
    
    # Add assertions to verify the episodes
    assert episodes_data is not None
    assert len(episodes_data) == len(seeds)
    for episode_data in episodes_data:
        assert "final_achievements" in episode_data
        assert isinstance(episode_data["final_achievements"], dict)
        assert len(episode_data["steps"]) > 0
        assert all(isinstance(step["reward"], (int, float)) for step in episode_data["steps"])
