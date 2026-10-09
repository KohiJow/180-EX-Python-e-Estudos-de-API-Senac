# Python no Senac: exercícios, testes e APIs

[![testes](https://github.com/KohiJow/180-EX-Python-e-Estudos-de-API-Senac/actions/workflows/testes.yml/badge.svg)](https://github.com/KohiJow/180-EX-Python-e-Estudos-de-API-Senac/actions/workflows/testes.yml)

Tudo que eu escrevi em Python durante o técnico no Senac, mais o que fiz por fora
estudando. São 228 arquivos `.py`, divididos por professor, porque foi assim que
as aulas aconteceram.

Não é um projeto único: é um caderno de código. Mantenho aqui porque mostra a
progressão, do `print('Hello, World!')` até API em Flask com teste automatizado.

Se você está avaliando o repositório pelo lado de QA, pule direto para
[Testes automatizados](#testes-automatizados) e [APIs em Flask](#apis-em-flask).
É a parte que tem a ver com o que eu faço hoje.

## Como rodar

Python 3.9 ou mais novo (o CI roda a suíte em 3.9, 3.11 e 3.13). Os exercícios
em si não têm dependência; a API e os testes usam o que está em
`requirements.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Para rodar um exercício pelo número, sem digitar o caminho com espaço:

```bash
python rodar.py guanabara 45         # roda "Professor Guanabara/ex045.py"
python rodar.py fernando 31          # roda "Professor Fernando/EX031.py"
python rodar.py fernando desafio02   # também aceita o nome do arquivo
python rodar.py guanabara 115a
python rodar.py gabriel --lista      # mostra o que existe na pasta
```

O exercício roda com a pasta dele como diretório atual, então arquivo aberto
por nome relativo (como o `arquivo.txt` do `EX040`, que não vem no repositório)
é procurado ali. O código de saída do exercício é repassado. Chamar direto
continua funcionando:

```bash
python3 "Professor Guanabara/ex045.py"
```

Alguns arquivos usam biblioteca que fica fora do `requirements.txt`, por serem
de janela ou áudio: `pygame` (`ex021`), `PyQt5` (`PyQt.py`, `helloworld.py`,
`gerenciadordeanotacoes_pyqt.py`) e `selenium` (`selene.py`). Os de `tkinter`
precisam do pacote `python3-tk` em Linux; no Windows e no macOS ele já vem.

## Testes automatizados

Um comando, na raiz, roda tudo:

```bash
python -m pytest
```

São 328 testes, divididos assim:

| Onde | Quantos | O que cobre |
| --- | --- | --- |
| `Professor Gabriel/` | 36 | As duas calculadoras e o gerenciador de notas, em pytest e em unittest |
| `ProfessorKauan/PICHAU/tests/` | 40 | Cada rota da API PICHAU, com `test_client`, sucesso e erro |
| `test_exercicios.py` | 225 | Todo `.py` do repositório compila (pega erro de sintaxe e escape inválido em caminho) |
| `test_rodar.py` | 27 | A busca por número do `rodar.py` e a linha de comando, com stdin fechado para não travar em `input()` |

O `pytest.ini` lista as pastas, então não precisa de argumento. A suíte também
roda a cada push no GitHub Actions (`.github/workflows/testes.yml`).

### Pasta `Professor Gabriel`

Essa parte foi o primeiro contato com teste escrito em código, e é a mais
relevante do repositório.

| Arquivo | O que cobre |
| --- | --- |
| `app.py` | Classe `Calculator` com um método `evaluate_expression`, o alvo dos testes |
| `test_calculator_pytest.py` | Soma e subtração via pytest, com `@pytest.fixture` |
| `test_calculator_unitte_native.py` | Mesma lógica em `unittest`, mais os casos de borda: divisão com decimal, precedência e parênteses, negativo, expoente, expressão vazia ou incompleta, entrada que não é string, divisão por zero |
| `calculadoraFernando.py` | Calculadora em tkinter com a lógica isolada numa classe, justamente para poder testar sem abrir a janela |
| `test_calculadorainterfaceFernando.py` | Fluxo de cliques (`1`, `+`, `2`, `=`), limpar, número de mais de um dígito, erro na tela, limpar depois do erro, continuar a conta em cima do resultado |
| `gerenciadordeanotacoesprf.py` | Gerenciador de notas em tkinter, com `add_note` e `delete_note` recebendo o listbox por parâmetro. A janela só abre quando o arquivo roda direto, por isso dá para importar as funções no teste |
| `test_gerenciador_anotacoesprf.py` | pytest com `MagicMock` no listbox e `patch` nos diálogos do tkinter |
| `test_gerenciador_unittest.py` | A mesma suíte em `unittest` (o arquivo estava sem extensão `.py` e o pytest não coletava) |
| `conftest.py` | Se `tkinter` não estiver instalado, deixa os três testes de interface de fora em vez de derrubar a coleção |
| `gerenciadordeanotacoes_pyqt.py` | O mesmo gerenciador reescrito em PyQt5, como classe |

Os testes importam o módulo vizinho direto (`from app import Calculator`). Pelo
`python -m pytest` na raiz isso já funciona; para rodar um arquivo isolado, entre
na pasta:

```bash
cd "Professor Gabriel"
python -m pytest test_calculator_pytest.py test_calculadorainterfaceFernando.py
python -m unittest test_calculator_unitte_native.py
```

O que ficou de lição aqui: separar lógica de interface é o que torna o teste
possível. A `Calculator` do `calculadoraFernando.py` existe fora do tkinter de
propósito, e o gerenciador de notas só passou a ser testável quando a criação
da janela saiu do nível do módulo.

Também tem `selene.py`, um primeiro teste em Selenium que abre a tela de login do
Instagram no Edge e confere o `title`. Usa `time.sleep` e credencial de exemplo,
não é para rodar, é registro de como eu começei com browser.

## Consumo de API

`Professor Gabriel/request.py`: GET em `jsonplaceholder.typicode.com/users/10`
com `requests`, `raise_for_status()` e tratamento de `RequestException`.
Curto, mas é o esqueleto que eu uso até hoje em teste de API.

## APIs em Flask

Pasta `ProfessorKauan`. Duas APIs REST com SQLite.

### PICHAU: catálogo de eletrônicos

A mais completa das duas. Depois do curso eu reorganizei em pacote com app
factory, para conseguir testar com banco em memória:

```
ProfessorKauan/PICHAU/
  app.py                  cria a aplicação e sobe o servidor
  pichau/__init__.py      create_app(config): monta Flask, banco, rotas e erros
  pichau/routes.py        blueprint com as cinco rotas
  pichau/controllers.py   regra de cada rota
  pichau/validacao.py     confere tipo, obrigatoriedade e faixa de cada campo
  pichau/erros.py         formato único de erro em JSON
  pichau/models.py        tabela Eletronicos
  pichau/dados.py         catálogo de exemplo, carregado quando a tabela está vazia
  pichau/db.py            instância do SQLAlchemy
  tests/test_eletronicos.py
```

| Método | Rota | Comportamento |
| --- | --- | --- |
| GET | `/Eletronico` | Lista tudo, com `total` |
| GET | `/Eletronico/<id>` | Retorna o item, ou 404 |
| POST | `/Eletronico` | Cadastra. Exige `nome`, `categoria`, `preco`, `modelo` e `ano`. Responde 201 com cabeçalho `Location` |
| PUT | `/Eletronico/<id>` | Atualiza só os campos enviados. 404 se não existir, 400 se vier vazio ou inválido |
| DELETE | `/Eletronico/<id>` | Remove e devolve o item removido. 404 se não existir |

Validação: `nome`, `categoria` e `modelo` são texto não vazio de até 80
caracteres (os espaços das pontas são aparados); `preco` é número maior que
zero, arredondado em duas casas; `ano` é inteiro entre 1950 e o ano que vem.
Campo desconhecido também é rejeitado. Todos os problemas voltam de uma vez:

```json
{"erro": "Bad Request", "mensagem": "Dados invalidos.", "detalhes": ["preco e obrigatorio.", "ano e obrigatorio."]}
```

Todo erro sai em JSON nesse mesmo formato (`erro`, `mensagem` e, quando tem,
`detalhes`): 400 para corpo inválido ou JSON mal formado, 404 para id ou rota
inexistente, 405 para método errado (com o cabeçalho `Allow`), 415 quando o corpo
não vem com `Content-Type: application/json` e 500 para erro não previsto.

```bash
cd ProfessorKauan/PICHAU
python app.py                      # http://127.0.0.1:5000 (PORT=8080 python app.py para trocar)
# em outro terminal
curl -s localhost:5000/Eletronico
curl -s -i -X POST localhost:5000/Eletronico \
  -H 'Content-Type: application/json' \
  -d '{"nome":"Monitor","categoria":"Periferico","preco":899.9,"modelo":"27 polegadas","ano":2024}'
curl -s -X PUT localhost:5000/Eletronico/7 -H 'Content-Type: application/json' -d '{"preco":799}'
curl -s -X DELETE localhost:5000/Eletronico/7
curl -s -i localhost:5000/Eletronico/999   # 404 em JSON
```

Na primeira execução o banco é criado em `instance/eletronicos.db` (não vai
versionado) com seis itens de exemplo, os de `pichau/dados.py`.

Os testes (`python -m pytest ProfessorKauan/PICHAU`) criam a aplicação com
`sqlite://` em memória, então cada teste começa do zero e nada é gravado em
disco. Cobrem cada rota com `test_client`, os limites da validação
(`parametrize`), o catálogo inicial, JSON mal formado, sem `Content-Type`,
rota inexistente, método não permitido e um erro inesperado virando 500.

### CARROS: cadastro de carros

Mais simples e inacabada. Só tem `POST /Carro`, que cadastra modelo, marca e ano.
Não existe GET, DELETE nem validação de campo obrigatório. Deixei como está por
ser o estado real em que a aula terminou.

```bash
cd ProfessorKauan/CARROS
python app.py
curl -s -X POST localhost:5000/Carro \
  -H 'Content-Type: application/json' \
  -d '{"modelo":"Gol","marca":"VW","ano":2015}'
```

## Exercícios do curso do Guanabara

Pasta `Professor Guanabara`, 123 arquivos. Seguem a numeração do curso em vídeo.

| Faixa | Tema |
| --- | --- |
| `ex001` a `ex015` | Entrada e saída, operadores, conversão de tipo, contas (média, unidades, desconto, reajuste, Celsius para Fahrenheit) |
| `ex016` a `ex021` | Módulos `math`, `random` e `datetime`. O `ex021` toca um MP3 com `pygame` |
| `ex022` a `ex027` | Strings: `upper`, `lower`, `split`, `count`, `find`, fatiamento |
| `ex028` a `ex045` | Condições. `if` / `elif` / `else`, condições aninhadas, jogos com `random` (adivinhar número, jokenpô) |
| `ex046` a `ex071` | Repetição. `for`, `while`, acumulador, contador, menu, validação de entrada, caixa eletrônico |
| `ex072` a `ex077` | Tuplas |
| `ex078` a `ex088` | Listas, listas dentro de listas e matriz 3x3 |
| `ex089` a `ex095` | Listas e dicionários combinados: cadastro de aluno, de pessoa e aproveitamento de jogador |
| `ex096` a `ex113` | Funções: parâmetro opcional, `*args`, docstring, módulo próprio e pacote |

Arquivos de anotação soltos na mesma pasta: `Condicões.py`, `CondiçõesAninhadas.py`,
`Estrutura de Repetição.py`, `Manipulando Texto.py`, `a10.py` e `cor.py`
(tabela de cor ANSI para o terminal).

Honestidade sobre o que falta: `ex114` (testar se um site responde) e
`ex115a` / `ex115b` / `ex115c` (leitura e escrita de arquivo) têm só o enunciado,
sem solução. O `ex114` é o que mais me interessa hoje e é exatamente o que
acabei fazendo depois no `request.py`.

## Exercícios do professor Fernando

Pasta `Professor Fernando`, 70 arquivos. Numeração própria, foco em lista e laço
aplicados a situação de negócio (estoque, meta de venda, fatura, cadastro).

| Faixa | Tema |
| --- | --- |
| `ex001` a `ex005`, `DESAFIO01` a `DESAFIO03`, `TIPOSPRIMITIVOS.py` | Básico e tipos primitivos |
| `EX006` a `EX015` | Função com `def`, concatenação, f-string e formatação de alinhamento (`<`, `^`, `>`) |
| `EX016` a `EX033` | `for` e `while` sobre listas, `enumerate`, `break`, `continue`, `for` dentro de `for`. O `EX031` é uma calculadora com `try` / `except` |
| `EX034` a `EX053` | Listas: `append`, `pop`, índice negativo, `len`, `max`, `min`, `reduce` do `functools`. Termina em quatro exercícios maiores (estoque de papelaria, classificação de aluno, cadastro de evento, análise de fatura) |
| `EX054` a `EX059` | Dicionários |
| `EX060` a `EX065` | Tuplas |

Fora da faixa: `EX040` abre arquivo `.txt` com `with open` e trata
`FileNotFoundError`, e `EX041` é o exercício de `try` / `except` numa divisão.

`csv.py` é um rascunho abandonado de `pandas` com `matplotlib`. Não tem sintaxe
válida, nunca rodou. Deixei para não apagar histórico, mas não conte com ele
(é o único arquivo que o `test_exercicios.py` ignora).

## O que mudou depois do curso

Os exercícios estão como foram escritos na aula, com uma exceção: o que não
rodava de jeito nenhum ganhou a correção mínima. Caminho do Windows com `\U`
que nem compila (`ex021`), aspas iguais dentro da f-string que só o 3.12 aceita
(`ex025`), atributo que não existe (`ex022`, `ex067`), chave de dicionário com
acento diferente da declarada (`EX054`), `append` da própria lista (`EX062`),
`tk.TK` e `comand` no hello world do tkinter. A lógica de cada um ficou a mesma.

O resto do que mudou está descrito nas seções acima: testes que rodam de uma vez
só, a API PICHAU reorganizada e o `rodar.py`.

## Contato

João Mateus Firmino Rodrigues, QA Engineer | contatojmfr@gmail.com
