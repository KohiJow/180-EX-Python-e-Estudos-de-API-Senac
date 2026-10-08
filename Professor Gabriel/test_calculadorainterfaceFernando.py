import pytest
from calculadoraFernando import Calculator

@pytest.fixture
def calc():
    #Cria a instancia da classe calculator para cada teste
    return Calculator()

#Clique de adição
def test_addition(calc):
    calc.click("1")
    calc.click("+")
    calc.click("2")
    calc.click("=")
    #verifica se o resultado na tela é "3"
    assert calc.get_screen() == "3"
    
    #Testa função de limpar
def test_clear(calc):
    calc.click("5")
    calc.click("C")
    assert calc.get_screen() == ""
    

#Casos de borda do fluxo de cliques

def clicar(calc, teclas):
    for tecla in teclas:
        calc.click(tecla)

def test_multi_digit_numbers(calc):
    clicar(calc, "12+34=")
    assert calc.get_screen() == "46"

def test_division_with_float_result(calc):
    clicar(calc, "7/2=")
    assert calc.get_screen() == "3.5"

def test_division_by_zero_shows_error(calc):
    clicar(calc, "1/0=")
    assert calc.get_screen() == "Erro"

def test_equals_with_empty_screen_shows_error(calc):
    calc.click("=")
    assert calc.get_screen() == "Erro"

def test_incomplete_expression_shows_error(calc):
    clicar(calc, "2+=")
    assert calc.get_screen() == "Erro"

def test_clear_after_error(calc):
    clicar(calc, "1/0=")
    calc.click("C")
    assert calc.get_screen() == ""

def test_continue_operating_on_result(calc):
    #o resultado vira o inicio da proxima expressao, como numa calculadora de bolso
    clicar(calc, "2+2=")
    clicar(calc, "*3=")
    assert calc.get_screen() == "12"

def test_precedence_without_parentheses(calc):
    clicar(calc, "2+3*4=")
    assert calc.get_screen() == "14"

def test_clear_on_empty_screen_keeps_empty(calc):
    calc.click("C")
    assert calc.get_screen() == ""
