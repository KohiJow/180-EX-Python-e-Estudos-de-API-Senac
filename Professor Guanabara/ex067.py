"""
Faca um programa que mostre a tabuada de varios numeros, um de cada vez para cada valor digitado pelo usuário.
O programa será interrompido quando o número solicitado for negativo
"""
num = int(input("Insira um numero para a tabuada, ou insira um numero negativo para encerrarmos: ")) 
verificador = isinstance(num, int)
count = 0

while num > 0:
    for _ in range(0,11):
        print(f"{num} x {count}= {num * count}")    
        count +=1
    if count > 10:
        num = int(input("Insira um numero para a tabuada denovo, ou insira um numero negativo para encerrarmos: ")) 
        count = 0
    
    
    