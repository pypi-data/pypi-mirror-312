import logic
import sys
import subprocess
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer
from datetime import datetime

UPGRADE_COUNTER = 0
SERVER_VERSION = ""
REPEATING_TIMER = None
SERVICE_STOP = 0

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



def update_and_run(package_name, package_version):
    try:
        # Log the package update attempt
        logic.ci_print(f"Attempting to update package '{package_name}' to version '{package_version}'")

        # Get the current directory and Python executable path
        current_directory = os.getcwd()
        python_path = sys.executable
        python_lib_path = os.path.join(os.path.dirname(python_path), "Lib", "site-packages")

        logic.ci_print(f"Current directory: {current_directory}")
        logic.ci_print(f"Python executable path: {python_path}")
        logic.ci_print(f"Python library path: {python_lib_path}")

        if package_version == '':
            # Upgrade the package
            command = ["pip", "install", "--upgrade", package_name]
        else:
            # Install or upgrade the package with specific version
            command = ["pip", "install", "--force-reinstall", f"{package_name}=={package_version}"]

        logic.ci_print(f"Running command: {' '.join(command)}")

        # Run the pip command
        result = subprocess.run(command, capture_output=True, text=True)

        logic.ci_print(f"Command output: {result.stdout}")
        logic.ci_print(f"Command error: {result.stderr}")

        if result.returncode != 0:
            logic.ci_print(f"Command failed with exit status {result.returncode}")
            return

        # Package update success
        logic.ci_print(f"Package '{package_name}' updated successfully to version '{package_version or 'latest'}'")


        source_path_logic = os.path.join(python_lib_path, "logic.py")
        source_path_main = os.path.join(python_lib_path, "main.py")
        source_path_myservice = os.path.join(python_lib_path, "myservice.py")
        source_path_setup = os.path.join(python_lib_path, "setup.py")

        destination_path_logic = os.path.join(current_directory, "logic.py")
        destination_path_main = os.path.join(current_directory, "main.py")
        destination_path_myservice = os.path.join(current_directory, "myservice.py")
        destination_path_setup = os.path.join(current_directory, "setup.py")

        shutil.copy(source_path_logic, destination_path_logic)
        shutil.copy(source_path_main, destination_path_main)
        shutil.copy(source_path_myservice, destination_path_myservice)
        shutil.copy(source_path_setup, destination_path_setup)
        
    except subprocess.CalledProcessError as e:
        logic.handleError(f"Subprocess error during package update: {e}", e)
        logic.ci_print(f"Error details: return code {e.returncode}, output: {e.output}")
    except Exception as e:
        logic.handleError(f"Unexpected error occurred: {e}", e)



def upgrade_version(new_version="", current_version=""):
    try:
        logic.ci_print(f"Attempting to upgrade from version {current_version} to version {new_version}")
        update_and_run("CI_CloudConnector", new_version)
        logic.ci_print("Upgrade successful.")

    except Exception as ex:
        logic.handleError("Error occurred during version upgrade: ", ex)


def MainLoopTimer():
    logic.ci_print(f"MainLoopTimer: {str(datetime.now())}", "INFO")

    global REPEATING_TIMER

    if REPEATING_TIMER:
        REPEATING_TIMER.stop()

    if SERVICE_STOP == 1:
        REPEATING_TIMER = None
        return

    try:
        MainLoop()
    except Exception as e:
        logic.handleError(f"Error occurred in MainLoopTimer", e)

    if REPEATING_TIMER:
        REPEATING_TIMER.start()
    else:
        REPEATING_TIMER = RepeatedTimer(5, MainLoopTimer)


