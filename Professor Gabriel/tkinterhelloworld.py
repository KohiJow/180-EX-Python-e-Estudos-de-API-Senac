'''
from tkinter import *
root= Tk()
a = Label(root, text= 'Hello, World!')
a.pack()

root.mainloop()

#correção do professor
'''
#importando Greet para substituir a Label
import tkinter as tk

#Função Greet para substituir a Label
def greet():
    label.config(text='Olá, Mundo!')

#Tela onde todos os componentes serão colocados    
app = tk.Tk()
app.title('Hello World App')

#Criando o Widget label, uma area onde exibe a informação
label = tk.Label(app, text = '')
label.pack()

#Botão que exibe o clique aqui
button = tk.Button(app, text= 'Clique aqui', command=greet)
button.pack()

#Linha que deixa o código/tela aberta em loop
app.mainloop()
