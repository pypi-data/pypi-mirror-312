# ethopy/cli.py
import os
import json
import subprocess
import getpass

def init_db():
    """Initialize the database environment using Docker"""
    try:
        # Create directory for MySQL Docker setup
        os.makedirs('mysql-docker', exist_ok=True)
        os.chdir('mysql-docker')
        
        # Download docker-compose file
        subprocess.run(['wget', 'https://raw.githubusercontent.com/datajoint/mysql-docker/master/docker-compose.yaml'], check=True)
        
        # Get password securely
        mysql_password = getpass.getpass("Enter the MySQL root password: ")
        
        # Update docker-compose file
        with open('docker-compose.yaml', 'r') as f:
            content = f.read()
        content = content.replace('MYSQL_ROOT_PASSWORD=simple', f'MYSQL_ROOT_PASSWORD={mysql_password}')
        with open('docker-compose.yaml', 'w') as f:
            f.write(content)
        
        # Start Docker container
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        
        # Clone and setup testcore
        subprocess.run(['git', 'clone', 'https://github.com/alexevag/testcore.git'], check=True)
        os.chdir('testcore')
        
        # # Create configuration files
        # create_config_files(mysql_password)
        
        print("Database initialization completed successfully!")

    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        return str(e)
