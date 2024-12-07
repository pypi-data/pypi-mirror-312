# ethopy/__main__.py
import sys
import subprocess
from typing import List

def get_import_commands() -> List[str]:
    """Get list of commands to create schemas in correct order"""
    return [
        "from ethopy.core.Experiment import *",
        "from ethopy.core.Stimulus import *",
        "from ethopy.core.Behavior import *",
        "from ethopy.Stimuli import *",
        "from ethopy.Behaviors import *",
        "from ethopy.Experiments import *"
    ]

def create_schemas():
    """Create schemas by running import commands as separate processes"""
    print("Creating schemas and tables...")
    
    for cmd in get_import_commands():
        try:
            subprocess.run(["python", "-c", cmd], check=True)
            print(f"Successfully executed: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {cmd}: {str(e)}")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'initdb':
            from .cli import init_db
            init_db()
            return
        if sys.argv[1] == 'createschema':
            create_schemas()
            return
        from .ethopy import run_ethopy
        error = run_ethopy(sys.argv[1])
        if error:
            print(error)
    else:
        from .ethopy import run_ethopy
        error = run_ethopy(False)
        if error:
            print(error)

if __name__ == "__main__":
    main()