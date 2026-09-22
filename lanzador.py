import os
import sys
import webbrowser
import subprocess
import tkinter as tk
from tkinter import ttk

def run_python_app():
    script_path = os.path.join(os.path.dirname(__file__), "flores_amarillas.py")
    subprocess.Popen([sys.executable, script_path])

def open_web_app():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    webbrowser.open(f"file://{os.path.abspath(html_path)}")

if __name__ == "__main__":
    # Menú rápido para elegir la experiencia
    print("=" * 60)
    print("💛 FLORES AMARILLAS PARA MIMI 🐰✨")
    print("=" * 60)
    print("1. Ejecutar Programa de Escritorio en Python (Tkinter)")
    print("2. Abrir Experiencia Web Interactiva (Con Música y Cartita)")
    print("=" * 60)
    
    # Si se ejecuta sin interacción o con argumento
    if len(sys.argv) > 1:
        if sys.argv[1] == "web":
            open_web_app()
        else:
            run_python_app()
    else:
        # Por defecto abre la versión Python
        print("Iniciando aplicación de Python...")
        run_python_app()
