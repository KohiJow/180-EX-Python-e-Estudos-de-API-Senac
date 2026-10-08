import unittest #importa a biblioteca para testes
from app import Calculator #Importa a classe calculator

#Define uma nova classe de teste, no qual herda as funções do Unitest
class TestCalculatorLogic(unittest.TestCase):
    
    def setUp(self):
        self.calculator = Calculator()#cria a instancia da Calculadora
        
    def test_addition(self):
        self.assertEqual(self.calculator.evaluate_expression('2+2'), 4)
        
    def test_subtraction(self):
        self.assertEqual(self.calculator.evaluate_expression('5-3'), 2)
    
    def test_multiplication(self):
        self.assertEqual(self.calculator.evaluate_expression('4 * 5'), 20)
    
    def test_division_by_zero(self):
        self.assertEqual(self.calculator.evaluate_expression('10 / 0'), 'Erro')
    
    #tinha o mesmo nome do teste acima e apagava ele: so a divisao por zero rodava
    def test_invalid_expression(self):
        self.assertEqual(self.calculator.evaluate_expression('invalid'), 'Erro')    
#Executa os testes, terminal (diretamente)        
if __name__ == '__main__':
    unittest.main()
    
    #Executando!!!!
    # ---> python -m unittest test_calculator.py <---