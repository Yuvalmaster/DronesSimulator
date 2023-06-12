from Predator import*

class Wolf(Predator):                                           # Inherite from Predator
   
    __slots__ = ['ID', 'Max_Speed', 'pos', 'state', 'Payload']  # Limits the number of attributes of this drone to this list
    def __init__(self, ID, Max_Speed, Payload = 0, pos = (1,1), state = 'Landed'):
        super().__init__(ID, Max_Speed, pos, state)
   
        if Payload < 0: 
            raise ValueError("Payload cannot be a negative weight. Please insert payload between 0-2000 [grams]")
        if Payload > 2000:                                      # Limit weight
            raise ValueError("Maximum allowed payload is 2[kg] (2000[g]).")
   
        self.Payload = Payload
         
    def __repr__(self):
        return "Drone Type: Wolf"                                       + '\n' +\
               "ID: "               + str(self.ID)                           + '\n' +\
               "Max Speed: "        + str(self.Max_Speed) + " [Squares/Sec]" + '\n' +\
               "Payload: "          + str(self.Payload)   + " [grams]"       + '\n' +\
               "Current Position: " + str(self.pos)       + " [X,Y]"         + '\n' +\
               "State: "            + str(self.state)                      
