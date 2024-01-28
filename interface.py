import tkinter as tk
import tkinter.scrolledtext as ScrolledText
import PIL.Image
import PIL.ImageTk
from high_level import Cls_Inferencia
from historial_mensaje import Cls_Burbuja
from flujo_mensaje import Cls_flujo
from llama_cpp import Llama
import threading
import customtkinter as ctk

#la clase Frames me permite crear multiples frames sin necesidad de 
#reescribir código, lo mismo sucede con las demás clases cuyos nombres
#hacen referencia a un widget
class Cls_Frames:
    def __init__(self, ventana,row,column,width,height,color,columnspan=None,rowspan=None,propagate = 0):
        self.frm = tk.Frame(ventana, borderwidth=0,width=width, height=height,padx=0, pady=0)
        self.frm.grid(column=column,row=row,columnspan=columnspan,rowspan=rowspan)
        self.frm.config(bg=color)
        #grid_propagate evita que el frame se redimensione al tamaño del widget dentro de él
        #para eso se debe poner en "0"
        self.frm.grid_propagate(propagate)

class Cls_Label:
    def fnt_lbl_parametros(self,ventana,texto,bg,tamano_letra,color_letra,row,column,padx,pady,sticky=None,):
        self.lbl = tk.Label(ventana,text=texto,bg=bg,font=("FixedSys",tamano_letra),fg = color_letra)
        self.lbl.grid(row=row,column=column,sticky=sticky,padx=padx,pady=pady)

