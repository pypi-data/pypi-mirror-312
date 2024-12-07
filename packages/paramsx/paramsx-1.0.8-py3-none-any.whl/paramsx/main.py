import os
import boto3
import curses
import importlib.util
from .funcions import (
    draw_header, draw_footer, show_main_menu, show_comparison_results,
    show_environment_selection, show_message, show_parameter_selection,
    get_parameters_by_prefix, delete_parameter, export_parameters_to_file, 
    compare_parameters, load_parameters
)


# Ruta de la configuración personalizada
CONFIG_PATH = os.path.expanduser("~/.xsoft/paramsx_config.py")

# Cargar configuraciones desde el archivo de usuario
def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"No se encontró el archivo de configuración en {CONFIG_PATH}")
    spec = importlib.util.spec_from_file_location("config", CONFIG_PATH)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config.configuraciones

# Función principal
def main(stdscr):

    ## Cargando configuración
    config = load_config()
    # Configurar boto3 con el perfil y región del usuario
    boto3.setup_default_session(profile_name=config["profile_name"])
    ssm = boto3.client("ssm", region_name=config["region_name"])

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    environments = config['entornos']
    PARAMETER_LIST = config['parameter_list']

    while True:
        stdscr.clear()
        draw_header(stdscr)
        show_main_menu(stdscr)
        draw_footer(stdscr)
        stdscr.refresh()

        choice = stdscr.getkey()
        
        if choice == '\x1b':  # Código ASCII para 'Esc'
                break  # Salir del programa
        
        elif choice == '1':
            # Leer parámetros
            param_choice = show_parameter_selection(stdscr, PARAMETER_LIST)
            if param_choice is None:  # Si se presionó Esc
                continue  # Regresar al menú principal

            selected_param = PARAMETER_LIST[param_choice]

            env_choice = show_environment_selection(stdscr, environments)
            if env_choice is None:  # Si se presionó Esc
                continue  # Regresar al menú principal

            selected_env = environments[env_choice]

            # Crear el prefijo completo
            full_path = f"{selected_param}/{selected_env}"
            show_message(stdscr, f"Buscando parámetros en: {full_path}...", 3)  # Mensaje inicial

            try:
                # Obtener parámetros desde AWS SSM
                parameters = get_parameters_by_prefix(ssm, full_path)
            except ValueError as e:
                show_message(stdscr, f"ERROR: {e}", 2)  # Error por prefijo vacío
                continue  # Regresar al menú principal
            except Exception as e:
                show_message(stdscr, f"Error inesperado: {e}", 2)  # Error genérico
                continue  # Regresar al menú principal

            # Validar si se encontraron parámetros antes de continuar
            if not parameters:
                show_message(stdscr, f"No se encontraron parámetros en: {full_path}.", 2)
                continue  # Regresar al menú principal

            # Crear archivos si se encontraron parámetros
            file_name = f"parameters_{selected_env}.py"
            backup_file_name = f"parameters_{selected_env}_backup.py"

            # Exportar parámetros al archivo principal
            export_parameters_to_file(parameters, file_name)

            # Crear un respaldo exacto del archivo principal
            export_parameters_to_file(parameters, backup_file_name)

            # Confirmación de archivos creados
            show_message(stdscr, f"Archivos creados:\n- {file_name}\n- {backup_file_name}", 3)

        elif choice == '2':
            # Cargar parámetros desde archivo
            env_choice = show_environment_selection(stdscr, environments)
            if env_choice is None:  # Si se presionó Esc
                continue  # Regresar al menú principal

            selected_env = environments[env_choice]
            file_name = f"parameters_{selected_env}.py"
            backup_file_name = f"parameters_{selected_env}_backup.py"

            if not os.path.exists(file_name) or not os.path.exists(backup_file_name):
                show_message(stdscr, f"Archivos {file_name} o {backup_file_name} no encontrados.", 2)
                continue


            try:
                # Cargar parámetros del archivo principal
                parametros = load_parameters(file_name)
            except SyntaxError as e:
                show_message(stdscr, f"ERROR: {e}", 2)
                continue  # Regresar al menú principal
            except Exception as e:
                show_message(stdscr, f"Error inesperado: {e}", 2)
                continue  # Regresar al menú principal

            # Comparar los parámetros
            changes = compare_parameters(file_name, backup_file_name, stdscr)

            if changes:
                # Mostrar resultados de la comparación
                confirmed = show_comparison_results(stdscr, changes)

                if not confirmed:  # Si el usuario cancela
                    show_message(stdscr, "Operación cancelada volvemos a menú principal.", 2)
                    continue

                # Subir parámetros si se confirman los cambios
                with open(file_name, 'r') as f:
                    param_scope = {}
                    exec(f.read(), param_scope)

                parametros = param_scope.get('parametros', [])
                current_dict = {p['parameter_name']: p['parameter_value'] for p in parametros}

                for change in changes:
                    param_name, change_type, _ = change
                    if change_type == "Nuevo" or change_type == "Modificado":
                        # Subir o actualizar parámetros
                        ssm.put_parameter(
                            Name=param_name,
                            Value=current_dict[param_name],
                            Type='SecureString',
                            Overwrite=True
                        )
                    elif change_type == "Eliminado":
                        # Borrar parámetros eliminados
                        delete_parameter(ssm, param_name)

                # Eliminar los archivos una vez procesados
                os.remove(file_name)
                os.remove(backup_file_name)
                show_message(stdscr, "¡Cambios aplicados y archivos eliminados!", 3)
            else:
                show_message(stdscr, "No se encontraron cambios entre los archivos.", 3)

        elif choice == '3':
            # Crear backup
            param_choice = show_parameter_selection(stdscr, PARAMETER_LIST)
            if param_choice is None:  # Si se presionó Esc
                continue  # Regresar al menú principal

            selected_param = PARAMETER_LIST[param_choice]

            env_choice = show_environment_selection(stdscr, environments)
            if env_choice is None:  # Si se presionó Esc
                continue  # Regresar al menú principal

            selected_env = environments[env_choice]

            # Crear el prefijo completo
            full_path = f"{selected_param}/{selected_env}"
            try:
                # Obtener parámetros desde AWS SSM
                parameters = get_parameters_by_prefix(ssm, full_path)
            except ValueError as e:
                show_message(stdscr, f"ERROR: {e}", 2)
                continue  # Regresar al menú principal
            except Exception as e:
                show_message(stdscr, f"Error inesperado: {e}", 2)
                continue  # Regresar al menú principal

            # Crear archivo de backup con nombre claro
            backup_file_name = f"{selected_param.replace('/', '_')}_{selected_env}_backup.py"
            export_parameters_to_file(parameters, backup_file_name)

            # Confirmación de backup creado
            show_message(stdscr, f"Backup creado:\n- {backup_file_name}", 3)


        else:
            show_message(stdscr, "Opción inválida. Inténtalo de nuevo.", 2)

def entry_point():
    curses.wrapper(main)

if __name__ == "__main__":
    curses.wrapper(main)