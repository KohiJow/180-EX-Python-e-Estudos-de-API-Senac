#Crie um programa que leia o nome de uma pessoa e diga se ela tem "Silva" no nome.
#Create a program who reads the name of an person and tells if have "Silva" in the name

#Nome = str(input('Qual seu nome? '))
#Silva = 'Silva'

#print(Silva in Nome)

###Correção

nome = str(input('Whats your name? ')).strip()
print(f'Your name have silva? {"SILVA" in nome.upper()}')
