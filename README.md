# Drone Farm Simulator 🎮 🛰 🚁
## Project Overview
The Drone Farm Simulator is a project aimed at developing a simple drone farm simulation using the tkinter GUI toolkit. 
The simulator provides a graphical interface for users to interact with and control different types of drones. 
It includes functionalities such as obtaining drone location, sending drones to specific coordinates, checking drone status, and more.
The simulation supports two types of drones: Predator and Wolf. The Wolf drone has an additional capability of carrying a payload of up to 2kg.

## Repository Structure
The repository is organized to facilitate easy access to the project resources and implementation. Here's an overview of the main components:

- **main.py**: This is the main script that serves as the entry point for the project. It contains the code for setting up the GUI, creating the drone farm simulation environment, and handling user interactions.

- **Predator.py**: This file contains the class definition for the Predator drone. It includes methods for controlling the Predator drone's movement, obtaining its location, and checking its status. The Predator drone is a type of drone in the simulation.

- **ResizingCanvas.py**: This file provides a helper function for creating a tkinter canvas with an auto aspect ratio. It ensures that the simulation environment is displayed properly on different screen sizes.

- **Wolf.py**: This file contains the class definition for the Wolf drone. It inherits from the Predator class and adds the functionality of carrying a payload of up to 2kg.

- requirements.txt: This file lists the required dependencies and their versions for running the project. 
It is recommended to set up a conda virtual environment and install the dependencies using ```conda install --file requirements.txt```
