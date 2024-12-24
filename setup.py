import os
import subprocess
import venv


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


def main():
    venv_path = '.venv'
    requirements_file = 'requirements.txt'

    create_venv(venv_path)
    install_requirements(venv_path, requirements_file)

    print("Virtual environment setup complete, starting the app...")


if __name__ == "__main__":
    main()