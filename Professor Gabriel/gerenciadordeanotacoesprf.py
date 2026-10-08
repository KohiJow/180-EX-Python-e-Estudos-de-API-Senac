import tkinter as tk
from tkinter import simpledialog, messagebox

#Alterar pois devemos guardar a informação em um argumento e não acessar a variavel direto
#def add_note():
def add_note(listbox):
    note = simpledialog.askstring("Nota", "Digite a sua nota:")
    if note: 
        listbox.insert(tk.END, note)

#Alterar pois devemos guardar a informação em um argumento e não acessar a variavel direto
#def delete_note():
def delete_note(listbox):
    try:
        selected_note = listbox.curselection()[0]
        listbox.delete(selected_note)
    
#Função delete_note captura especificamente IndexError, 
#que é a exceção lançada quando não há seleção na Listbox,
#except é genérico.
    #except:
    except IndexError:
        messagebox.showwarning("Aviso", "Nenhuma nota selecionada.")

#A janela so e criada quando o arquivo e executado direto. Quem importa add_note e
#delete_note (os testes) nao pode abrir janela nem ficar preso no mainloop.
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Gerenciador de Notas")

    listbox = tk.Listbox(root, font="Arial 14", height=10, width=50)
    listbox.pack(pady=10)

    #Usar lambda para passar a referência do listbox quando os botões são clicados.
    #Sem o lambda não teria acesso ao listbox
    add_button = tk.Button(root, text="Adicionar Nota", command=lambda: add_note(listbox), font="Arial 14")
    add_button.pack(pady=5)

    #Usar lambda para passar a referência do listbox quando os botões são clicados.
    #Sem o lambda não teria acesso ao listbox
    delete_button = tk.Button(root, text="Remover Nota", command=lambda: delete_note(listbox), font="Arial 14")
    delete_button.pack(pady=5)

    root.mainloop()