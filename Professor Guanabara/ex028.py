#Escreva um programa que faça o computador "pensar" em um número entre 0 e 5
#e peça para o usuário tentar descobrir qual foi o número
#escolhido pelo computador.
#O programa deverá escrever na tela se o usuário venceu ou perdeu.
"""""
from random import randint

computador = randint(0, 5)
user = int(input('Tente advinhar em que número estou pensando entre 1 a 5: '))

if user == computador:
    print('Caramba você lê mentes? era esse mesmo!')
#elif type(user) != int:
#    print('Insira um número de 1 a 5 burro')
else:
    print(f'Ha! Errou! eu pensei no {computador}')

#Correção do que eu queria fazer, basicamente eu queria muito fazer um verificador sem try
#pois eu sei que em str eu aprendi sobre identificadores e tipos, porém não tava conseguindo pensar
#na lógica pra fazer isso, e acabou que dava, com bastante if e else mas deu:
"""
"""
import random

num = [1,2,3,4,5]

user_input = (input('Tente advinhar em que número estou pensando entre 1 a 5: ')).strip()

if user_input.isdigit():
    user = int(user_input)
    if user in num:
        if user == random.choice(num):
            print('Caramba você lê mentes? era esse mesmo!')
        else:
            print('Ha! Errou!')
    else:
        print('Insira um número entre 1 e 5!')
else:
    print('Insira um valor válido!')
"""

#Abaixo irei colocar a correção do guanabara


from random import randint
from time import sleep
computador = randint(0,5) #Faz o computador "Pensar"
print('-=-' *20)
print('Vou pensar em um número entre 0 e 5. Tente adivinhar...')
print('-=-' *20)

jogador = int(input('Em que número eu pensei? ')) #Jogador tenta advinhar
print('PROCESSANDO...')
sleep(3)

if jogador == computador:
    print('PARABÉNS! Você conseguiu me vencer!')
else:
    print(f'GANHEI! Eu pensei no número {computador} e não no {jogador}')
