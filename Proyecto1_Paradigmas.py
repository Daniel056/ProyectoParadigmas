#Daniel Zamora García
#Esteban Montero Fonseca
#Jefferson Moreno Zuñiga

#Proyecto #1 de Paradigmas de Programación

#interfaz
from tkinter import *
from tkinter.filedialog import askopenfilename

#metodo para agregar a los botones del menu
def donothing():
    filewin = TopLevel(root)
    button = Button(filewin, text="Do nothin button")
    button.pack()

#abre el explorador de archivos
def openFile():
    filename = askopenfilename() 
    print (filename)

#pantalla principal
root = Tk()
root.title("IDLE")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry('%sx%s' % (screen_width, screen_height))

#barra de menu
menubar= Menu(root)

#opciones del file menu
filemenu= Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

#opciones del edit menu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)

#opciones del helpmenu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()