def MainLoop():
    global SERVER_VERSION
    global UPGRADE_COUNTER

    try:
        # Get version and update if needed
        logic.get_cloud_version()
        local_ver = str(logic.getLocalVersion())
        update_to_ver = str(logic.getServerSugestedVersion())

        # To prevent upgrading too much in case of a problem, count upgrade attempts and stop when it's too big.
        # If the version changes, try again.
        if SERVER_VERSION != update_to_ver:
            SERVER_VERSION = update_to_ver
            UPGRADE_COUNTER = 0

        if str(update_to_ver) == "None":
            update_to_ver = ""

        if (bool(update_to_ver != "") & bool(update_to_ver != local_ver) & bool(UPGRADE_COUNTER < 10)):
            UPGRADE_COUNTER += 1
            logic.ci_print(
                f"Starting auto upgrade from: {local_ver} to: {update_to_ver}, Upgrade count: {UPGRADE_COUNTER}",
                "INFO")
            upgrade_version(update_to_ver, local_ver)

        logic.Main()
    except Exception as e:
        logic.handleError(f"Error occurred in MainLoop", e)


def StartMainLoop():
    global REPEATING_TIMER
    try:
        REPEATING_TIMER = RepeatedTimer(5, MainLoopTimer)
    except Exception as inst:
        logic.handleError("Error occurred in StartMainLoop", inst)


def args(argv):
    if len(argv) > 1 and argv[1] == "Start":
        StartMainLoop()


class MainFileChangeHandler(FileSystemEventHandler):
    def __init__(self, main_file, service):
        super().__init__()
        self.main_file = main_file
        self.myService = service

    def on_modified(self, event):

        try:
            if event.src_path.endswith(self.main_file):
                logic.ci_print("Main file has been modified. Signaling service to restart...")

                # Stop the service
                self.myService.ServiceUpdated()
                logic.ci_print("Service stopped. You may restart it if necessary.")

        except Exception as e:
            logic.handleError(f"Error occurred during file modification event handling", e)

def monitor_main_file(file_name, service):
    try:
        observer = Observer()

        current_dir = os.getcwd()
        
        event_handler = MainFileChangeHandler(file_name, service)
        observer.schedule(event_handler, path=current_dir, recursive=False)
        
        observer.start()
        logic.ci_print(f"Monitoring main file: {file_name}")

        return observer

    except Exception as e:
        logic.handleError(f"Error occurred while setting up file monitoring", e)
        return None


def serviceStop():
    global SERVICE_STOP
    SERVICE_STOP = 1
    logic.ci_print("Service stop requested.")


def set_service_restart_delay(service_name, delay_milliseconds):
    command = f'sc failure {service_name} reset= 0 actions= restart/{delay_milliseconds}'
    try:
        subprocess.run(command, shell=True, check=True)
        logic.ci_print(f"Restart delay for service '{service_name}' set to {delay_milliseconds} milliseconds.")
    except subprocess.CalledProcessError as e:
        logic.ci_print(f"Error setting restart delay for service '{service_name}': {e}")


def set_service_startup_type(service_name, startup_type):
    """
    Set the startup type for a Windows service.

    Args:
        service_name (str): The name of the service.
        startup_type (str): The startup type to set ('auto', 'demand', 'disabled', 'delayed-auto').

    Returns:
        bool: True if the command is executed successfully, False otherwise.
    """
    try:
        subprocess.run(['sc', 'config', service_name, 'start=' + startup_type], check=True, shell=True)
        logic.ci_print(f"Service '{service_name}' startup type set to '{startup_type}'.")
    except subprocess.CalledProcessError as e:
        logic.handleError(f"Failed to set service startup type. Error: {e}")


def change_working_directory():
    try:
        new_directory = os.path.dirname(os.path.realpath(__file__))
    
        # Get the current working directory before changing it
        current_directory = os.getcwd()
                
        logic.ci_print(f"Current Working Directory: {current_directory}")

        # Change the working directory
        os.chdir(new_directory)

        # Verify the directory change
        logic.ci_print(f"New Working Directory: {os.getcwd()}")

    except FileNotFoundError as e:
        logging.error(f"Directory not found: {new_directory}")
        sys.exit(1)
    except PermissionError as e:
        logging.error(f"Permission denied: {new_directory}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred while changing directory: {e}")
        sys.exit(1)

        
def init():
    change_working_directory();
    logic.initialize_config()
    set_service_restart_delay("PlantSharpEdgeGateway", 10000)
    set_service_startup_type("PlantSharpEdgeGateway", "auto")


if __name__ == '__main__':
    init()
    args(sys.argv)
    monitor_main_file('logic.py')