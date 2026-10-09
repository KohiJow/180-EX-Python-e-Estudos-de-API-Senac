#(01)Setup (Configuração Inicial)
#É a configuração inicial para personalizar o uso do Git, como seu nome e e-mail, para que 
#todos os commits possam ser atribuídos corretamente.
'''
git config --global user.name "João Mateus Firmino Rodrigues"
git config --global user.email "contatojmfr@gmail.com"
git config --global color.ui auto  # Ativa cores no terminal para facilitar leitura
'''

#(02)Setup e Init (Configuração e Inicializção)
#Inicia um novo repositório em um diretório local ou clona um repositório remoto para sua máquina.
'''
git init                    # Cria um novo repositório Git no diretório atual
git clone <url>             # Clona um repositório remoto para o seu computador
'''

#(03)Stage e Snapshot 
#O processo de "stage" é quando você adiciona arquivos ao staging area, uma área 
# intermediária onde as mudanças são preparadas para serem gravadas. Já o snapshot é o 
# registro permanente dessas mudanças no histórico do Git.
'''
git branch <nome>           # Cria uma nova branch
git checkout <nome>         # Troca para a branch desejada
git checkout -b <nome>      # Cria e troca para uma nova branch
git merge <branch>          # Mescla a branch especificada com a atual
'''

#(04)Branch e Merge (Ramificação e Mesclagem)
#Uma branch é uma linha independente de desenvolvimento. A criação de branches permite que 
#você trabalhe em diferentes recursos ou correções sem interferir no desenvolvimento 
#principal. Merge é o processo de integrar as mudanças de uma branch a outra.

'''
git branch <nome>           # Cria uma nova branch
git checkout <nome>         # Troca para a branch desejada
git checkout -b <nome>      # Cria e troca para uma nova branch
git merge <branch>          # Mescla a branch especificada com a atual
'''

#(05)Inspect e Compare (Inspecionar e Comparar) 
#Esses comandos permitem que você veja o histórico de mudanças e compare versões de 
# arquivos no repositório, útil para verificar diferenças antes de um merge ou para revisão.
'''
git log                     # Exibe o histórico de commits
git log --oneline           # Exibe o histórico resumido
git diff                    # Compara as mudanças não comitadas no código
git diff <branch1> <branch2> # Compara mudanças entre duas branches
'''

#(06)Share e Update (Compartilhar e Atualizar)
#Para colaborar com outras pessoas, você precisa compartilhar e atualizar as mudanças 
# regularmente. Isso envolve enviar seus commits para um repositório remoto e trazer 
# alterações que outros fizeram.
'''
git push origin <branch>    # Envia mudanças para o repositório remoto
git pull                    # Puxa mudanças do repositório remoto para o local
git fetch                   # Puxa mudanças do remoto sem mesclar automaticamente
'''

#(07)Tracking Path Changes (Rastreamento de Mudanças de Caminho)
#Git permite rastrear mudanças de nome e movimentação de arquivos. 
#É importante para manter o histórico e a integridade do código.
'''
git mv <antigo> <novo>      # Move ou renomeia um arquivo e rastreia a mudança
git rm <arquivo>            # Remove um arquivo do repositório e do sistema
'''

#(08)Rewrite History (Reescrever Histórico)
#Permite ajustar commits antigos, seja corrigindo mensagens, juntando commits 
# ou mesmo apagando commits problemáticos. 
# Isso pode ser útil em projetos pessoais, mas precisa de cuidado em projetos colaborativos.
'''
git commit --amend          # Edita o último commit
git rebase -i HEAD~n        # Abre os últimos n commits para edição interativa
'''

#(09)Temporary Commits (Commits Temporários)
#Quando você quer guardar temporariamente mudanças em progresso sem criar um commit formal, o 
# comando stash é útil. 
# Ele armazena mudanças para recuperação posterior, permitindo que você volte 
# a um estado limpo.
'''
git stash                   # Salva as mudanças temporariamente
git stash pop               # Restaura as mudanças temporárias para o workspace
'''

#(10)Ignoring Patterns (Ignorando Padrões)
#Para evitar que certos arquivos ou pastas sejam rastreados pelo Git (como arquivos temporários ou de configuração local) 
# você pode definir padrões de exclusão.
'''
Criar um arquivo .gitignore e listar os arquivos ou padrões que você quer ignorar
# Exemplo de .gitignore
*.log
node_modules/
*.temp
'''