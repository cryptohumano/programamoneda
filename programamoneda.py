import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime


def evaluar_aplicabilidad_moneda():
    criterios_relevancia = ['Eficiencia en los pagos', 'Reducción de costos', 'Acceso a nuevas oportunidades de mercado']
    investigacion_aceptacion = ['Proveedores', 'Clientes', 'Socios comerciales']
    analisis_estabilidad = ['Volatilidad histórica', 'Política monetaria', 'Liquidez']

    pesos = {
        'Eficiencia en los pagos': 0.4,
        'Reducción de costos': 0.3,
        'Acceso a nuevas oportunidades de mercado': 0.3
    }

    resultados = {
        'Eficiencia en los pagos': 0,
        'Reducción de costos': 0,
        'Acceso a nuevas oportunidades de mercado': 0
    }

    print("Evaluación de aplicabilidad de una moneda a un negocio\n")

    # Evaluación de criterios de relevancia
    print("Criterios de relevancia:")
    for criterio in criterios_relevancia:
        respuesta = input(f"¿Cumple {criterio}? (s/n): ")
        if respuesta.lower() == 's':
            resultados[criterio] = 1

    # Evaluación de investigación de aceptación
    print("\nInvestigación de aceptación:")
    for investigacion in investigacion_aceptacion:
        respuesta = input(f"¿Hay aceptación por parte de {investigacion.lower()}? (s/n): ")
        if respuesta.lower() == 's':
            resultados[investigacion] = 1

    # Evaluación de análisis de estabilidad
    print("\nAnálisis de estabilidad:")
    for analisis in analisis_estabilidad:
        respuesta = input(f"¿Cumple con la estabilidad en términos de {analisis.lower()}? (s/n): ")
        if respuesta.lower() == 's':
            resultados[analisis] = 1

    # Cálculo de puntaje total
    puntaje_total = sum(resultados[criterio] * pesos[criterio] for criterio in criterios_relevancia)

    print("\n--- Resultados ---")
    for criterio in criterios_relevancia:
        print(f"{criterio}: {'Cumple' if resultados[criterio] == 1 else 'No cumple'}")

    print(f"\nPuntaje total: {puntaje_total}")

    if puntaje_total >= 0.5:
        print("La moneda es potencialmente aplicable al negocio.")
    else:
        print("La moneda no es adecuada para el negocio.")


def mostrar_pantalla_evaluacion(criterios_relevancia):
    def calcular_puntaje():
        resultados = {}
        for criterio in criterios_relevancia:
            resultados[criterio] = criterio_scale[criterio].get()

        puntaje_total = sum(resultados[criterio] * pesos[criterio] for criterio in criterios_relevancia)
        embajador = embajador_entry.get()
        telefono_prospecto = telefono_entry.get()
        nombre_prospecto = nombre_entry.get()
        correo_prospecto = correo_entry.get()
        direccion = direccion_text.get(1.0, tk.END)

        guardar_evaluacion(resultados, puntaje_total, embajador, telefono_prospecto, nombre_prospecto, correo_prospecto, direccion)

        mostrar_resultado(puntaje_total)

    evaluacion_window = tk.Toplevel(root)
    evaluacion_window.title("Evaluación")
    evaluacion_window.geometry("400x400")

    titulo_label = ttk.Label(evaluacion_window, text="Evaluación de Relevancia")
    titulo_label.pack(pady=10)

    frame = ttk.Frame(evaluacion_window)
    frame.pack()

    scroll = tk.Scrollbar(frame)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    evaluacion_canvas = tk.Canvas(frame, yscrollcommand=scroll.set)
    evaluacion_canvas.pack(side=tk.LEFT, fill=tk.BOTH)

    scroll.config(command=evaluacion_canvas.yview)

    evaluacion_canvas.bind('<Configure>', lambda e: evaluacion_canvas.configure(scrollregion=evaluacion_canvas.bbox('all')))

    evaluacion_frame = ttk.Frame(evaluacion_canvas)
    evaluacion_canvas.create_window((0, 0), window=evaluacion_frame, anchor='nw')

    criterio_scale = {}
    for i, criterio in enumerate(criterios_relevancia):
        criterio_label = ttk.Label(evaluacion_frame, text=criterio)
        criterio_label.pack()
        criterio_scale[criterio] = tk.Scale(evaluacion_frame, from_=0, to=10, orient=tk.HORIZONTAL)
        criterio_scale[criterio].pack(pady=5)

    calcular_button = ttk.Button(evaluacion_window, text="Calcular Puntaje", command=calcular_puntaje)
    calcular_button.pack(pady=10)

