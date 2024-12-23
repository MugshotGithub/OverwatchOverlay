import os
import subprocess
import threading
import venv

from WebApp import app as flask_app
from waitress import serve
import GUI

def create_venv(venv_path):
    if not os.path.exists(venv_path):
        venv.create(venv_path, with_pip=True)
    else:
        print(f"Virtual environment already exists at {venv_path}.")

def install_requirements(venv_path, requirements_file):
    pip_executable = os.path.join(venv_path, 'Scripts', 'pip')
    if not os.path.exists(requirements_file):
        print(f"Requirements file '{requirements_file}' not found.")
        return

    subprocess.check_call([pip_executable, 'install', '-r', requirements_file])

def run_flask():
    serve(flask_app, host='127.0.0.1', port=5000)

def start_gui_thread():
    app = GUI.App()
    app.mainloop()

def main():
    venv_path = '.venv'
    requirements_file = 'requirements.txt'

    create_venv(venv_path)
    install_requirements(venv_path, requirements_file)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start GUI in the main thread
    start_gui_thread()

if __name__ == "__main__":
    main()