#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from hello_ai.crew import HelloAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run_bot():
    """
    Start the Discord bot.
    """
    from hello_ai.discord_bot import start_bot
    start_bot()

def run_visuals():
    """
    Trigger ONLY the Visual Asset Manager task.
    Usage: crewai run run_visuals [topic]
    """
    import sys
    if len(sys.argv) < 2:
        print("Usage: crewai run run_visuals [topic]")
        return

    topic = sys.argv[1]
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }

    try:
        crew_instance = HelloAi().crew()
        # Find the visual asset task
        visual_task = None
        for task in crew_instance.tasks:
            if task.description.startswith("Review the script for"):
                visual_task = task
                break
        
        if visual_task:
            print(f"🚀 Triggering Visual Asset Manager for: {topic}")
            visual_task.execute()
        else:
            print("❌ Visual asset task not found in crew configuration.")

    except Exception as e:
        raise Exception(f"An error occurred while running visuals: {e}")

def run():
    """
    Run the crew (Starts the Discord bot).
    """
    run_bot()

def kickoff():
    """
    Kickoff the crew locally without Discord.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }

    try:
        HelloAi().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        HelloAi().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        HelloAi().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        HelloAi().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = HelloAi().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
