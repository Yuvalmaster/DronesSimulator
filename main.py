"""
@author: Yuval Argoetti
Sep-2022
"""

####### Assumptions #######  
'''
1. Grid coordinates are set from x,y=(1,1) to x,y= (100,100) - ((1,1) is located on top-left of the canvas, (100,100) is located on bottom-right of the canvas)
2. The Drones parameters are randomly generated (starting location, type, max speed, payload). Can be set otherwise by changing the fields under 'Generate Drones' title.
3. All drones start on the ground
4. No collision between drones - drones can reach the same coordinate at the same time (assuming height delta between drones which is not present in this build)
5. More than one drone can be landed in the same spot.
6. Max payload is limited for Wolf Drone: 2[kg] (2000[grams])
7. Wolf Drones' max speed are affected by payload according to the following formula: Max_Speed - 0.5*Max_Speed*(Payload/Max_Payload)
hence, at max payload the speed is half of the maximum speed.
8. Predator drones cannot have payload
9. One drone can be fly at a time.
10. The commands a drone can recieve are:
    i.   'Takeoff'  - Taking off the ground
    ii.  'Land'     - Landing on the ground
    iii. 'location' - output the drone's coordinates
    iv.  'Goto'     - Send the drone to set location
11. Rules:
    i.    Drone ID can be set from 1 to 9 only
    ii.   Actions input must be one of the aforementioned (assumption 10)
    iii.  Drone cannot get only one of X or Y coordinate
    iv.   Drone cannot fly when is on the ground - require 'takeoff' command first
    v.    'Land' command while flying will land the drone at the destination coordinates

'''
'PACKAGES'
import tkinter as tk
import random
import time

from Predator import*
from Wolf import*
from ResizingCanvas import*

        
'Generate Drones'
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #     
NumDrones   = 10
Max_speed   = 30
Grid_size   = 100                                                          # The number of rows/cols 
Max_Payload = 2000                                                         # Limit weight Wolf Drone
Drone_list  = list()
ID_list     = list()

for i in range(1, NumDrones):                                              # Create Drones 1-9
    if random.randrange(0,2) == 1:      
        Drone_list.append(Predator(i ,                                     # ID
                                 random.randrange(1,Max_speed),            # Max Speed
                                 (random.randrange(1,Grid_size+1),         # Starting position
                                  random.randrange(1,Grid_size+1))))       
    else:
        Drone_list.append(Wolf(i,                                          # ID
                                    random.randrange(1,Max_speed),         # Max Speed
                                    random.randrange(0,Max_Payload+1),     # Payload
                                    (random.randrange(1,Grid_size+1),      # Starting position
                                     random.randrange(1,Grid_size+1))))    
    
    ID_list.append(Drone_list[i-1].ID) 



'Create GUI'
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #  

# This section creates the GUI window
window = tk.Tk()
window.title("Drone Control")
initial_board_width = 1000 ; initial_board_height = initial_board_width
window.configure(bg = "#fdf7e2")
window.geometry(f'{initial_board_width}x{initial_board_height}')
   
# Create prompter        
Prompter = tk.Entry(window, borderwidth = 5, font = ("default", 20 ))
Prompter.pack(fill = "both", side = 'bottom')

# Create frame for inputs        
buttons_frame = tk.Frame(window)
buttons_frame.pack(side = 'left')

# Create Board with 100x100 grid
Board = tk.Canvas(window, width = initial_board_height, 
                          height = initial_board_height, bg = "#c9def2")
Board.pack(fill = "both", expand = "yes")

# Create Dynamic scaling Board based on Board.
Resize_Board = ResizingCanvas(Board, width  = initial_board_width, 
                                     height = initial_board_height, bg = "#c9def2", highlightthickness=0)
Resize_Board.pack(fill = "both", expand = "yes")


'Create objects on board'
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
Drone_radius    = initial_board_width/(Grid_size*2) # Scale divided by the sum of rows*2 (fit the center of the drone inside the grid)
Scale_X = initial_board_width/Grid_size             # Scale divided by the sum of rows
Scale_Y = initial_board_height/Grid_size            # Scale divided by the sum of columns
Drone_position  = list()
Drone_numbers   = list()

# Plot Grid lines
for i in range(Grid_size+1):    
    # Create horizontal and vertical lines of the grid
    Resize_Board.create_line(i*Scale_X, 0,
                             i*Scale_X, initial_board_height, fill="#6f8fcc")
    Resize_Board.create_line(0, i*Scale_Y, 
                             initial_board_width, i*Scale_Y, fill="#6f8fcc")
