# Gerard Diaz y Cristian Martinez

## Clona el repositorio
    ```bash
    git clone https://github.com/Nocturnete/M12PRO1.git
    ```

## Ponte dentro del directorio
    ```bash
    cd M12PRO1
    ```
## Instala los requisitos
    ```bash
    pip install -r requirements.txt
    ```

## Importa los CSV a la base de datos

    1. Abre la aplicación DB Browser for SQLite.
    2. Abre la base de datos del proyecto: selecciona Abrir base de datos y elige database.db.
    3. Importa los archivos .csv en este orden (user.csv, categorias.csv, products.csv):
    Ve a Archivo > Importar > Tabla desde archivo CSV.
        Selecciona el archivo correspondiente y haz clic en Abrir.
        Asegúrate de configurar correctamente las opciones de importación, como el nombre de la tabla y las opciones de delimitadores.
        Haz clic en Aceptar o Importar para completar el proceso de importación.
    4. Haz clic en Escribir en la base de datos para guardar los cambios.

## Ejecuta
    flask --debug run