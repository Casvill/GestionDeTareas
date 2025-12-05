## Gestor de Tareas con Heap y AVL — Proyecto Final ADA 1

Este proyecto implementa un sistema de gestión de tareas utilizando dos estructuras fundamentales:

* Heap mínimo (para gestionar tareas por prioridad)

* Árbol AVL (para mantener las tareas balanceadas y permitir búsquedas eficientes)

Además, incluye una interfaz gráfica (GUI) desarrollada en Tkinter, con visualización en vivo del Heap y el AVL mediante Matplotlib.

### Cómo ejecutar el programa:
1. Clonar el repositorio:   
```git clone https://github.com/Casvill/GestionDeTareas.git```   
Entrar al proyecto:   
```cd GestionDeTareas```   
<br>
2. Crear y activar un entorno virtual:   
```python -m venv venv```   
```venv\Scripts\activate```   
<br>
3. Instalar dependencias:   
El proyecto utiliza unas pocas librerías externas. Instálalas con:   
```pip install -r requirements.txt```   
<br>
4. Ejecutar el programa:   
Desde la carpeta raíz del proyecto:   
```python __main__.py```<br>   
o en algunos sistemas:   
```python3 __main__.py```   
   
La interfaz gráfica se abrirá automáticamente.   


#### Descripción breve  del sistema: 
La interfaz contiene 2 paneles: Tabla y Visual.
* Panel Tabla: 
En el panel Tabla se verá una lista con las tareas pendientes.
Cada tarea en la lista de tareas se resalta con un solor según su prioridad:   
🔴 Alta   
🟡 Media   
🟢 Baja   
<br>   
* Panel Visual:   
Se divide en dos, la parte de arriba muestra de manera gráfica  el HEAP como árbol y la parte de abajo muestra de manera gráfica el árbol AVL.
Cada nodo se representa con un círulo y un número dentro del círculo que representa su ID, y cada círculo tiene un color que representa su prioridad así:   
🔴 Alta   
🟡 Media   
🟢 Baja   
<br>
   
📁 Estructura del proyecto:   
Proyecto:
│── __main__.py        # Punto de entrada   
│── GUI.py             # Interfaz gráfica completa   
├── Heap.py            # Implementación del heap   
├── AVL.py             # Implementación del AVL   
├── Task.py            # Clase que representa una tarea del sistema   
│── TaskManager.py     # Lógica de integración   
│── requirements.txt   # Archivo de dependencias   
│── README.md          # Este archivo   
<br>   

#### Autor:
Daniel Castillo Villamarín   
Universidad del Valle   
2025   