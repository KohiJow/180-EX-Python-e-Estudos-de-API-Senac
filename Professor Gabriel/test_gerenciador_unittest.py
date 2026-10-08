import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from gerenciadordeanotacoesprf import add_note, delete_note  

class TestNoteManager(unittest.TestCase):

    def setUp(self):
        # Configuração do mock para a lista
        self.listbox = MagicMock()

    @patch('tkinter.simpledialog.askstring', return_value='Test Note')
    def test_add_note(self, mock_askstring):
        add_note(self.listbox)
        self.listbox.insert.assert_called_once_with(tk.END, 'Test Note')

    @patch('tkinter.simpledialog.askstring', return_value='Adicionar Nota')
    def test_add_note_simulation(self, mock_askstring):
        add_note(self.listbox)
        self.listbox.insert.assert_called_once_with(tk.END, 'Adicionar Nota')

    def test_delete_note_success(self):
        self.listbox.curselection.return_value = [0]  # Simula a seleção de uma nota
        delete_note(self.listbox)
        self.listbox.delete.assert_called_once_with(0)  # Verifica se a nota foi removida

    @patch('tkinter.messagebox.showwarning')
    def test_delete_note_no_selection(self, mock_warning):
        self.listbox.curselection.return_value = []  # Simula que nenhuma nota está selecionada
        delete_note(self.listbox)
        mock_warning.assert_called_once_with("Aviso", "Nenhuma nota selecionada.")  # Verifica o aviso

if __name__ == '__main__':
    unittest.main()
