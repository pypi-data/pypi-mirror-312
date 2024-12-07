import paramiko
import time
from typing import Optional, Dict, Union, List


class PersistentSSHRunner:
    def __init__(
        self,
        hostname: str,
        username: str,
        password: Optional[str] = None,
        key_filename: Optional[str] = None,
        port: int = 22,
        timeout: int = 30,
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.timeout = timeout
        self.ssh = None

    def connect(self):
        """Establish SSH connection."""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            key_filename=self.key_filename,
            port=self.port,
            timeout=self.timeout,
        )

    def run_persistent_command(
        self, command: str, output_file: str
    ) -> Dict[str, Union[int, str]]:
        """
        Run a command that persists after terminal closure.
        Args:
            command: The command to run
            output_file: Path where command output should be saved on remote system
        """
        if not self.ssh:
            self.connect()

        # Construct a persistent command that:
        # 1. Uses nohup to keep running after ssh disconnects
        # 2. Redirects stdout and stderr to the output file
        # 3. Runs in background
        # 4. Saves PID for later checking
        persistent_command = f"""
            nohup bash -c '
                {{ {command}; }} > {output_file} 2>&1 & 
                echo $! > {output_file}.pid
            '
        """

        # Execute the wrapped command
        session = self.ssh.get_transport().open_session()
        session.exec_command(persistent_command)

        # Wait briefly to ensure the PID file is created
        time.sleep(1)

        # Get the PID
        _, stdout, _ = self.ssh.exec_command(f"cat {output_file}.pid")
        pid = stdout.read().decode().strip()

        return {"pid": pid, "output_file": output_file}

    def check_command_status(self, pid: str) -> Dict[str, Union[bool, str]]:
        """Check if a command is still running using its PID."""
        if not self.ssh:
            self.connect()

        # Check if process is running
        _, stdout, _ = self.ssh.exec_command(f"ps -p {pid} > /dev/null 2>&1; echo $?")
        exit_status = stdout.read().decode().strip()

        is_running = exit_status == "0"

        return {"running": is_running, "pid": pid}

    def get_command_output(self, output_file: str) -> str:
        """Get the current content of the output file."""
        if not self.ssh:
            self.connect()

        _, stdout, _ = self.ssh.exec_command(f"cat {output_file}")
        return stdout.read().decode()

    def kill_command(self, pid: str) -> bool:
        """Kill a running command using its PID."""
        if not self.ssh:
            self.connect()

        _, stdout, _ = self.ssh.exec_command(f"kill {pid} > /dev/null 2>&1; echo $?")
        exit_status = stdout.read().decode().strip()

        return exit_status == "0"

    def close(self):
        """Close the SSH connection."""
        if self.ssh:
            self.ssh.close()
            self.ssh = None


# Example usage
if __name__ == "__main__":
    try:
        # Initialize SSH runner
        runner = PersistentSSHRunner(
            hostname="139.91.75.103",
            username="eflab",
            # password="your_password",  # Or use key_filename for key-based auth
        )

        # Start a long-running command that will persist
        result = runner.run_persistent_command(
            command="cd /home/eflab/github/EthoPy/;/usr/bin/sudo /usr/bin/python3 run.py",
            output_file="/tmp/long_running_task.log",
        )

        pid = result["pid"]
        output_file = result["output_file"]

        print(f"Started process with PID: {pid}")
        print("You can now close this terminal, and the process will continue running")
        print(f"To monitor it later, reconnect and check PID: {pid}")
        print(f"Output is being saved to: {output_file}")

        # Optional: Monitor for a while before closing
        for _ in range(3):
            time.sleep(5)
            status = runner.check_command_status(pid)
            print(f"Process still running: {status['running']}")
            print("Recent output:")
            print(runner.get_command_output(output_file))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        runner.close()
