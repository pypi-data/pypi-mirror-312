import tkinter as tk
from tkinter import scrolledtext, messagebox
import paramiko
from threading import Thread

class RemoteExecutor:
    def __init__(self, master):
        self.master = master
        self.master.title("Remote Python Executor")

        # IP Address
        tk.Label(master, text="IP Address:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = tk.Entry(master)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        # Username
        tk.Label(master, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        # Password
        tk.Label(master, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Remote File Path
        tk.Label(master, text="Remote Path:").grid(row=3, column=0, padx=5, pady=5)
        self.remote_path_entry = tk.Entry(master)
        self.remote_path_entry.grid(row=3, column=1, padx=5, pady=5)

        # Execute Button
        self.execute_button = tk.Button(master, text="Upload and Execute", command=self.execute_command)
        self.execute_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Output Text Box
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=20)
        self.output_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def execute_command(self):
        ip = self.ip_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        remote_path = self.remote_path_entry.get()

        if not ip or not username or not password or not remote_path:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        self.output_text.delete(1.0, tk.END)
        thread = Thread(target=self.run_ssh_command, args=(ip, username, password, remote_path))
        thread.start()

    def run_ssh_command(self, ip, username, password, remote_path):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)

            sftp = ssh.open_sftp()
            sftp.put('remote_script.py', remote_path)
            sftp.close()

            # Enable X11 forwarding
            transport = ssh.get_transport()
            session = transport.open_session()
            session.get_pty()
            session.set_combine_stderr(True)
            session.exec_command('export DISPLAY=:0.0 && python3 {}'.format(remote_path))

            while True:
                if session.recv_ready():
                    output = session.recv(4096).decode()
                    self.output_text.insert(tk.END, output)
                    self.output_text.yview(tk.END)
                if session.recv_stderr_ready():
                    error = session.recv_stderr(4096).decode()
                    self.output_text.insert(tk.END, error)
                    self.output_text.yview(tk.END)
                if session.exit_status_ready():
                    break

            ssh.close()
        except Exception as e:
            self.output_text.insert(tk.END, "Error: {}\n".format(str(e)))
            self.output_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = RemoteExecutor(root)
    root.mainloop()
