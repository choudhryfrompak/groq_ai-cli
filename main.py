import os
import sys

from prompts import generate_prompt
from profile import get_or_create_enhanced_user_profile
from api import query_groq
from utils import (
    get_environment_info,
    get_command_history,
    get_current_directory_contents,
)
from ai_assist import ai_assist


# Generate Linux command from AI
def generate_command(user_input, user_profile):
    context = {
        "user_profile": user_profile,
        "env_info": get_environment_info(),
        "command_history": get_command_history(),
        "directory_contents": get_current_directory_contents(),

        "task": f"""
Convert this request into ONE Linux command.

RULES:
- Only output command
- No explanation
- No markdown
- One line only

Request:
{user_input}
"""
    }

    prompt = generate_prompt(context)
    response = query_groq(prompt)

    return response.strip().replace("```", "").split("\n")[0]


#  REAL HISTORY HANDLER
def show_history():
    try:
        history_file = os.path.expanduser("~/.bash_history")

        if not os.path.exists(history_file):
            print("No history found.")
            return

        with open(history_file, "r") as f:
            lines = f.readlines()

        print("\n📜 REAL LINUX HISTORY (Last 30 commands):\n")

        for i, line in enumerate(lines[-30:], 1):
            print(f"{i}. {line.strip()}")

    except Exception as e:
        print("Error reading history:", e)


#  Execute commands safely
def run_command(command):
    try:
        #  FIX HISTORY COMMAND
        if command.strip().lower() in ["history", "hiatory", "hstory"]:
            show_history()
            return

        os.system(command)

    except Exception as e:
        print("Execution error:", e)


#  MAIN LOOP
def run_terminal():
    user_profile = get_or_create_enhanced_user_profile()

    print("\n🤖 AI Terminal Started (type 'exit' to quit)\n")

    while True:
        user_input = input("AI> ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        if not user_input:
            continue

        #  Generate AI command
        command = generate_command(user_input, user_profile)

        print(f"\n🧠 Command: {command}")

        run = input("Execute? (y/n): ")

        if run.lower() == "y":
            print("\n🚀 Running...\n")
            run_command(command)
        else:
            print("❌ Skipped")


# ▶️ENTRY POINT
if __name__ == "__main__":
    run_terminal()
