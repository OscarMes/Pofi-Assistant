import json

#la clase flujo permite saber el contenido de los mensajes y escribirlos 
#en la pantalla, también extrae el estado de la IA, Online o Escribiendo
class Cls_flujo:
    #la función lee el archivo Json donde se almacenan los mensajes y el estado
    #luego almacena esto en las variables (condicion_user, respuesta_ai, estado_ai)
    #para posteriormente retornarlo 
    def fnt_leer_JSON(self):
        with open('mensaje.json', 'r' ,encoding="utf-8" ) as archivo:
            lector = json.load(archivo)
            condicion_user = lector['User']
            respuesta_ai = lector['AI']
            estado_ai = lector['State']
            return condicion_user, respuesta_ai, estado_ai

    #recibe los parametros de (_user, _ai, _state) ya que esta función es llamada 
    #en la interfaz para cambiar el contenido del Json, no retorna nada porque para eso
    #eso está la función de leer Json
    def fnt_modificar_JSON(self, _user, _ai, _state):
        with open('mensaje.json', 'r' ,encoding="utf-8" ) as archivo:
            self.lector = json.load(archivo)
            self.user = _user
            self.ia = _ai
            self.state = _state
            self.lector['User'] = self.user
            self.lector['AI'] = self.ia
            self.lector['State'] = self.state
            #mandamos la nueva info al JSON
        with open('mensaje.json', 'w', encoding="utf-8") as archivo:
            json.dump(self.lector, archivo, indent=4)



