import socket
import subprocess
import sys

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port, end_port):
    for port in range(start_port, end_port + 1):
        if not is_port_in_use(port):
            return port
    return None

def run_ansible_playbook(port):
    playbook_command = [
        'ansible-playbook',
        '-i', 'localhost,',
        '-e', f'container_port={port}',
        '-e', f'container_name=my-nginx-container-{port}',
        '/home/houda/dockerImages/docker_playbook.yml'
    ]
    subprocess.run(playbook_command, check=True)

if __name__ == "__main__":
    start_port = 8080
    end_port = 8084
    available_port = find_available_port(start_port, end_port)

    if available_port:
        print(f"Available port found: {available_port}")
        try:
            run_ansible_playbook(available_port)
        except subprocess.CalledProcessError as e:
            print(f"Ansible playbook failed: {e}")
            sys.exit(1)
    else:
        print(f"No available ports found between {start_port} and {end_port}.")
        sys.exit(1)