# Plot drones on board
for i in range(len(Drone_list)):   
    # Position Drones on the grid
    Drone_position.append(Resize_Board.create_oval(Scale_X*(Drone_list[i].pos[0]) - Drone_radius*2,
                                                   Scale_Y*(Drone_list[i].pos[1]) - Drone_radius*2,
                                                   Scale_X*(Drone_list[i].pos[0]),
                                                   Scale_Y*(Drone_list[i].pos[1]),
                                                   fill="red", outline="black", width=2))
    
    # Position No. of drones on the grid
    Drone_numbers.append(Resize_Board.create_text(Scale_X*Drone_list[i].pos[0] - Drone_radius,
                                                  Scale_Y*Drone_list[i].pos[1] - Scale_Y - Drone_radius, 
                                                  font=("Comic Sans MS", 10, 'bold'), text=f"{Drone_list[i].ID}"))
    
    if Drone_list[i].pos[1] == 1:                   # If Y coordinate is 1, then the drone ID will be shown below instead of above.
            Resize_Board.move(Drone_numbers[i], 0, 2*Scale_Y) 


'Functions'
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

# This function checks the ID of a drone and prompt an error when is not valid ID
def Check_ID(Drone_ID):    
    if (not all(char.isdigit() for char in Drone_ID)):
        Prompter.delete(0,'end') ; Prompter.insert(0, 'Error: Invalid ID. ID must be a number')
        raise ValueError("Error: Invalid ID. ID must be a number")
    
    elif (int(Drone_ID) not in ID_list):
        Prompter.delete(0,'end') ; Prompter.insert(0, 'Error: Invalid ID. Please choose one of the drones on board')
        raise ValueError("Error: Invalid ID")
    
    return int(Drone_ID)

# This function gets the location of chosen drone
def Choose_Drone_location():
    
    Drone_ID = Check_ID(ID_insert.get())
    
    coordinates = Drone_list[Drone_ID - 1].Location()  
    Prompter.delete(0,'end') ; Prompter.insert(0, f"Drone No. {Drone_ID} current location: {coordinates}")    

# This function commands 'Takeoff' to a chosen drone
def Choose_Drone_takeoff():
    
    Drone_ID = Check_ID(ID_insert.get())
    
    res = Drone_list[Drone_ID - 1].Action('Takeoff')
    
    if res == '10':
        Prompter.delete(0,'end') ; Prompter.insert(0, f"Drone No. {Drone_ID} is already in the air")
    
    elif res == '11':
        Prompter.delete(0,'end') ; Prompter.insert(0, f"Drone No. {Drone_ID} is taking off")
        Resize_Board.itemconfig(Drone_position[Drone_ID - 1], fill = 'green')
        
# This function commands 'Land' to a chosen drone    
def Choose_Drone_landing():
    
    Drone_ID = Check_ID(ID_insert.get())
        
    res = Drone_list[Drone_ID - 1].Action('Land')
    
    if res == '00':
        Prompter.delete(0,'end') ; Prompter.insert(0, f'Drone No. {Drone_ID} is already on the ground')
    
    elif res == '01':
        Prompter.delete(0,'end') ; Prompter.insert(0, f"Drone No. {Drone_ID} is landing")
        Resize_Board.itemconfig(Drone_position[Drone_ID - 1], fill = 'red')

# This function gets the status of a chosen drone: Type, Max speed, Actual Speed, Payload, State      
def Choose_Drone_status():
    
    Drone_ID = Check_ID(ID_insert.get())
        
    Drone = Drone_list[Drone_ID - 1]
    
    Type_read.config(state          = "normal")   
    Speed_read.config(state         = "normal")
    Payload_read.config(state       = "normal")
    Statusof_read.config(state      = "normal")
    Actual_Speed_read.config(state  = "normal") 
    
    Prompter.delete(0,                   'end')   
    Type_read.delete(0,                  'end')
    Speed_read.delete(0,                 'end')
    Payload_read.delete(0,               'end')
    Statusof_read.delete(0,              'end')
    Actual_Speed_read.delete(0,          'end')

    if hasattr(Drone, 'Payload'):
        Type = 'Wolf'
        
        Payload_read.insert(0       ,f"{Drone.Payload} [grams]")
        Actual_Speed_read.insert(0  ,f"{round(Drone.Max_Speed - 0.5*Drone.Max_Speed*(Drone.Payload/Max_Payload),2)} [Squares/Sec]")
    else:
        Type = 'Predator'

        Payload_read.insert(0       ,"N/A")
        Actual_Speed_read.insert(0  ,"N/A")

    Statusof_read.insert(0          ,f"Drone No. {Drone.ID}")
    Speed_read.insert(0             ,f"{Drone.Max_Speed} [Squares/Sec]")
    Type_read.insert(0              ,f"{Type}")
    Prompter.insert(0               , f"Drone No. {Drone_ID} is {Drone.state}")

    Actual_Speed_read.config(state  = "readonly")    
    Statusof_read.config(state      = "readonly")
    Payload_read.config(state       = "readonly")
    Speed_read.config(state         = "readonly")
    Type_read.config(state          = "readonly")

