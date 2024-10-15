# Fuzzy KBS para empréstimos bancários
## Sistema Baseado em Conhecimento com Scikit-Fuzzy para diagnóstico de risco de empréstimo a clientes de um banco

Antes de executar o programa, instale pacotes necessários com o comando seguinte:

`pip install numpy scikit-fuzzy scipy packaging networkx`

O programa recebe como entrada uma avaliação do histórico de crédito e da dívida do cliente, assim como sua renda. O programa retorna o fator de risco de realizar um empréstimo, e explica brevemente a lógica por trás do cálculo.

A Base de Conhecimento deste sistema é baseada numa árvore de decisão gerada pelo algoritmo C4.5 aplicado à seguinte tabela:

![decisiontree](https://github.com/user-attachments/assets/2ebca49c-c758-4026-a681-8e2421220142)

A variável "Garantia" foi removida por a) ser totalmente discreta e b) não ter tanto peso na árvore de decisão.
