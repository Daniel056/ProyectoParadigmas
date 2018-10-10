#Daniel Zamora García
#Esteban Montero Fonseca
#Jefferson Moreno Zuñiga

#Proyecto #1 de Paradigmas de Programación

#interfaz
from tkinter import *
from tkinter import filedialog

#===============================================================Seccion de metodos=============================================================================
def donothing():
    filewin = TopLevel(root)
    button = Button(filewin, text="Do nothin button")
    button.pack()

#abre el explorador de archivos
def abrirArchivo():
   filedialog.askopenfilename(initialdir = "/",title = "Abrir archivo",filetypes = (("Text files","*.txt"),("XML files","*.xml"),("all files","*.*")))
   
#guardar el archivo como
def guardarArchivo():
    filedialog.asksaveasfilename(initialdir = "/",title = "Guardar archivo",filetypes = (("Text files","*.txt"),("XML files","*.xml"),("all files","*.*")))

#==============================================================================================================================================================


#================================================================Pantalla principal============================================================================
root = Tk()
root.title("IDE")
#screen_width = root.winfo_screenwidth()
#screen_height = root.winfo_screenheight()
#root.geometry('%sx%s' % (screen_width, screen_height))
#root.attributes('-fullscreen', True)
root.state('zoomed')
#==============================================================================================================================================================


#===================================================================Componentes================================================================================

#barra de menu
menubar= Menu(root)

#submenu archivo
filemenu= Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo", command=donothing)
filemenu.add_command(label="Abrir", command=abrirArchivo)
filemenu.add_command(label="Guardar", command=donothing)
filemenu.add_command(label="Guardar como...", command=guardarArchivo)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.destroy)
menubar.add_cascade(label="Archivo", menu=filemenu)

#submenu editar
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Deshacer", command=donothing)
editmenu.add_separator()
editmenu.add_command(label="Cortar", command=donothing)
editmenu.add_command(label="Copiar", command=donothing)
editmenu.add_command(label="Pegar", command=donothing)
editmenu.add_command(label="Seleccionar todo", command=donothing)
menubar.add_cascade(label="Editar", menu=editmenu)

#submenu ayuda
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Indice de Ayuda", command=donothing)
helpmenu.add_command(label="Acerca de...", command=donothing)
menubar.add_cascade(label="Ayuda", menu=helpmenu)

#area de texto y scroll
scroll= Scrollbar(root)
textarea = Text(root, height=22, width=170)
scroll.pack(side=RIGHT, fill=Y)
textarea.pack(side=TOP, fill=Y)
scroll.config(command=textarea.yview)
textarea.config(yscrollcommand=scroll.set)



#textarea.tag_configure('bold_italics', 
#                   font=('Verdana', 12, 'bold', 'italic'))

#textarea.tag_configure('big', 
#                   font=('Verdana', 24, 'bold'))
#textarea.tag_configure('color', 
 #                  foreground='blue', 
 #                  font=('Tempus Sans ITC', 14))
                   
#textarea.tag_configure('groove', 
 #                  relief=GROOVE, 
  #                 borderwidth=2)
                   
#textarea.tag_bind('bite', 
 #             '<1>', 
  #            lambda e, t=textarea: t.insert(END, "Text"))

#==============================================================================================================================================================

root.config(menu=menubar)
root.mainloop()
