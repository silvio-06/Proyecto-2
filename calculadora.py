import flet as ft
import math


class Calculadora:
    def __init__(self):
        self.resultado = "0"
        self.operador = ""
        self.operando_anterior = ""
        self.resetear_display = False

    def main(self, page: ft.Page):
        page.title = "Calculadora Elegante"
        page.theme_mode = "dark"
        page.bgcolor = "#1a1a1a"
        page.window_width = 350
        page.window_height = 500
        page.window_resizable = False
        
        # Display de la calculadora
        self.display = ft.Text(
            value="0",
            size=36,
            weight=ft.FontWeight.BOLD,
            color="#ffffff",
            text_align=ft.TextAlign.RIGHT,
        )
        
        # Container para el display
        display_container = ft.Container(
            content=self.display,
            padding=ft.padding.all(20),
            bgcolor="#2d2d2d",
            border_radius=10,
            margin=ft.margin.only(bottom=10),
        )

        # Función para manejar clicks de números
        def numero_click(e):
            if self.resetear_display:
                self.resultado = ""
                self.resetear_display = False
            
            if self.resultado == "0":
                self.resultado = e.control.data
            else:
                self.resultado += e.control.data
            
            self.actualizar_display()

        # Función para manejar operadores
        def operador_click(e):
            if self.operador and not self.resetear_display:
                self.calcular()
            
            self.operando_anterior = self.resultado
            self.operador = e.control.data
            self.resetear_display = True

        # Función para calcular
        def calcular_click(e):
            self.calcular()

        def limpiar_click(e):
            self.resultado = "0"
            self.operador = ""
            self.operando_anterior = ""
            self.resetear_display = False
            self.actualizar_display()

        def borrar_click(e):
            if len(self.resultado) > 1:
                self.resultado = self.resultado[:-1]
            else:
                self.resultado = "0"
            self.actualizar_display()

        def punto_click(e):
            if "." not in self.resultado:
                self.resultado += "."
                self.actualizar_display()

        def porcentaje_click(e):
            try:
                valor = float(self.resultado)
                self.resultado = str(valor / 100)
                self.actualizar_display()
                self.resetear_display = True
            except:
                pass

        def cambiar_signo_click(e):
            try:
                valor = float(self.resultado)
                self.resultado = str(-valor)
                self.actualizar_display()
            except:
                pass

        # Función para crear botones
        def crear_boton(texto, on_click, bgcolor="#404040", color="#ffffff", data=None):
            return ft.ElevatedButton(
                text=texto,
                on_click=on_click,
                data=data or texto,
                style=ft.ButtonStyle(
                    bgcolor=bgcolor,
                    color=color,
                    shape=ft.RoundedRectangleBorder(radius=20),
                    elevation=3,
                ),
                width=70,
                height=70,
            )

        # Crear botones con diferentes colores
        def crear_boton_numero(texto):
            return crear_boton(texto, numero_click, "#505050", "#ffffff")

        def crear_boton_operador(texto):
            return crear_boton(texto, operador_click, "#ff9500", "#ffffff")

        def crear_boton_funcion(texto, on_click):
            return crear_boton(texto, on_click, "#a6a6a6", "#000000")

        # Layout de botones
        botones = ft.Column([
            # Fila 1: Funciones
            ft.Row([
                crear_boton_funcion("C", limpiar_click),
                crear_boton_funcion("⌫", borrar_click),
                crear_boton_funcion("%", porcentaje_click),
                crear_boton_operador("÷", operador_click),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # Fila 2: 7, 8, 9, ×
            ft.Row([
                crear_boton_numero("7"),
                crear_boton_numero("8"),
                crear_boton_numero("9"),
                crear_boton_operador("×", operador_click),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # Fila 3: 4, 5, 6, -
            ft.Row([
                crear_boton_numero("4"),
                crear_boton_numero("5"),
                crear_boton_numero("6"),
                crear_boton_operador("-", operador_click),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # Fila 4: 1, 2, 3, +
            ft.Row([
                crear_boton_numero("1"),
                crear_boton_numero("2"),
                crear_boton_numero("3"),
                crear_boton_operador("+", operador_click),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # Fila 5: +/-, 0, ., =
            ft.Row([
                crear_boton_funcion("±", cambiar_signo_click),
                crear_boton_numero("0"),
                crear_boton(".", punto_click, "#505050", "#ffffff"),
                crear_boton("=", calcular_click, "#ff9500", "#ffffff"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], spacing=10)

        # Container principal
        main_container = ft.Container(
            content=ft.Column([
                display_container,
                botones,
            ], spacing=0),
            padding=ft.padding.all(20),
            bgcolor="#1a1a1a",
            border_radius=15,
        )

        page.add(main_container)

    def actualizar_display(self):
        # Formatear el número para que se vea mejor
        try:
            if "." in self.resultado:
                valor = float(self.resultado)
                if valor == int(valor):
                    self.display.value = str(int(valor))
                else:
                    self.display.value = f"{valor:.10g}"  # Evita notación científica innecesaria
            else:
                self.display.value = self.resultado
        except:
            self.display.value = self.resultado
        
        # Truncar si es muy largo
        if len(self.display.value) > 12:
            self.display.value = self.display.value[:12]
        
        self.display.update()

    def calcular(self):
        try:
            if self.operador and self.operando_anterior:
                anterior = float(self.operando_anterior)
                actual = float(self.resultado)
                
                if self.operador == "+":
                    resultado = anterior + actual
                elif self.operador == "-":
                    resultado = anterior - actual
                elif self.operador == "×":
                    resultado = anterior * actual
                elif self.operador == "÷":
                    if actual != 0:
                        resultado = anterior / actual
                    else:
                        self.resultado = "Error"
                        self.actualizar_display()
                        return
                
                self.resultado = str(resultado)
                self.operador = ""
                self.operando_anterior = ""
                self.actualizar_display()
                self.resetear_display = True
        except:
            self.resultado = "Error"
            self.actualizar_display()
            self.resetear_display = True


def main():
    calc = Calculadora()
    ft.app(target=calc.main)


if __name__ == "__main__":
    main()