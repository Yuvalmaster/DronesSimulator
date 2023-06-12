class Predator:
    
    __slots__ = ['ID', 'Max_Speed', 'pos', 'state']         # Limits the number of attributes of this drone to this list
    def __init__(self, ID, Max_Speed, pos = (1,1), state = 'Landed'):
        
        #ValueErrors
        if (type(ID) != int or ID < 1 or ID > 9 ):          # Check Valid ID
            raise ValueError("ID is set between 1-9")
        
        if type(pos) == tuple:                              # Check Valid Coordinates
            if (len(pos) != 2   or 
                pos[0]   <  1   or pos[1] < 1   or
                pos[0]   >  100 or pos[1] > 100   ):
                    
                raise ValueError("Invalid Coordinates. Please insert (X,Y) Coordinates with values of 0-100 for each axis")
        
        # Builder 
        self.ID         = ID                    # Unique ID: Value 1-9
        self.Max_Speed  = Max_Speed             # Max Speed: [Squares/Sec]
        self.state      = state                 # Drone's State
        self.pos        = pos                   # Drone's position    
    
    def __repr__(self):
        return "Drone Type: Predator"                                        + '\n' +\
               "ID: "               + str(self.ID)                           + '\n' +\
               "Max Speed: "        + str(self.Max_Speed) + " [Squares/Sec]" + '\n' +\
               "Current Position: " + str(self.pos)       + " [X,Y]"         + '\n' +\
               "State: "            + str(self.state)                      
    
    
####### Functions #######    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------- #  
   
# This function returns the current location of a drone with his ID
    def Location(self):
        
        print(f"Drone No. {self.ID} current location: {self.pos}")
        return self.pos

    
# This function send an action to the drone.    L = Land, T = Takeoff, A = Action    
    def Action(self, action):                   # 00 - LL ; 01 - TL ; 10 - TT ; 11 - LT ; 20 - LA ; 21 - AA ; 22 - TA 
        
        # Incorrect action errors
        if (action       != 'Takeoff' and 
            action       != 'Land'    and 
            type(action) != tuple        ):
           
            raise TypeError("Invalid Action. Valid actions are 'Land', 'Takeoff', GoTo - (desired location - (X, Y))")
            
        # Takeoff
        if action == 'Takeoff':
            
            if self.state == 'Flying':
                print(f'Drone No. {self.ID} is already in the air')
                return '10'     # Action state as aformationed: Takeoff -> Takeoff
            else:
                self.state = 'Flying'
                print(f'Drone No. {self.ID} is taking off')
                return '11'
            
        # Land
        elif action =='Land':
            
            if self.state == "Landed":
                print(f'Drone No. {self.ID} is already on the ground')
                return '00'
            else:                   
                self.state = 'Landed'
                print('Landing')
                return '01'
               
        # GoTo
        elif type(action) == tuple:
            if (len(action) != 2   or 
                action[0]   <  1   or action[1] < 1   or
                action[0]   >  100 or action[1] > 100   ):
                    
                raise ValueError("Invalid Coordinates. Please insert (X,Y) Coordinates with values of 0-100 for each axis")
      
            else:
                if self.state == "Landed":
                    print(f"Drone No. {self.ID} is landed. Please Takeoff first")
                    return '20'
                
                elif self.pos == action:
                    print(f"Drone No. {self.ID} is already in destination. Please change coordinates")
                    return '22'
                
                else:                      
                    [x_steps, y_steps] = [action[0] - self.pos[0], action[1] - self.pos[1]]
                    self.pos = action
                    print(f"Drone No. {self.ID} Arrived destination {action}")
                    return '21', [x_steps , y_steps]