from historial_mensaje import Cls_Burbuja
import tkinter as tk
import time 
import json
from flujo_mensaje import Cls_flujo

class Cls_Inferencia:
    def __init__(self,n_ctx, llm, encoding):
        self.n_ctx = n_ctx
        self.llm = llm
        self.encoding = encoding
        #creo un cadena de caracteres y la codifico a bytes utf-8
        #este es el historial y contexto de la conversación
        self.byte_historial_Contexto = "".encode(self.encoding)

    def fnt_parametros_ventana(self,frm):
        self.frm = frm

    def fnt_inferencia(self, entrada):
        # self.obj_cls_burbuja_pofi = Cls_Burbuja(self.frm,1,0,"#ffffff")

        #se establecen los datos para la inferencia
        stream = self.llm(
                #llamo a esta cadena de caracteres y la decodifico a string para que sea usado como
                #contexto junto con la nueva entrada del usuario 
                f"{self.byte_historial_Contexto.decode(self.encoding)}### User:\n{entrada}\n\n### AI:\n",
                max_tokens=256,
                temperature=1.31, 
                top_p=0.10, 
                top_k=49,
                repeat_penalty=1.17,
                tfs_z=1.0,
                mirostat_mode=0,
                mirostat_tau=5.0, 
                mirostat_eta=0.1,
                stream=True,
            #presence_penalty=0.75, 
            #frequency_penalty=0.75,
            stop=["User:", "\n"],    
        )
        #creo un string para extraer la inferencia del modelo 
        self.texto_inferencia = ""

        #agrego la entrada del usuario a la cadena de bytes 
        #para esto se debe pasar como bytes utf-8
        self.byte_historial_Contexto += f"### User:\n{entrada}\n\n### AI:\n".encode(self.encoding)

        for output in stream:
            # Extraer el texto del resultado y agregarlo a la lista
            self.text = output["choices"][0]["text"]
            #print(self.text, end="")
            #agrego la inferencia creada por Pofi a la cadena de bytes utf-8
            self.byte_historial_Contexto += self.text.encode(self.encoding)
            #como estoy dentro un un bucle debo agregar token por token 
            #la generación de Pofi a la cadena de String fuera del bucle
            self.texto_inferencia += self.text




        Obj_Cls_flujo = Cls_flujo()
        Obj_Cls_flujo.fnt_modificar_JSON(_user="",_ia=self.texto_inferencia,_state="Escribiendo")




        #agrego un salto de línea al final de todo el contexto
        self.byte_historial_Contexto += "\n\n".encode(self.encoding)
        
        #creo una variable para sacar el número de tokens dentro de la 
        #cadena de bytes que contienen el contexto (historial)
        n_tokens = self.llm.tokenize(self.byte_historial_Contexto)

        #hago un condicional para saber si el número de tokens es mayor 
        #o igual al número de contexto (1024)
        if (len(n_tokens) >= self.n_ctx):
            #si hay mayor o igual cantidad de tokens en el historial
            #borro los primeros 256 y sigo dejando 768 de un maximo de 1024 
            n_tokens = (n_tokens[256:])
            #reescribo mi lista de bytes con los los primeros 256 tokens
            #borrados y así el bucle continua, haciendo espacio y
            #metiendo más tokens 
            self.byte_historial_Contexto = self.llm.detokenize(n_tokens)
           # print(len(n_tokens))

