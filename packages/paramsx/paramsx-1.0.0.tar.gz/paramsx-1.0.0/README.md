# ParamsX

ParamsX es una librería diseñada para gestionar parámetros de AWS SSM de manera sencilla y eficiente. Con ella podrás:
- Leer parámetros almacenados en AWS SSM.
- Comparar y actualizar parámetros existentes.
- Eliminar parámetros que ya no estén presentes en los archivos de configuración.
- Crear respaldos para evitar pérdida de datos.


#### Consejos varios para tener un orden en los parámetros
Para un uso óptimo, se recomienda organizar los parámetros de AWS SSM utilizando prefijos que sigan una estructura lógica. Por ejemplo:
- /APP/nombreApp/tipoEntorno/más datos...

Esta estructura permite identificar y gestionar los parámetros por su aplicación y entorno. En ParamsX, puedes configurar listas específicas para modificar y gestionar estos parámetros de manera eficiente.

## Instalación

pip install paramx

### Configuración inicial
Al instalar el paquete, se crea automáticamente una carpeta de configuración en tu directorio de usuario:

Windows: C:\Users\<tu_usuario>\.xsoft
Linux/MacOS: /home/<tu_usuario>/.xsoft

Dentro de esta carpeta encontrarás un archivo llamado paramsx_config.py. 
Este archivo contiene la configuración inicial de la librería. Antes de usarla, debes asegurarte de editar este archivo para incluir el perfil de AWS y la región que utilizarás.

Contenido de paramsx_config.py:

```
configuraciones = {
    "profile_name": "default",  # Cambiar por el nombre de tu perfil en ~/.aws/credentials
    "region_name": "us-east-1",  # Cambiar por tu región de AWS
    "entornos": ["DEV", "PROD"],  # Los entornos que manejarás
    "parameter_list": [
        "/params1/xx",
        "/params2/xx",
    ]
}
```
Nota: Si el archivo paramsx_config.py ya existe, no será sobrescrito durante la instalación para proteger las configuraciones personalizadas.


## Modo de Uso
Ejecuta el comando principal desde la terminal:

```paramsx```

Navega por el menú interactivo:

El programa mostrará un menú donde Podrás:
- Leer parámetros desde AWS SSM.
- Cargar y actualizar parámetros.
- Backup de parámetros.


### Leer Parámetros:
1. Selecciona la opción "Leer parámetros" en el menú.
2. Elige el prefijo y el entorno que deseas consultar.
3. Los parámetros serán descargados y guardados en archivos como:
    - parameters_DEV.py
    - parameters_DEV_backup.py
    ```Importante: Los archivos se generarán en la misma ruta desde donde ejecutes el comando paramsx```


### Cargar Parámetros:
1. Modifica los archivos generados (parameters_DEV.py).
2. Usa la opción "Cargar parámetros desde archivo" para comparar los cambios.
3. El programa mostrará una lista con los siguientes estados:
    - Nuevos: Parámetros que se agregarán.
    - Modificados: Parámetros existentes que se actualizarán.
    - Eliminados: Parámetros que se eliminarán automáticamente de AWS SSM.
    * Revisa los cambios antes de confirmar.
    ```Importante: Una vez confirmados los cambios, los archivos parameters_DEV.py y parameters_DEV_backup.py se eliminarán automáticamente```

### Notas Adicionales
- Credenciales de AWS:
    Asegúrate de que el perfil especificado en paramsx_config.py exista en tus archivos de configuración de AWS (~/.aws/credentials y ~/.aws/config).

- Seguridad:
    Los parámetros se manejan como SecureString para garantizar que la información sensible esté cifrada

- Backup:
    Antes de realizar cualquier cambio, ParamsX crea automáticamente un respaldo (parameters_DEV_backup.py). Este archivo se eliminará después de cargar los nuevos parámetro

## Licencia
ParamsX se distribuye bajo la licencia MIT. Puedes usarlo libremente, modificarlo y adaptarlo a tus necesidades. Recuerda siempre hacer un respaldo de tus configuraciones antes de realizar cambios.
```Nota: El creador de ParamsX no se hace responsable de posibles pérdidas de datos o configuraciones incorrectas.```