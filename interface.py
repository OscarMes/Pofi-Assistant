import tkinter as tk
from tkinter import DISABLED
from datetime import datetime
import tkinter.scrolledtext as ScrolledText
import PIL.Image
import PIL.ImageTk
from high_level import Cls_Inferencia
from historial_mensaje import Cls_Burbuja
from llama_cpp import Llama, llama_tokenize
import threading

class Cls_Frames:
    def __init__(self, ventana,row,column,width,height,color,columnspan=None,rowspan=None,propagate = 0):
        self.frm = tk.Frame(ventana, borderwidth=0,width=width, height=height,padx=0, pady=0)
        self.frm.grid(column=column,row=row,columnspan=columnspan,rowspan=rowspan)
        self.frm.config(bg=color)
        #grid_propagate evita que el frame se redimensione al tamaño del widget dentro de él
        #para eso se debe poner en "0"
        self.frm.grid_propagate(propagate)

class Cls_Label:
    def __init__(self,ventana,texto,bg,row=0,column=0,sticky=None,padx=15,pady=10):
        self.lbl = tk.Label(ventana,text=texto,bg=bg,font=("FixedSys",11))
        self.lbl.grid(row=row,column=column,sticky=sticky,padx=padx,pady=pady)

class Cls_Botones:
    def __init__(self,ventana,row,column,width,height,img,command=None):
        self.selcImagen = PIL.Image.open(img)
        self.selcImagen = self.selcImagen.resize((self.selcImagen.width // 12, self.selcImagen.height // 12))
        self.imgBoton = PIL.ImageTk.PhotoImage(self.selcImagen)
        self.btn = tk.Button(ventana,width=width, height=height, image=self.imgBoton,borderwidth=0, command=command,bg="#dedbd6",activebackground="#dedbd6")
        self.btn.grid(row=row, column=column,pady=7,padx=4)

class Cls_Ventana:
    def __init__(self):
        self.model = r"model\modelo_Pofi_Lora_ggml-q4_0.bin"
        self.n_ctx = 1024
        self.llm = Llama(model_path=self.model,n_batch = 512,low_vram = True,n_ctx=self.n_ctx)
        self.encoding = "utf-8"
        self.ObjCls_Inferencia = Cls_Inferencia(n_ctx=self.n_ctx,llm=self.llm,encoding=self.encoding)

        self.ventana = tk.Tk()
        self.fnt_ParametrosVentana()
        self.ventana.mainloop()

    def fnt_ParametrosVentana(self):
        self.int_ancho_ventana = 500
        self.int_alto_ventana = 540
        self.ventana.geometry(f"{self.int_ancho_ventana}x{self.int_alto_ventana}")
        self.fnt_Items()

    def fnt_Items(self):
        #frames
        ObjCls_Frames_contenedor = Cls_Frames(ventana=self.ventana,row=0,column=0,width=self.int_ancho_ventana,height=580,color="#e5ddd5")

        ObjCls_Frames_Nombre_IA = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=0,column=0,width=self.int_ancho_ventana,height=70,color="#095f56",columnspan=2)
        self.ObjCls_Frames_historial_mensaje = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=1,column=0,width=self.int_ancho_ventana,height=400,color="#e5ddd5",columnspan=2,rowspan=2)
       
        self.ObjCls_Frames_Entrada_contenedor = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=3,column=0,width=500,height=50,color="#e5ddd5", columnspan=3)
        ObjCls_Frames_Entrada_Text = Cls_Frames(ventana=self.ObjCls_Frames_Entrada_contenedor.frm,row=0,column=0,width=450,height=50,color="#e5ddd5",columnspan=2)
        ObjCls_Frames_Entrada_Boton = Cls_Frames(ventana=self.ObjCls_Frames_Entrada_contenedor.frm,row=0,column=2,width=50,height=50,color="#e5ddd5")

        ObjCls_Frames_Pie = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=5,column=0,width=self.int_ancho_ventana,height=10,color="#e5ddd5",columnspan=3)
        
        #text
        self.txt_chat = tk.Text(ObjCls_Frames_Entrada_Text.frm,font=("FixedSys", 12),width=54,height=2)
        self.txt_chat.grid(column=0,row=0,padx=10,pady=10)
        self.txt_chat.bind("<Return>", self.fnt_Obtener_Mensaje)

        scrollbar = tk.Scrollbar(ObjCls_Frames_Entrada_Text.frm, command=self.txt_chat.yview)
        scrollbar.grid(column=1, row=0, sticky='ns')

        self.txt_chat.config(yscrollcommand=scrollbar.set)
    
        #buttom
        self.ObjCls_Botones_Enviar = Cls_Botones(ObjCls_Frames_Entrada_Boton.frm,row=0,column=0,width=40,height=40,img="icons/enviando.png",command=lambda:self.fnt_Obtener_Mensaje(None))



        self.ScrText_historial_Chat = ScrolledText.ScrolledText(
            self.ObjCls_Frames_historial_mensaje.frm,
            bg="#e5ddd5",
            height="22",
            width="54",
            font="Arial")
        
        self.ObjCls_Inferencia.fnt_parametros_ventana(self.ScrText_historial_Chat)


    def fnt_Obtener_Mensaje(self,event):

        mensaje = self.txt_chat.get("1.0",tk.END)

        if self.txt_chat.compare("end-1c","==","1.0"):
            return "break"
        else:
            
            obj_cls_burbuja_usuario = Cls_Burbuja(self.ScrText_historial_Chat,0,0,"#d5ffc6")
            
            #primero envio mi mensaje a la interfaz,
            obj_cls_burbuja_usuario.fnt_mensaje(mensaje)
            #luego envio el mensaje al modelo por medio de un hilo
            hilo_inferencia = threading.Thread(target=self.ObjCls_Inferencia.fnt_inferencia, args=(mensaje,))
            #inicia el hilo 
            hilo_inferencia.start()

            #envio de mensajes sin manipulación de hilo
            #self.ObjCls_Inferencia.fnt_inferencia(mensaje)


            #le indico la posición que debe tener la burbuja del usuario, en este caso la derecha
            self.ScrText_historial_Chat.tag_configure('tag-right', justify='right')

            #state normal es que el widget si funciona
            self.ScrText_historial_Chat.config(state=tk.NORMAL,)
            #saltos de linea 
            self.ScrText_historial_Chat.insert('end', '\n ','tag-right')
            #window create es para decirle que vamos a meter dentro del widget de text scrtext
            self.ScrText_historial_Chat.window_create('end', window=obj_cls_burbuja_usuario.frm)
            
            #esto habilita el desplazamiento hacía abajo de manera automatica
            self.ScrText_historial_Chat.see(tk.END)
            #limpia el campo de texto(entrada de texto)
            self.txt_chat.delete("1.0", tk.END)
            return "break"
        


Cls_Ventana()




        

    