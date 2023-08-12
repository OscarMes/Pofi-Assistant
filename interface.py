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
import concurrent.futures


class Cls_Frames:
    def __init__(self, ventana,row,column,width,height,color,columnspan=None,rowspan=None,propagate = 0):
        self.frm = tk.Frame(ventana, borderwidth=0,width=width, height=height,padx=0, pady=0)
        self.frm.grid(column=column,row=row,columnspan=columnspan,rowspan=rowspan)
        self.frm.config(bg=color)
        #grid_propagate evita que el frame se redimensione al tamaño del widget dentro de él
        #para eso se debe poner en "0"
        self.frm.grid_propagate(propagate)

class Cls_Label:
    def __init__(self,ventana,texto,bg,tamano_letra,color_letra,row,column,padx,pady,sticky=None,):
        self.lbl = tk.Label(ventana,text=texto,bg=bg,font=("FixedSys",tamano_letra),fg = color_letra)
        self.lbl.grid(row=row,column=column,sticky=sticky,padx=padx,pady=pady)

class Cls_Botones:
    def __init__(self,ventana,row,column,width,height,img,bg,acbg,resize,pady,padx,command=None):
        self.selcImagen = PIL.Image.open(img)
        self.selcImagen = self.selcImagen.resize((self.selcImagen.width // resize, self.selcImagen.height // resize))
        self.imgBoton = PIL.ImageTk.PhotoImage(self.selcImagen)
        self.btn = tk.Button(ventana,width=width, height=height, image=self.imgBoton,borderwidth=0, command=command,bg=bg,activebackground=acbg)
        self.btn.grid(row=row, column=column,pady=pady,padx=padx)

class Cls_Ventana:
    def __init__(self):
        self.control_mensaje = False
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

        #esta sección es la cabecera de la aplicación
        ObjCls_Frames_Nombre_IA = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=0,column=0,width=self.int_ancho_ventana,height=60,color="#095f56",columnspan=2)
        ObjCls_Frames_Boton_imagen = Cls_Frames(ventana=ObjCls_Frames_Nombre_IA.frm,row=0,column=0,width=70,height=60,color="#095f56")
        ObjCls_Frames_Pofi_estado = Cls_Frames(ventana=ObjCls_Frames_Nombre_IA.frm,row=0,column=1,width=400,height=60,color="#095f56")
        ObjCls_Frames_llamadas = Cls_Frames(ventana=ObjCls_Frames_Nombre_IA.frm,row=0,column=2,width=self.int_ancho_ventana,height=60,color="#095f56")

        self.ObjCls_Frames_historial_mensaje = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=1,column=0,width=self.int_ancho_ventana,height=400,color="#e5ddd5",columnspan=2,rowspan=2)
       
        self.ObjCls_Frames_Entrada_contenedor = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=3,column=0,width=500,height=50,color="#e5ddd5", columnspan=3)
        ObjCls_Frames_Entrada_Text = Cls_Frames(ventana=self.ObjCls_Frames_Entrada_contenedor.frm,row=0,column=0,width=450,height=50,color="#e5ddd5",columnspan=2)
        ObjCls_Frames_Entrada_Boton = Cls_Frames(ventana=self.ObjCls_Frames_Entrada_contenedor.frm,row=0,column=2,width=50,height=50,color="#e5ddd5")

        ObjCls_Frames_Pie = Cls_Frames(ventana=ObjCls_Frames_contenedor.frm,row=5,column=0,width=self.int_ancho_ventana,height=10,color="#e5ddd5",columnspan=3)
        
        #label

        objCls_Label_nombre = Cls_Label(ObjCls_Frames_Pofi_estado.frm,"Pofi","#095f56",17,"white",0,0,None,None)
        objCls_Label_online = Cls_Label(ObjCls_Frames_Pofi_estado.frm,"En linea","#095f56",13,"white",1,0,None,None)
        
        #text
        self.txt_chat = tk.Text(ObjCls_Frames_Entrada_Text.frm,font=("FixedSys", 12),width=54,height=2)
        self.txt_chat.grid(column=0,row=0,padx=10,pady=10)
        self.txt_chat.focus_set()
        self.txt_chat.bind("<Return>", self.fnt_Obtener_Mensaje)

        scrollbar = tk.Scrollbar(ObjCls_Frames_Entrada_Text.frm, command=self.txt_chat.yview)
        scrollbar.grid(column=1, row=0, sticky='ns')

        self.txt_chat.config(yscrollcommand=scrollbar.set)
    
        #buttom
        self.objCls_Botones_imagen = Cls_Botones(ObjCls_Frames_Boton_imagen.frm,row=0,column=0,width=46,height=46,bg="#095f56",acbg="#095f56",img=r"icons/pofi_img.png",resize=9,pady=6,padx=10)
        self.ObjCls_Botones_Enviar = Cls_Botones(ObjCls_Frames_Entrada_Boton.frm,row=0,column=0,width=40,height=40,bg="#dedbd6",acbg="#dedbd6", img="icons/enviando.png",resize=12,pady=7,padx=4, command=lambda:self.fnt_Obtener_Mensaje(None))



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
            if self.control_mensaje == False:
            
                obj_cls_burbuja_usuario = Cls_Burbuja(self.ScrText_historial_Chat,0,0,"#d5ffc6")
                
                #primero envio mi mensaje a la interfaz,
                obj_cls_burbuja_usuario.fnt_mensaje(mensaje,False)

                
                #luego envio el mensaje al modelo por medio de un hilo
                self.hilo_inferencia = threading.Thread(target=self.ObjCls_Inferencia.fnt_inferencia, args=(mensaje,))
                #inicia el hilo 
                self.hilo_inferencia.start()


                mensaje_control = self.hilo_inferencia.is_alive()

                self.control_mensaje = mensaje_control

                

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
            else:
                mensaje_control = self.hilo_inferencia.is_alive()
                if mensaje_control == False:
                    self.control_mensaje = False 
                    
                return "break"
        


Cls_Ventana()




        

    