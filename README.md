# Pofi Assistant - interfaz de usuario 
Interfaz grafica creada en Tkinter para interactuar con el modelo de lenguaje Pofi Assistant, dicho modelo de lenguaje fue ajustado por mi para obtener ese “comportamiento”, el objetivo principal era solo ajustar un modelo de lenguaje llama de Meta, pero me surgió la necesidad de crear mi propia interfaz grafica al estilo de Whatsapp en honor a que el modelo base hace parte de la misma compañía.
Para utilizar el modelo primero hay que descargarlo del repositorio de Huggin face https://huggingface.co/Bluckr/llama-7B-ggml-q4_0-Pofi-Assistant/tree/main  y ubicar el archivo .bin en la carpeta model (si no se encuentra entonces se debe crear)
![descargar_modelo](https://github.com/OscarMes/Pofi-Assistant/assets/128978144/1fb65c9f-807e-4c3c-883c-a9019364adc8)
![carpeta_model1](https://github.com/OscarMes/Pofi-Assistant/assets/128978144/d6b6fed2-3603-46c6-90ef-177f172db721)
![modelo](https://github.com/OscarMes/Pofi-Assistant/assets/128978144/df38a48c-1a9e-4412-855c-791bb2027a8d)

El modelo esta cuantificado para correr sin necesidad de una GPU, al cuantificarlo pierde capacidad (es un poco tonto) pero para las ordenes de asistente se desempeña bien, esta versión del modelo solo actúa como asistente más no tiene la capacidad de interactuar con su entorno.

![1](https://github.com/OscarMes/Pofi-Assistant/assets/128978144/7e86d8b1-e83e-4983-9c91-effcff85d793)



Para subsanar esta incapacidad he creado un dataset
https://huggingface.co/datasets/Bluckr/function-calling-assistant-spanish-pofi-v2
 para entrenar un modelo mucho más inteligente al actual, cuya capacidad incluya function calling al estilo de GPT-3.5 turbo de OPENAI, aun así, las limitaciones por hardware son desalentadoras ya que un modelo más inteligente requiere como mínimo el uso de llama 2 13b chat y aunque sea cuantificado es mucho más lento al modelo más pequeño (llama 2 7b chat).