# This Function commands 'GoTo' to a chosen Drone   
def Choose_Drone_GoTo():
    
    Drone_ID = Check_ID(ID_insert.get())

    # Check if X or Y coordinates are missing    
    if len(X_insert.get()) == 0 or len(Y_insert.get()) == 0:
        Prompter.delete(0,'end') ; Prompter.insert(0, 'Error: Please insert X and Y Coordinates')
        return
             
    x_coor = int(X_insert.get())                            # X coordinates: from X_insert Entry field
    y_coor = int(Y_insert.get())                            # Y coordinates: from Y_insert Entry field
    prev_coordinations = Drone_list[Drone_ID - 1].pos
    res = Drone_list[Drone_ID - 1].Action((x_coor,y_coor))
    
    
    # Choose the following command based on output recieves from the Action function
    if type(res) == str:
        
        if res =='20':
            Prompter.delete(0,'end') ; Prompter.insert(0, f"Drone No. {Drone_ID} is landed. Please Takeoff first")        
        elif res == '22':
            Prompter.delete(0,'end') ; Prompter.insert(0, f"Drone No. {Drone_ID} already recieved these coordination. Please change coordinates")
            
    elif res[0] == '21':
        
        [x_steps, y_steps] = res[1]
        Prompter.delete(0,'end') ; Prompter.insert(0, f"Drone No. {Drone_ID} fly to destination")
        
        # Fix number position based on destination coordinates
        if prev_coordinations[1] != 1 and y_coor == 1:      # If Y coordinate == 1, then the drone ID will be shown below instead of above.
            Resize_Board.move(Drone_numbers[Drone_ID - 1], 0, 2*Scale_Y)        
        elif prev_coordinations[1] == 1 and y_coor != 1:   
            Resize_Board.move(Drone_numbers[Drone_ID - 1], 0, -2*Scale_Y) 
            
        # Initiate Movement 
        Drone_list[Drone_ID - 1].pos = prev_coordinations   # Initiate movement from starting point - dynamically get location during moving
        animate_movement(window,Resize_Board,x_steps,y_steps,
                         Drone_position[Drone_ID - 1], 
                         Drone_numbers[Drone_ID - 1], 
                         Drone_list[Drone_ID - 1],
                         (x_coor,y_coor))
        
# This function animates drone movement on board
def animate_movement(window, Resize_Board, x_steps, y_steps, Drone_fig, Drone_number, Drone, loc):
    
    GoTo_button.config(state = "disabled")  
    Resize_Board.itemconfig(Drone_fig, outline = "#ce4619")                     # Mark the moving drone with Orange circle
    
    if hasattr(Drone, 'Payload'):                                               # Change the Actual speed of a Wolf drone based on a function below
        speed = Drone.Max_Speed - 0.5*Drone.Max_Speed*(Drone.Payload/Max_Payload)
    else:     
        speed = Drone.Max_Speed
        
    # Move the drone on X axis, then on Y axis; based on the direction
    for i in range(abs(x_steps)):
        if x_steps < 0:
            Scale_X = -Resize_Board.width/Grid_size                              # Scale divided by the sum of rows
            x_move = Drone.pos[0]-1
            
        else:    
            Scale_X = Resize_Board.width/Grid_size                              # Scale divided by the sum of rows
            x_move = Drone.pos[0]+1
            
        update_location(Scale_X, 0, (x_move, Drone.pos[1]), 
                        speed, window, Resize_Board, Drone_fig, Drone_number, Drone)

            
    for j in range(abs(y_steps)):
        if y_steps < 0:
            Scale_Y = -Resize_Board.height/Grid_size                             # Scale divided by the sum of columns   
            y_move = Drone.pos[1]-1

        else:
            Scale_Y = Resize_Board.height/Grid_size                             # Scale divided by the sum of columns
            y_move = Drone.pos[1]+1
            
        update_location(0, Scale_Y, (Drone.pos[0], y_move), 
                        speed, window, Resize_Board, Drone_fig, Drone_number, Drone)

    Prompter.delete(0,'end') ; Prompter.insert(0, f"Drone No. {Drone.ID} Arrived destination {loc}")
    Resize_Board.itemconfig(Drone_fig, outline = "black")
    
    GoTo_button.config(state = "normal")

