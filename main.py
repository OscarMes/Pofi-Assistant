from llama_cpp import Llama, llama_tokenize
from interface import Cls_Ventana
from high_level import Cls_Inferencia


class Cls_Pofi:
    def __init__(self):
        model = r"model\modelo_Pofi_Lora_ggml-q4_0.bin"
        n_ctx = 1024
        llm = Llama(model_path=model,n_batch = 512,low_vram = True,n_ctx=n_ctx)
        encoding = "utf-8"
        
        ObjCls_Ventana = Cls_Ventana()
        ObjCls_Inferencia = Cls_Inferencia()
        ObjCls_Inferencia.fnt_argumentos(n_ctx=n_ctx,llm=llm,encoding=encoding)


if __name__ == "__main__":
    ObjCls_Pofi = Cls_Pofi()
