from flask import Flask, render_template
from script import find_available_port, run_ansible_playbook

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    start_port = 8080
    end_port = 8084
    available_port = find_available_port(start_port, end_port)

    if available_port:
        try:
            run_ansible_playbook(available_port)
            return f"Container is running on port {available_port}"
        except subprocess.CalledProcessError as e:
            return f"Ansible playbook failed: {e}", 500
    else:
        return f"No available ports found between {start_port} and {end_port}.", 500

if __name__ == '__main__':
    app.run(debug=True)
