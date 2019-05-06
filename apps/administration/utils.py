import shutil


def check_docker():
    """
    Checks if docker is installed.
    """
    return True if shutil.which('docker') else False
