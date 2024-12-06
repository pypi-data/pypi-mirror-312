

import os
import subprocess

def run_command(command):
    """Run a terminal command."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout, result.stderr

def shortcut_python():
    """Shortcut to run Python."""
    return run_command("python3")

def create_virtualenv(env_name):
    """Create a virtual environment."""
    run_command(f"python3 -m venv {env_name}")
    return run_command(f"source {env_name}/bin/activate")

def list_virtualenvs():
    """List all virtual environments (requires virtualenvwrapper)."""
    return run_command("lsvirtualenv")

def activate_virtualenv(env_name):
    """Activate a virtual environment."""
    return f"source {env_name}/bin/activate"

def deactivate_virtualenv():
    """Deactivate the current virtual environment."""
    return run_command("deactivate")

def remove_virtualenv(env_name):
    """Remove a virtual environment."""
    return run_command(f"rm -rf {env_name}")

def install_package(package):
    """Install a package in the current environment."""
    return run_command(f"pip install {package}")

def check_env_python_version():
    """Check the Python version in the current environment."""
    return run_command("python --version")

def install_requirements():
    """Install dependencies from requirements.txt."""
    return run_command("pip install -r requirements.txt")

def list_files():
    """List files in the current directory."""
    return run_command("ls -la")

def change_directory(directory):
    """Change the current directory."""
    os.chdir(directory)
    return f"Changed directory to {directory}"

def remove_file(file):
    """Remove a file."""
    return run_command(f"rm {file}")

def copy_file(source, destination):
    """Copy a file."""
    return run_command(f"cp {source} {destination}")

def move_file(source, destination):
    """Move or rename a file."""
    return run_command(f"mv {source} {destination}")

def create_directory(directory):
    """Create a new directory."""
    return run_command(f"mkdir {directory}")

def current_directory():
    """Show the current directory."""
    return os.getcwd()

def clear_screen():
    """Clear the terminal screen."""
    return run_command("clear")

def check_disk_usage():
    """Check disk usage."""
    return run_command("df -h")

def check_python_version():
    """Check the Python version."""
    return run_command("python3 --version")

def run_script(script):
    """Run a Python script."""
    return run_command(f"python3 {script}")

def list_installed_packages():
    """List installed Python packages."""
    return run_command("pip list")

def show_package_info(package):
    """Show information about a specific package."""
    return run_command(f"pip show {package}")

def upgrade_package(package):
    """Upgrade a specific package."""
    return run_command(f"pip install --upgrade {package}")

def uninstall_package(package):
    """Uninstall a specific package."""
    return run_command(f"pip uninstall -y {package}")

def create_requirements_file():
    """Create a requirements.txt file from installed packages."""
    return run_command("pip freeze > requirements.txt")



def start_jupyter_notebook():
    """Start a Jupyter Notebook server."""
    return run_command("jupyter notebook")
