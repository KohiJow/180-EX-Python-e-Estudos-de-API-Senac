#Sem o modulo tkinter (em Linux ele e um pacote separado, python3-tk), os tres
#arquivos abaixo nem importam. Em vez de derrubar a colecao inteira, eles ficam de fora
#e os testes puros da calculadora continuam rodando.
try:
    import tkinter  # noqa: F401
except ImportError:
    collect_ignore = [
        'test_calculadorainterfaceFernando.py',
        'test_gerenciador_anotacoesprf.py',
        'test_gerenciador_unittest.py',
    ]
