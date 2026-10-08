#Exercicio 2º - Tuplas no Python

#Lista para armazenar os funcionários
funcionarios = []

def adicionar_funcionario(nome, cargo, salario):
    funcionario = (nome, cargo, salario)
    funcionarios.append(funcionario)
    
def exibir_funcionarios():
    for funcionario in funcionarios:
        nome, cargo, salario = funcionario
        print(f'Nome: {nome}, Cargo: {cargo}, Salário: R$ {salario:.2f}')

#Adicionando funcionários
adicionar_funcionario('Carlos', 'Gerente', 5000.00)
adicionar_funcionario('Ana', 'Vendedora', 3000.00)

#Exibindo funcionários cadastrados
exibir_funcionarios()
