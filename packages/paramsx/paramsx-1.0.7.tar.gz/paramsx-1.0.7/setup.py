from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import shutil
import platform

class CustomInstallCommand(install):
    def run(self):
        # Ejecutar instalación predeterminada
        install.run(self)

        # 1. Agregar directorio de scripts al PATH
        self._add_scripts_to_path()

        # 2. Crear carpeta de configuración .xsoft
        self._create_config_folder()

    def _add_scripts_to_path(self):
        system = platform.system()
        scripts_dir = None

        if system == "Windows":
            # Ruta del directorio de scripts en Windows
            scripts_dir = os.path.join(
                os.path.expanduser("~"),
                "AppData",
                "Roaming",
                "Python",
                f"Python{sys.version_info.major}{sys.version_info.minor}",
                "Scripts",
            )
        elif system in ["Linux", "Darwin"]:  # Linux o macOS
            scripts_dir = os.path.join(os.path.dirname(sys.executable), "bin")

        if scripts_dir:
            path_env = os.environ.get("PATH", "")
            if scripts_dir not in path_env:
                if system == "Windows":
                    os.system(f'setx PATH "{path_env};{scripts_dir}"')
                    print(f"Se agregó {scripts_dir} al PATH. Reinicia tu terminal para que los cambios surtan efecto.")
                elif system == "Darwin":
                    self._add_to_shell_config("~/.zshrc", scripts_dir)
                elif system == "Linux":
                    self._add_to_shell_config("~/.bashrc", scripts_dir)

    def _create_config_folder(self):
        config_dir = os.path.expanduser("~/.xsoft")
        os.makedirs(config_dir, exist_ok=True)

        config_file = "paramsx/paramsx_config.py"
        target_file = os.path.join(config_dir, "paramsx_config.py")

        if os.path.exists(target_file):
            print(f"El archivo de configuración ya existe en {target_file}. No se sobrescribirá.")
        else:
            if os.path.exists(config_file):
                shutil.copy(config_file, target_file)
                print(f"Archivo de configuración copiado a {target_file}")
            else:
                print(f"Advertencia: No se encontró {config_file}. No se creó la configuración inicial.")


    def _add_to_shell_config(self, config_file, scripts_dir):
        """Añadir el directorio de scripts al archivo de configuración de shell."""
        export_line = f'export PATH="{scripts_dir}:$PATH"'
        if os.path.exists(config_file):
            with open(config_file, "a") as f:
                f.write(f"\n{export_line}\n")
            print(f"Se agregó {scripts_dir} a {config_file}.")
        else:
            with open(config_file, "w") as f:
                f.write(f"{export_line}\n")
            print(f"Se creó {config_file} y se agregó {scripts_dir}.")

install_requires = ["boto3"]

# Añadir windows-curses si el sistema es Windows
if platform.system() == "Windows":
    install_requires.append("windows-curses")

setup(
    name="paramsx",
    version="1.0.7",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'paramsx': ['paramsx_config.py'],  # Archivos específicos
    },
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "paramsx=paramsx.main:entry_point",
        ],
    },
    cmdclass={
        "install": CustomInstallCommand,
    },
    description="Librería para gestionar y respaldar parámetros de AWS SSM de manera sencilla y eficiente.",
    author="Mariox",
    author_email="info@tomonota.net",
    url="https://github.com/pistatxos/paramsx",
)