def guardar_evaluacion(resultados, puntaje_total, embajador, telefono_prospecto, nombre_prospecto, correo_prospecto, direccion):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    evaluacion = [timestamp, embajador, telefono_prospecto, nombre_prospecto, correo_prospecto, direccion, puntaje_total]
    with open("evaluaciones.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(evaluacion)

    messagebox.showinfo("Guardado Exitoso", "La evaluación ha sido guardada exitosamente.")

def mostrar_resultado(puntaje_total):
    if puntaje_total >= 0.5:
        messagebox.showinfo("Resultado de Evaluación", "La moneda es potencialmente aplicable al negocio.")
    else:
        messagebox.showinfo("Resultado de Evaluación", "La moneda no es adecuada para el negocio.")

def mostrar_historial_evaluaciones():
    historial_window = tk.Toplevel(root)
    historial_window.title("Historial de Evaluaciones")
    historial_window.geometry("800x400")

    tabla = ttk.Treeview(historial_window)
    tabla["columns"] = ("Timestamp", "Embajador", "Teléfono", "Nombre", "Correo", "Dirección", "Puntaje")
    tabla.column("#0", width=0, stretch="NO")
    tabla.column("Timestamp", width=150)
    tabla.column("Embajador", width=100)
    tabla.column("Teléfono", width=100)
    tabla.column("Nombre", width=150)
    tabla.column("Correo", width=150)
    tabla.column("Dirección", width=200)
    tabla.column("Puntaje", width=100)

    tabla.heading("#0", text="")
    tabla.heading("Timestamp", text="Fecha y Hora")
    tabla.heading("Embajador", text="Embajador")
    tabla.heading("Teléfono", text="Teléfono")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Correo", text="Correo")
    tabla.heading("Dirección", text="Dirección")
    tabla.heading("Puntaje", text="Puntaje")

    try:
        with open("evaluaciones.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                tabla.insert("", tk.END, text="", values=row)
    except FileNotFoundError:
        messagebox.showinfo("Archivo no encontrado", "No se encontró el archivo de evaluaciones.")

    tabla.pack(expand=True, fill=tk.BOTH)

def main():
    global root, embajador_entry, telefono_entry, nombre_entry, correo_entry, direccion_text

    root = tk.Tk()
    root.title("Programa Moneda")
    root.geometry("400x300")

    embajador_label = ttk.Label(root, text="Nombre del Embajador:")
    embajador_label.pack()
    embajador_entry = ttk.Entry(root)
    embajador_entry.pack(pady=5)

    telefono_label = ttk.Label(root, text="Teléfono del Prospecto:")
    telefono_label.pack()
    telefono_entry = ttk.Entry(root)
    telefono_entry.pack(pady=5)

    nombre_label = ttk.Label(root, text="Nombre del Prospecto:")
    nombre_label.pack()
    nombre_entry = ttk.Entry(root)
    nombre_entry.pack(pady=5)

    correo_label = ttk.Label(root, text="Correo del Prospecto:")
    correo_label.pack()
    correo_entry = ttk.Entry(root)
    correo_entry.pack(pady=5)

    direccion_label = ttk.Label(root, text="Dirección del Prospecto:")
    direccion_label.pack()
    direccion_text = tk.Text(root, height=4, width=30)
    direccion_text.pack(pady=5)

    iniciar_button = ttk.Button(root, text="Iniciar Evaluación", command=lambda: mostrar_pantalla_evaluacion(criterios_relevancia))
    iniciar_button.pack(pady=10)

    historial_button = ttk.Button(root, text="Historial de Evaluaciones", command=mostrar_historial_evaluaciones)
    historial_button.pack()

    root.mainloop()

if __name__ == "__main__":
    criterios_relevancia = ["Eficiencia en los pagos", "Reducción de costos", "Acceso a nuevas oportunidades de mercado"]
    pesos = {"Eficiencia en los pagos": 0.4, "Reducción de costos": 0.3, "Acceso a nuevas oportunidades de mercado": 0.3}
    main()
