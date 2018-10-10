#Daniel Zamora García
#Esteban Montero Fonseca
#Jeferson Moreno Zuñiga

#Proyecto #1 de Paradigmas de Programación

#interfaz
from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as ET 

#===============================================================Seccion de metodos=========================================================================
textTop = 0 #Guarda el text superior para usarlo en otras funciones
textBot = 0 #Guarda el text innferior para usarlo en otras funciones

#Funcion para mostrar datos en el TextArea
def writeOnText(str):
    textTop.delete('1.0', END)
    textTop.update()
    textTop.insert(END, str)

#Fncion para obtener el input del Text
def retrieveInput():
    input = textTop.get("1.0",'end-1c')
    print(input)
    return input

#Leer archivos xml y mostrarlos en pantalla
def readXML(path):
    tree = ET.parse(path)  
    root = tree.getroot()
    # atributos de un item
    #print('Item #2 attribute:')  
    #print(root[0][1].attrib)
    # atributos de toddos los items
    #print('\nAll attributes:')  
    for elem in root:  
        for subelem in elem:
            print(subelem.attrib)
    # dato de un item especifico
    #print('\nItem #2 data:')  
    #print(root[0][1].text)
    # datos de todos los items
    #print('\nAll item data:')  
    for elem in root:  
        for subelem in elem:
            writeOnText(subelem.text)
        writeOnText("\n")

#Leer archivos txt y mostrarlos en pantalla
def readTXT(path):
    file = open(path, "r") 
    for line in file:
        writeOnText(line) 

#Crear y guarddar archivos xml (ver e implementar el formato del los xml)
def writeXML(path):
    data = ET.Element('data')  
    items = ET.SubElement(data, 'items')  
    item1 = ET.SubElement(items, 'item')  
    item2 = ET.SubElement(items, 'item')  
    item1.set('name','item1')  
    item2.set('name','item2')  
    item1.text = 'item1abc'  
    item2.text = 'item2abc'
    # crea un nuevo archivo XML con los resultados 
    myfile = open(path, "wb")  
    myfile.write(ET.tostring(data))

#Crear y guardar archivos txt
def writeTXT(path):
    file = open(path,"w")
    file.write(retrieveInput())
    file.close() 

def donothing():
    filewin = TopLevel(root)
    button = Button(filewin, text="Do nothin button")
    button.pack()

#abre el explorador de archivos
def abrirArchivo():
    path = filedialog.askopenfilename(initialdir = "/",title = "Abrir archivo",filetypes = (("Text file","*.txt"),("XML file","*.xml")))
    if (path.endswith('.xml')):
        readXML(path)
    elif (path.endswith('.txt')):
        readTXT(path)
   
#guardar el archivo como
def guardarArchivo():
    path = filedialog.asksaveasfilename(initialdir = "/",title = "Guardar archivo",filetypes = (("Text files","*.txt"),("XML files","*.xml")))
    if (path.endswith('.xml')):
        writeXML(path)
    elif (path.endswith('.txt')):
        writeTXT(path)

#Opcion guardar en el menu (implementar)
def modificarArchivo():
    print("")



#Mostrar el textArea en la pantalla
def textArea(root):
    scroll = Scrollbar(root)
    root.textarea = Text(root)
    root.textarea.pack()
    scroll.pack(side=RIGHT, fill=Y)
    root.textarea.pack(side=TOP, fill=BOTH)
    scroll.config(command=root.textarea.yview)
    root.textarea.config(yscrollcommand=scroll.set)
    return root.textarea 
    

#Mostrar el menu en la pantalla
def menu(root):
    menubar = Menu(root)
    #barra menu
    filemenu = Menu(menubar, tearoff=0)
    #submenu archivo
    filemenu.add_command(label="Nuevo", command=donothing)
    filemenu.add_command(label="Abrir", command=abrirArchivo)
    filemenu.add_command(label="Guardar", command=modificarArchivo)
    filemenu.add_command(label="Guardar como...", command=guardarArchivo)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.destroy)
    menubar.add_cascade(label="Archivo", menu=filemenu)
    editmenu = Menu(menubar, tearoff=0)
    #submenu editar
    editmenu.add_command(label="Deshacer", command=donothing)
    editmenu.add_separator()
    editmenu.add_command(label="Cortar", command=donothing)
    editmenu.add_command(label="Copiar", command=donothing)
    editmenu.add_command(label="Pegar", command=donothing)
    editmenu.add_command(label="Seleccionar todo", command=donothing)
    menubar.add_cascade(label="Editar", menu=editmenu)
    helpmenu = Menu(menubar, tearoff=0)
    #submenu ayuda
    helpmenu.add_command(label="Indice de Ayuda", command=donothing)
    helpmenu.add_command(label="Acerca de...", command=donothing)
    menubar.add_cascade(label="Ayuda", menu=helpmenu)
    root.config(menu=menubar)

#Mostrar la pantalla princcipal
def pantallaPrincipal():
    root = Tk()
    root.title("IDE")
    #screen_width = root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()
    #root.geometry('%sx%s' % (screen_width, screen_height))
    #root.attributes('-fullscreen', True)
    root.state('zoomed')
    #menu principal y submenus
    menu(root)
    #area de texto y scroll
    global textTop, textBot
    textTop = textArea(root)
    textBot = textArea(root)
    root.mainloop()

#===========================================================================================================================================================

#==============================================================Pantalla principal==========================================================================
pantallaPrincipal()



#==========================================================================================================================================================

