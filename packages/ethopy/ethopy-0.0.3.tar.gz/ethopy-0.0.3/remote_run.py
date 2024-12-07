import time
from typing import Dict, Optional, Union

import paramiko


def run_remote_script(
    hostname: str,
    username: str,
    script_content: str,
    password: Optional[str] = None,
    key_filename: Optional[str] = None,
    port: int = 22,
    timeout: int = 30,
) -> Dict[str, Union[int, str]]:
    """
    Connects to a remote host via SSH, executes a script, and returns the results.

    Args:
        hostname (str): The remote server hostname or IP address
        username (str): SSH username
        script_content (str): The content of the script to execute
        password (str, optional): SSH password (if not using key-based auth)
        key_filename (str, optional): Path to private key file
        port (int): SSH port number (default: 22)
        timeout (int): Connection timeout in seconds (default: 30)

    Returns:
        dict: Dictionary containing exit code, stdout, and stderr

    Raises:
        paramiko.AuthenticationException: If authentication fails
        paramiko.SSHException: If SSH connection fails
        Exception: For other errors during execution
    """
    # Initialize the SSH client
    ssh = paramiko.SSHClient()

    try:
        # Add the host key automatically if not present
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote host
        ssh.connect(
            hostname=hostname,
            username=username,
            password=password,
            key_filename=key_filename,
            port=port,
            timeout=timeout,
        )

        # Create a session
        session = ssh.get_transport().open_session()
        session.set_combine_stderr(True)  # Combine stdout and stderr

        # Execute the script
        session.exec_command(script_content)

        # Get the output
        output = ""
        while True:
            if session.recv_ready():
                output += session.recv(4096).decode("utf-8")
            if session.exit_status_ready():
                break
            time.sleep(0.1)

        exit_status = session.recv_exit_status()

        return {"exit_code": exit_status, "output": output.strip()}

    except Exception as e:
        raise Exception(f"Failed to execute script: {str(e)}")

    finally:
        # Always close the SSH connection
        ssh.close()


# Example usage
if __name__ == "__main__":
    # Example script to run
    example_script = """#!/bin/bash
    echo "Current directory:"
    pwd
    echo "Files in current directory:"
    ls -la
    cd /home/eflab/github/EthoPy/
    sudo python3 run.py 28
    """

    try:
        result = run_remote_script(
            hostname="139.91.75.103",
            username="eflab",
            script_content=example_script,
            password="your_password",  # Or use key_filename for key-based auth
        )

        print(f"Exit Code: {result['exit_code']}")
        print(f"Output:\n{result['output']}")

    except Exception as e:
        print(f"Error: {e}")
