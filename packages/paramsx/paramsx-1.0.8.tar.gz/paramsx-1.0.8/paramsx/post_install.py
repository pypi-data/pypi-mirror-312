import os
import shutil

def run_post_install():
    config_dir = os.path.expanduser("~/.xsoft")
    os.makedirs(config_dir, exist_ok=True)

    config_file = os.path.join(os.path.dirname(__file__), "paramsx", "paramsx_config.py")
    target_file = os.path.join(config_dir, "paramsx_config.py")

    if not os.path.exists(target_file):
        if os.path.exists(config_file):
            shutil.copy(config_file, target_file)
            print(f"Archivo de configuración copiado a {target_file}")
        else:
            print(f"Advertencia: No se encontró {config_file}. No se creó la configuración inicial.")

if __name__ == "__main__":
    run_post_install()