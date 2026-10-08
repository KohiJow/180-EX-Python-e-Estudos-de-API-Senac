'''
Validação do pedido de socorro: S.o.S que é igual à: ...---... em código Morse

CURIOSIDADE:

O código Morse foi usado para enviar mensagens via telegráfo e o mesmo foi
desenvolvido por: Samuel Finley Breese "Morse", criado em 1835.
'''

print('\n')
l0 = '-----------------------------------------------------------------------------------'
l1 = '......................................'

print(l1)
msg_help = input(' --- Digite o pedido de ajuda em Morse: ')
print(l1)

tabela_morse = [' ...---... ','S.O.S']

if msg_help == tabela_morse[0]:
    print('\n' + l0)
    print(' O código digitado foi: {} e foi ACEITO!, a mensagem e: {}'. format(msg_help, tabela_morse[1] ) )
    print(l0)

else:
    print('\n' + l0)
    print(' Codigo NAO confere com a tabela Morse, referente a mensagem: {}' .format(tabela_morse[1] ) )
    print(l0)

#Autor: material de aula do professor Fernando
