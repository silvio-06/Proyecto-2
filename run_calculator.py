#!/usr/bin/env python3
"""
Launcher script for the Elegant Calculator
"""

from calculator import ElegantCalculator

def main():
    print("Iniciando Calculadora Elegante...")
    calculator = ElegantCalculator()
    calculator.run()

if __name__ == "__main__":
    main()