class Cls_Botones:
    def __init__(self,ventana,row,column,width,height,img,bg,acbg,resize,pady,padx,command=None):
        self.selcImagen = PIL.Image.open(img)
        self.selcImagen = self.selcImagen.resize((self.selcImagen.width // resize, self.selcImagen.height // resize))
        self.imgBoton = PIL.ImageTk.PhotoImage(self.selcImagen)
        self.btn = tk.Button(ventana,width=width, height=height, image=self.imgBoton,borderwidth=0, command=command,bg=bg,activebackground=acbg)
        self.btn.grid(row=row, column=column,pady=pady,padx=padx)

#con esta clase puedo crear un mensaje en pantalla y añadir los parametros necesarios
#si es un mensaje de la IA o un mensaje del usuario, a la par que agregar el 
#color y la dirección que conlleva cada uno, IA (Izquierda, blanco), Usuario (Derecha, verde)
class Cls_Parametros_Burbujas_chat:
    def __init__(self,mensaje,tag,justify,scrolltext,color):
        self.obj_cls_burbuja_pofi = Cls_Burbuja(scrolltext,0,0,color)
        self.obj_cls_burbuja_pofi.fnt_mensaje(mensaje)
        self.scrolledtext = scrolltext
        self.scrolledtext.config(state=tk.NORMAL)
        #scrolltext.configure(state= "disabled")
        self.scrolledtext.tag_configure(tag, justify=justify)
        self.scrolledtext.insert('end', '\n ',tag)
        self.scrolledtext.window_create('end', window=self.obj_cls_burbuja_pofi.frm)
    
        self.scrolledtext.see(tk.END)

#añado los objetos de las clases creadas anteriormente
class Cls_Ventana:
    def __init__(self):
        self.control_mensaje = False
        #agrego la dirección del modelo para que inicie con la interfaz
        self.model = r"model\modelo_Pofi_Lora_ggml-q4_0.bin"
        #el contexto que tendrá el modelo 
        self.n_ctx = 1024
        self.llm = Llama(model_path=self.model,n_batch = 512,low_vram = True,n_ctx=self.n_ctx)
        self.encoding = "utf-8"
        self.ObjCls_Inferencia = Cls_Inferencia(n_ctx=self.n_ctx,llm=self.llm,encoding=self.encoding)
        #self.ObjCls_flujo = Cls_flujo(_user="",_ia="",_state="")
        self.ObjCls_flujo = Cls_flujo()
        self.ObjCls_flujo.fnt_modificar_JSON(_user="",_ai="",_state="")
        #self.ventana = tk.Tk()
        self.ventana = ctk.CTk()
        self.fnt_ParametrosVentana()


        #self.fnt_presionar_frm
        #self.fnt_mover_ventana
        
        self.ventana.mainloop()

    def fnt_ParametrosVentana(self):
        self.int_ancho_ventana = 500
        self.int_alto_ventana = 520
        self.ventana.geometry(f"{self.int_ancho_ventana}x{self.int_alto_ventana}")
        #====intento de crear mi barra personalizada====#
        #self.ventana.overrideredirect(True)
        #===============================================#
        self.lbl_estado = "En linea"
        self.ventana.title("WhatChat")
        self.ventana.iconbitmap("icons\shimeji.ico")
        ctk.set_appearance_mode("darck")



        self.ventana.resizable(False, False)
        self.fnt_Items()

    def fnt_Items(self):
        #frames
        #este es el contenedor principal de todos los items
        ObjCls_Frames_contenedor = Cls_Frames(ventana=self.ventana,row=0,column=0,width=self.int_ancho_ventana,height=540,color="#e5ddd5")

        #======= Quería crear una barra de menú personalizada =====#
        #frame para minimizar, mover y cerrar la ventana
        #ObjCls_Frames_Clos_Min_Mov = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=0,column=0,width=self.int_ancho_ventana,height=20,color="#e5ddd5",columnspan=3)
        #ObjCls_Frames_Espacio_Mover = Cls_Frames(ventana=ObjCls_Frames_Clos_Min_Mov.frm,row=0,column=0,width=450,height=50,color="#e5ddd5",columnspan=2)
        #ObjCls_Frames_Espacio_Mover.frm.bind("<ButtonPress-1>", self.fnt_presionar_frm)
        #ObjCls_Frames_Espacio_Mover.frm.bind("<B1-Motion>", self.fnt_mover_ventana)
        #ObjCls_Frames_Botones_principales = Cls_Frames(ventana=ObjCls_Frames_Clos_Min_Mov.frm,row=0,column=2,width=50,height=50,color="#e5ddd5")
        #==========================================================#

        #esta sección es la cabecera de la aplicación
        #el frame donde se almacena el nombre, la foto y el estado es este (Nombre_IA)
        ObjCls_Frames_Nombre_IA = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=1,column=0,width=self.int_ancho_ventana,height=60,color="#095f56",columnspan=2)
        ObjCls_Frames_Boton_imagen = Cls_Frames(ventana=ObjCls_Frames_Nombre_IA.frm,row=0,column=0,width=70,height=60,color="#095f56")
        self.ObjCls_Frames_Pofi_estado = Cls_Frames(ventana=ObjCls_Frames_Nombre_IA.frm,row=0,column=1,width=400,height=60,color="#095f56")
        ObjCls_Frames_llamadas = Cls_Frames(ventana=ObjCls_Frames_Nombre_IA.frm,row=0,column=2,width=self.int_ancho_ventana,height=60,color="#095f56")

        #frame para poner el scroll historial de mensajes
        self.ObjCls_Frames_historial_mensaje = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=2,column=0,width=self.int_ancho_ventana,height=400,color="#e5ddd5",columnspan=2,rowspan=2)
       
        #frame que contiene la parte de abajo del diseño, entrada de texto y botón de enviar
        self.ObjCls_Frames_Entrada_contenedor = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=4,column=0,width=500,height=50,color="#e5ddd5", columnspan=3)
        ObjCls_Frames_Entrada_Text = Cls_Frames(ventana=self.ObjCls_Frames_Entrada_contenedor.frm,row=0,column=0,width=450,height=50,color="#e5ddd5",columnspan=2)
        ObjCls_Frames_Entrada_Boton = Cls_Frames(ventana=self.ObjCls_Frames_Entrada_contenedor.frm,row=0,column=2,width=50,height=50,color="#e5ddd5")

        #un simple frame para dejar un espacio entre la entrada de texto y el marco de la ventana
        ObjCls_Frames_Pie = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=6,column=0,width=self.int_ancho_ventana,height=10,color="#e5ddd5",columnspan=3)
        

        #label
        objCls_Label_nombre = Cls_Label()
        objCls_Label_nombre.fnt_lbl_parametros(self.ObjCls_Frames_Pofi_estado.frm,"Pofi","#095f56",17,"white",0,0,None,None)
        self.objCls_Label_online = Cls_Label()
        self.objCls_Label_online.fnt_lbl_parametros(self.ObjCls_Frames_Pofi_estado.frm,self.lbl_estado,"#095f56",13,"white",1,0,None,None)
        
        #text
        self.txt_chat = tk.Text(ObjCls_Frames_Entrada_Text.frm,font=("FixedSys", 12),width=54,height=2)
        self.txt_chat.grid(column=0,row=0,padx=10,pady=10)
        #establecer el focus en el area de escritura
        self.txt_chat.focus_set()
        #evitar que "Enter" sea un salto de linea 
        self.txt_chat.bind("<Return>", self.fnt_Obtener_Mensaje)

        scrollbar = tk.Scrollbar(ObjCls_Frames_Entrada_Text.frm, command=self.txt_chat.yview)
        scrollbar.grid(column=1, row=0, sticky='ns')

        self.txt_chat.config(yscrollcommand=scrollbar.set)
    
        #buttom
        self.objCls_Botones_imagen = Cls_Botones(ObjCls_Frames_Boton_imagen.frm,row=0,column=0,width=46,height=46,bg="#095f56",acbg="#095f56",img=r"icons/pofi_img.png",resize=9,pady=6,padx=10)
        self.ObjCls_Botones_Enviar = Cls_Botones(ObjCls_Frames_Entrada_Boton.frm,row=0,column=0,width=40,height=40,bg="#dedbd6",acbg="#dedbd6", img="icons/enviando.png",resize=12,pady=7,padx=4, command=lambda:self.fnt_Obtener_Mensaje(None))

        #======Botones descartados =====#
        #self.ObjCls_Botones_Minimizar = Cls_Botones(ObjCls_Frames_Botones_principales.frm,row=0,column=0,width=20,height=20,bg="#dedbd6",acbg="#dedbd6", img="icons/minimizar.png",resize=23,pady=0,padx=1, command= lambda:self.ventana.iconify())
        #self.ObjCls_Botones_Cerrar = Cls_Botones(ObjCls_Frames_Botones_principales.frm,row=0,column=1,width=20,height=20,bg="#dedbd6",acbg="#dedbd6", img="icons/cerrar.png",resize=23,pady=0,padx=0, command=lambda:self.ventana.destroy())
        #===============================#

        self.ScrText_historial_Chat = ScrolledText.ScrolledText(
            self.ObjCls_Frames_historial_mensaje.frm,
            bg="#e5ddd5",
            height="22",
            width="54",
            font="Arial")
        
    #====funciones de barra de titulo personalizado==#
    # def fnt_mover_ventana(self,event):
    #     self.ventana.geometry(f"+{event.x_root - self.x_click}+{event.y_root - self.y_click}")

    # def fnt_presionar_frm(self,event):
        
    #     self.x_click = event.x
    #     self.y_click = event.y
    #=================================================#

        self.fnt_leer_AI()

    #función que sirve para establecer el estado de la IA y
    #poner su mensaje en pantalla 
    def fnt_leer_AI(self):
        #debemos leer el estado del Json
        self.ObjCls_flujo = Cls_flujo()
        _user,_ai,_state = self.ObjCls_flujo.fnt_leer_JSON()
        #actualizamos la ventana contantemente 
        self.ventana.after(500,self.fnt_leer_AI)
        self.ventana.update()

        self.lbl_estado = _state
        #self.objCls_Label_online = Cls_Label(self.ObjCls_Frames_Pofi_estado.frm,self.lbl_estado,"#095f56",13,"white",1,0,None,None)
        self.objCls_Label_online.fnt_lbl_parametros(self.ObjCls_Frames_Pofi_estado.frm,self.lbl_estado,"#095f56",13,"white",1,0,None,None)
        #self.ScrText_historial_Chat.see(tk.END)

        if _ai != "":
            Obj_Cls_Parametros = Cls_Parametros_Burbujas_chat(mensaje=_ai,tag='tag-left',justify='left',scrolltext=self.ScrText_historial_Chat,color='#ffffff')
            self.ObjCls_flujo.fnt_modificar_JSON(_user = _user, _ai="",_state="En linea")
            
    
    #función para obtener el texto escrito por el usuario 
    def fnt_Obtener_Mensaje(self,event):

        #obtenemos el texto de Text
        mensaje = self.txt_chat.get("1.0",tk.END)

        #nos aseguramos que el mensaje no esté vacío,
        #si el mensaje es vacío entonces no pasa nada (no se envía y solo hace un salto de línea)
        if self.txt_chat.compare("end-1c","==","1.0"):
            return "break"
        else:
            #debo leer el archivo JSON para usar el condicional
            self.ObjCls_flujo = Cls_flujo()
            #leemos el archivo Json
            _user,_ai,_status = self.ObjCls_flujo.fnt_leer_JSON()

            #debemos asegurarnos que el usuario no tiene un mensaje ya cargado
            #cuando (_user == "") es porque la IA ya respondió y el programa limpia la parte
            #del usuario para no mandar más de un mensaje a la vez
            if _user == "":
                
                #modifico el contenido del JSON 
                self.ObjCls_flujo.fnt_modificar_JSON(_user=mensaje,_ai="",_state="En línea")
            
                #luego envio el mensaje al modelo por medio de un hilo
                self.hilo_inferencia = threading.Thread(target=self.ObjCls_Inferencia.fnt_inferencia, args=(mensaje,))
                #inicia el hilo 
                self.hilo_inferencia.start()
                
                #envio de mensajes sin manipulación de hilo(esto causa que la ventana principal se congele)
                #self.ObjCls_Inferencia.fnt_inferencia(mensaje)
                #los mensajes del usuario van a la derecha y sonde color verde
                Obj_Cls_Parametros = Cls_Parametros_Burbujas_chat(mensaje=mensaje,tag='tag-right',justify='right',scrolltext=self.ScrText_historial_Chat,color='#d5ffc6')
                #limpiamos la caja de texto porque el mensaje ya se envió
                self.txt_chat.delete("1.0", tk.END)
                
                #self.ObjCls_flujo.fnt_modificar_JSON(_user=_user,_ai=_ai,_state="Escribiendo")

                #cargamos la variable _user con el último mensaje que envió el usuario y quedó registrado en el Json 
                _user,_ai,_state = self.ObjCls_flujo.fnt_leer_JSON()


                return "break"
            else:
                return "break"
            
Cls_Ventana()




        

    