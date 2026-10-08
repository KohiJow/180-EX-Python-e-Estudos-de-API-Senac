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

    #Casos de borda: o que a calculadora faz fora do caminho feliz

    def test_division_with_float_result(self):
        self.assertEqual(self.calculator.evaluate_expression('7 / 2'), 3.5)

    def test_integer_division_and_modulo(self):
        self.assertEqual(self.calculator.evaluate_expression('7 // 2'), 3)
        self.assertEqual(self.calculator.evaluate_expression('10 % 3'), 1)

    def test_operator_precedence_and_parentheses(self):
        self.assertEqual(self.calculator.evaluate_expression('2 + 3 * 4'), 14)
        self.assertEqual(self.calculator.evaluate_expression('(2 + 3) * 4'), 20)

    def test_negative_numbers(self):
        self.assertEqual(self.calculator.evaluate_expression('-3 + 1'), -2)
        self.assertEqual(self.calculator.evaluate_expression('5 - -2'), 7)

    def test_exponent_and_large_numbers(self):
        self.assertEqual(self.calculator.evaluate_expression('2 ** 10'), 1024)
        self.assertEqual(self.calculator.evaluate_expression('999999999 * 999999999'), 999999998000000001)

    def test_surrounding_spaces_are_ignored(self):
        self.assertEqual(self.calculator.evaluate_expression('   2 + 2   '), 4)

    def test_empty_expression(self):
        self.assertEqual(self.calculator.evaluate_expression(''), 'Erro')
        self.assertEqual(self.calculator.evaluate_expression('   '), 'Erro')

    def test_incomplete_expression(self):
        self.assertEqual(self.calculator.evaluate_expression('2 +'), 'Erro')
        self.assertEqual(self.calculator.evaluate_expression('(2 + 3'), 'Erro')

    def test_non_string_input(self):
        #eval(None) levanta TypeError, que tambem tem que virar 'Erro'
        self.assertEqual(self.calculator.evaluate_expression(None), 'Erro')

    def test_float_division_by_zero(self):
        self.assertEqual(self.calculator.evaluate_expression('1.5 / 0'), 'Erro')

#Executa os testes, terminal (diretamente)        
if __name__ == '__main__':
    unittest.main()
    
    #Executando!!!!
    # ---> python -m unittest test_calculator.py <---