# This function update the location of objects on the board
def update_location(Scale_X, Scale_Y, coor, speed, window, Resize_Board, Drone_fig, Drone_number, Drone):
    
    Resize_Board.move(Drone_fig,    Scale_X, Scale_Y)
    Resize_Board.move(Drone_number, Scale_X, Scale_Y)
    window.update()
    time.sleep(1/speed)
    Drone.pos = coor


'GUI inputs'  
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
            
# Buttons layout
Takeoff_button    = tk.Button(buttons_frame, text = "Takeoff",    bg = "green" ,  fg = "white", command = Choose_Drone_takeoff )
Land_button       = tk.Button(buttons_frame, text = "Land",       bg = "red" ,    fg = "white", command = Choose_Drone_landing )
GoTo_button       = tk.Button(buttons_frame, text = "GoTo",                                     command = Choose_Drone_GoTo    )
location_button   = tk.Button(buttons_frame, text = "Get Location",                             command = Choose_Drone_location)
Status_button     = tk.Button(buttons_frame, text = "Status",                                   command = Choose_Drone_status  )

Takeoff_button.grid(    row = 1, column = 1, sticky = "we")
Land_button.grid(       row = 2, column = 1, sticky = "we")
GoTo_button.grid(       row = 5, column = 1, sticky = "we")
location_button.grid(   row = 6, column = 1, sticky = "we")
Status_button.grid(     row = 7, column = 1, sticky = "we")

# Entry layout
ID_insert         = tk.Entry(buttons_frame)
X_insert          = tk.Entry(buttons_frame)
Y_insert          = tk.Entry(buttons_frame)
Statusof_read     = tk.Entry(buttons_frame)
Speed_read        = tk.Entry(buttons_frame)
Type_read         = tk.Entry(buttons_frame)
Payload_read      = tk.Entry(buttons_frame)
Actual_Speed_read = tk.Entry(buttons_frame)

Statusof_read.config(state     = 'readonly') # Create an Entry Field for read only.
Actual_Speed_read.config(state = 'readonly') # Create an Entry Field for read only.
Speed_read.config(state        = "readonly") # Create an Entry Field for read only.
Payload_read.config(state      = 'readonly') # Create an Entry Field for read only.
Type_read.config(state         = 'readonly') # Create an Entry Field for read only.

ID_insert.grid(         row = 0,  column = 1, sticky = 'E')
X_insert.grid(          row = 3,  column = 1, sticky = 'E')
Y_insert.grid(          row = 4,  column = 1, sticky = 'E')                
Statusof_read.grid(     row = 8,  column = 1, sticky = 'E') 
Speed_read.grid(        row = 9,  column = 1, sticky = 'E') 
Type_read.grid(         row = 10, column = 1, sticky = 'E')    
Payload_read.grid(      row = 11, column = 1, sticky = 'E')  
Actual_Speed_read.grid( row = 12, column = 1, sticky = 'E')  

# Labels layout
droneidlabel       = tk.Label(buttons_frame, text= "Drone No.").grid(            row = 0,  column = 0)
X_label            = tk.Label(buttons_frame, text= "X").grid(                    row = 3,  column = 0)
Y_label            = tk.Label(buttons_frame, text= "Y").grid(                    row = 4,  column = 0)
statusof_label     = tk.Label(buttons_frame, text= "Status Of").grid(            row = 8,  column = 0)
Max_Speed_label    = tk.Label(buttons_frame, text= "Max Speed").grid(            row = 9,  column = 0)
Type_label         = tk.Label(buttons_frame, text= "Type").grid(                 row = 10, column = 0)
Payload_label      = tk.Label(buttons_frame, text= "Payload").grid(              row = 11, column = 0)
Actual_Speed_label = tk.Label(buttons_frame, text= "Speed \n with payload").grid(row = 12, column = 0)


'Run Application'
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
Resize_Board.addtag_all("all")
window.mainloop()






  
