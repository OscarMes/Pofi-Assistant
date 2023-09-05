import json

class Cls_flujo:
    
    def fnt_leer_JSON(self):
        with open('mensaje.json', 'r' ,encoding="utf-8" ) as archivo:
            lector = json.load(archivo)
            condicion_user = lector['User']
            return condicion_user

    
    def fnt_modificar_JSON(self, _user, _ia, _state):
        with open('mensaje.json', 'r' ,encoding="utf-8" ) as archivo:
            self.lector = json.load(archivo)
            self.user = _user
            self.ia = _ia
            self.state = _state
            self.lector['User'] = self.user
            self.lector['IA'] = self.ia
            self.lector['State'] = self.state
            #mandamos la nueva info al JSON
        with open('mensaje.json', 'w', encoding="utf-8") as archivo:
            json.dump(self.lector, archivo, indent=4)



