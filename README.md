# Calculadora Elegante en Python 🧮

Una calculadora moderna y elegante con interfaz gráfica desarrollada en Python usando tkinter.

## Características

✨ **Diseño Moderno**: Tema oscuro elegante con colores naranjas para operadores
🔢 **Operaciones Básicas**: Suma, resta, multiplicación y división
⌨️ **Soporte de Teclado**: Puedes usar tanto el mouse como el teclado
🎨 **Interfaz Intuitiva**: Botones grandes con efectos hover
📱 **Pantalla Dual**: Muestra la operación anterior y el resultado actual
🧹 **Funciones Avanzadas**: Borrar, retroceso, cambio de signo, porcentaje

## Instalación

No requiere instalación de dependencias adicionales, solo Python 3 con tkinter (incluido por defecto).

## Uso

### Ejecutar la calculadora:

```bash
python calculator.py
```

o usando el launcher:

```bash
python run_calculator.py
```

### Controles del Teclado:

- **Números (0-9)**: Ingreso de números
- **Operadores (+, -, *, /)**: Operaciones matemáticas
- **Enter o =**: Calcular resultado
- **C**: Limpiar todo
- **Backspace**: Borrar último dígito
- **.**: Punto decimal
- **%**: Porcentaje

### Controles de la Interfaz:

- **C**: Limpiar toda la calculadora
- **⌫**: Borrar el último dígito ingresado
- **±**: Cambiar signo del número actual
- **%**: Convertir a porcentaje
- **÷, ×, -, +**: Operaciones matemáticas
- **=**: Calcular resultado

## Funcionalidades

### Operaciones Básicas
- Suma, resta, multiplicación y división
- Manejo de decimales
- Operaciones encadenadas

### Funciones Especiales
- **Cambio de signo (±)**: Convierte números positivos en negativos y viceversa
- **Porcentaje (%)**: Divide el número actual entre 100
- **Borrado inteligente**: Retroceso dígito por dígito

### Características de la Interfaz
- **Tema oscuro moderno**: Fácil para los ojos
- **Efectos hover**: Los botones cambian de color al pasar el mouse
- **Pantalla dual**: Muestra la operación en curso y el resultado
- **Responsivo**: Se adapta bien a diferentes tamaños

## Arquitectura

El código está organizado en una clase principal `ElegantCalculator` que maneja:

- **Interfaz gráfica**: Creación y gestión de la UI con tkinter
- **Lógica de cálculo**: Procesamiento de operaciones matemáticas
- **Eventos**: Manejo de clics de botones y teclas del teclado
- **Estado**: Gestión del estado de la calculadora (números, operadores, etc.)

## Requisitos del Sistema

- Python 3.6 o superior
- tkinter (incluido con Python por defecto)
- Sistema operativo: Windows, macOS, o Linux con interfaz gráfica

¡Disfruta usando tu nueva calculadora elegante! 🎉 
