import os
import shutil
import subprocess
import sys
from pathlib import Path

from spark_dataproc_local_tools.utils import BASE_DIR


def validate_virtualenv_global():
    print("=====================================")
    print("====INSTALLING VIRTUALENV GLOBAL=====")
    print("=====================================")
    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        print("Instalando virtualenv globalmente...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "virtualenv"])
        print("virtualenv instalado exitosamente.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error durante la instalación de virtualenv: {e}")
    except FileNotFoundError:
        raise RuntimeError("pip no está instalado. Instala pip primero.")


def validate_path_virtualenv(env_path):
    print("=====================================")
    print("=========VALIDATE VIRTUALENV=========")
    print("=====================================")
    if os.path.exists(env_path):
        try:
            print(f"Eliminando el entorno virtual en: {env_path}")
            shutil.rmtree(env_path)
            print(f"Entorno virtual en '{env_path}' eliminado exitosamente.")
        except PermissionError as e:
            raise PermissionError(f"No se puede eliminar '{env_path}'. Permisos insuficientes.") from e
        except OSError as e:
            raise OSError(f"Error al intentar eliminar '{env_path}'.") from e


def get_install_virtualenv(env_path, pip_version):
    print("=====================================")
    print("=============INSTALL VENV============")
    print("=====================================")
    try:
        result = subprocess.check_output(
            ["virtualenv", env_path, "--no-pip", "--no-setuptools", "--no-wheel"],
            shell=True
        )
        env_path_dir = str(result.decode("utf8")).split("(")[1].split(",")[0].split("=")[1]
        print("env_path_dir =>", env_path_dir)
        print(f"Entorno virtual creado sin pip en: {env_path}")
        get_pip_path = os.path.join(BASE_DIR, "utils", "dataproc", "get-pip.py")
        is_windows = sys.platform.startswith('win')
        if is_windows:
            get_pip_path = get_pip_path.replace("\\", "/")
            env_path_dir = env_path_dir.replace("\\", "/")

        activate_script = os.path.join(env_path_dir, "Scripts", "activate.bat")
        subprocess.run(activate_script,check=True)
        python_executable = Path(env_path_dir) / ("Scripts" if sys.platform == "win32" else "bin") / "python"
        print("python_executable =>", python_executable)
        subprocess.run(
            [python_executable, get_pip_path, f"pip=={pip_version}"],
            check=True
        )
        print(f"pip {pip_version} instalado en el entorno virtual.")

    except subprocess.CalledProcessError as e:
        print(f"Error al crear el entorno virtual '{env_path}': {e}")
        return

    return env_path_dir


def get_library_install(env_path_dir):
    print("=====================================")
    print("===========INSTALL LIBRARY===========")
    print("=====================================")
    pip_path = Path(env_path_dir) / ("Scripts" if sys.platform == "win32" else "bin") / "pip"
    paquetes = ["setuptools==58.2.0", "jupyterlab==4.3.1", "findspark==2.0.1", "pkginfo==1.11.2",
                "cryptography==3.4.8", "pyopenssl==21.0.0", "pytz==2024.2"]
    if paquetes:
        for paquete in paquetes:
            try:
                subprocess.check_call([pip_path, "install", paquete])
                print(f"Paquete '{paquete}' instalado en el entorno '{env_path_dir}'.")
            except subprocess.CalledProcessError as e:
                print(f"Error al instalar el paquete '{paquete}': {e}")


def get_wheel_install(env_path_dir):
    print("=====================================")
    print("===========INSTALL WHEEL=============")
    print("=====================================")
    pip_path = Path(env_path_dir) / ("Scripts" if sys.platform == "win32" else "bin") / "pip"

    ether_http_client = os.path.join(BASE_DIR, "utils", "dataproc", "ether_http_client-0.2.2-py3-none-any.whl")
    dataproc_omega_handler = os.path.join(BASE_DIR, "utils", "dataproc", "dataproc_omega_handler-0.1.9-py3-none-any.whl")
    dataproc_sdk = os.path.join(BASE_DIR, "utils", "dataproc", "dataproc_sdk-0.4.9.3.1-py3-none-any.whl")
    pykaa = os.path.join(BASE_DIR, "utils", "dataproc", "pykaa-0.6.0-py3-none-any.whl")
    is_windows = sys.platform.startswith('win')

    if is_windows:
        ether_http_client = ether_http_client.replace("\\", "/")
        dataproc_omega_handler = dataproc_omega_handler.replace("\\", "/")
        dataproc_sdk = dataproc_sdk.replace("\\", "/")
        pykaa = pykaa.replace("\\", "/")

    wheels = [ether_http_client, dataproc_omega_handler, dataproc_sdk, pykaa]
    if wheels:
        for wheel in wheels:
            try:
                subprocess.check_call([pip_path, "install", wheel])
                print(f"Archivo .whl '{wheel}' instalado en el entorno '{env_path_dir}'.")
            except subprocess.CalledProcessError as e:
                print(f"Error al instalar el archivo .whl '{wheel}': {e}")


def run(env_path, pip_version="24.0"):
    """
    Args:
        env_path (str): Ruta donde se creará el entorno virtual.
        pip_version (str): Versión específica de pip a instalar (por defecto: 24.0).
    """
    validate_virtualenv_global()
    validate_path_virtualenv(env_path)
    env_path_dir = get_install_virtualenv(env_path, pip_version)
    get_library_install(env_path_dir)
    get_wheel_install(env_path_dir)
    return True
