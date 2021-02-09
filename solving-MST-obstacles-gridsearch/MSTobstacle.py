import tkinter as tk
import MST
import time

obstacle = []
draw = []

def myfunction(event):
    x, y = event.x, event.y
    draw.append([x,y])
    obstacle.append([x/10,(1000-y)/10])
    canvas.create_oval(x-2, y-2, x+2,y+2, fill="grey", outline="grey", width=1)
    if canvas.old_coords:
        x1, y1 = canvas.old_coords
        canvas.create_line(x, y, x1, y1,fill="grey",width = 3)
    canvas.old_coords = x, y

def polygon(event):
    if(len(obstacle)>1):
        canvas.create_line(draw[0][0], draw[0][1], draw[len(draw)-1][0], draw[len(draw)-1][1],fill="grey",width = 3)
    root.after(500,exit)
    
    

# root.bind('<3>', polygon)
def exit():
    root.destroy()
    MST.GeneticAlgorithm(100,100,obstacle)
    



root = tk.Tk()
points = MST.getPoints()
canvas = tk.Canvas(root, width=1000, height=1000)
canvas.pack()
canvas.old_coords = None
for x,y in points:
    canvas.create_oval((10*x)-5, 1000-(10*y)-5, (10*x)+5,1000-(10*y)+5, fill="blue", outline="blue", width=1)

root.bind('<Button-1>', myfunction)
root.bind('<Button-3>', polygon)




root.mainloop()