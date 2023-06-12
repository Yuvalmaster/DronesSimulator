import tkinter as tk
####### Dynamic GUI resize functions #######   
class ResizingCanvas(tk.Canvas):
    def __init__(self,parent,**kwargs):
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width  = self.winfo_reqwidth()

    def on_resize(self,event):                                  # determine the ratio of old width/height to new width/height
        
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width  = event.width
        self.height = event.height
       
        self.config(width = self.width, height = self.height)   # resize the canvas         
        self.scale("all",0,0,wscale,hscale)                     # rescale all the objects tagged with the "all" tag