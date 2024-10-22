import flet as ft
import os

def main(page: ft.Page):
    # Establecemos el color de fondo en verde agua (verde claro)
    page.bgcolor = "#34495e"  # Color verde agua

    # Creamos una lista para almacenar los ítems de la compra
    shopping_list = []

    # Cargamos la imagen del logo desde el directorio actual
    logo = ft.Image(src="../img/logo.png", width=200, height=150)

    # Definimos las dimensiones de la ventana
    page.window_width = 450  # Ancho de la ventana
    page.window_height = 650  # Alto de la ventana
    page.title = "Lista de Compras"

    # Función para mostrar un cuadro de diálogo en caso de intentar agregar un ítem vacío
    def show_error_dialog():
        def close_dlg(e):
            page.dialog.open = False  # Cerrar el diálogo
            page.update()  # Actualizar la página

        page.dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text("No puedes agregar un ítem en blanco."),  # No se puede agregar un ítem vacío
            actions=[ft.TextButton("OK", on_click=close_dlg)],  # Botón para cerrar el diálogo
            open=True
        )
        page.update()

    # Función para agregar un nuevo ítem
    def add_clicked(e):
        # Verificamos si el campo de entrada está vacío
        if not new_task.value.strip():  # Validar entrada
            show_error_dialog()  # Mostrar diálogo de error
            return

        # Crear y agregar el ítem si la entrada es válida
        item = create_item(new_task.value)
        shopping_list.append(new_task.value)  # Añadir el ítem a la lista de compras
        page.add(item)  # Agregar el ítem a la página
        new_task.value = ""  # Limpiar el campo de entrada
        new_task.focus()  # Enfocar el campo para una nueva entrada

    # Crear un ítem de compra con un checkbox y botones de editar/eliminar
    def create_item(text):
        checkbox = ft.Checkbox(label=text)
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, text))
        item = ft.Row([checkbox, edit_button, delete_button])  # Combinar controles en una fila
        return item

    # Función para editar un ítem existente
    def edit_clicked(e, checkbox, item):
        new_value = ft.TextField(value=checkbox.label, width=300)
        save_button = ft.IconButton(icon=ft.icons.SAVE, on_click=lambda e: save_clicked(e, checkbox, new_value, item))
        cancel_button = ft.IconButton(icon=ft.icons.CANCEL, on_click=lambda e: cancel_clicked(e, checkbox, item))
        item.controls = [new_value, save_button, cancel_button]  # Actualizar controles para edición
        page.update()

    # Función para guardar los cambios realizados en un ítem
    def save_clicked(e, checkbox, new_value, item):
        checkbox.label = new_value.value  # Actualizar la etiqueta del checkbox
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, checkbox.label))
        item.controls = [checkbox, edit_button, delete_button]  # Actualizar controles
        page.update()

    # Función para cancelar la edición de un ítem
    def cancel_clicked(e, checkbox, item):
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, checkbox.label))
        item.controls = [checkbox, edit_button, delete_button]  # Restaurar controles originales
        page.update()

    # Función para eliminar un ítem
    def delete_clicked(e, item, text):
        shopping_list.remove(text)  # Eliminar de la lista de compras
        page.controls.remove(item)  # Remover el ítem de la página
        page.update()

    # Función para actualizar los botones (Agregar)
    def update_buttons():
        button_row.controls = [
            new_task,
            ft.ElevatedButton("Agregar", on_click=add_clicked),  # Botón para agregar ítems
        ]
        page.update()

    # Campo de entrada para nuevo ítem
    new_task = ft.TextField(hint_text="¿Qué necesitas comprar?", width=250)
    
    # Crear una cabecera con el logo y el texto de bienvenida
    header_text = ft.Text("Bienvenidos a la App de Lista de Compras", size=20, weight=ft.FontWeight.BOLD)

    # Organizar la cabecera en una columna
    header = ft.Column([logo, header_text], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Definir una fila para los botones
    button_row = ft.Row([new_task, ft.ElevatedButton("Agregar", on_click=add_clicked)])  # Botón para agregar ítems

    # Añadir elementos a la aplicación
    page.add(
        header,  # Mostrar la cabecera primero
        ft.Divider(height=20),  # Agregar un divisor para separar el logo de la sección
        button_row  # Fila de botones
    )

ft.app(target=main)
