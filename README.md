# Analisador Sintático

---

## Requisitos



---

## Execução

Para rodar o programa: `python3 main.py` na raíz do diretório.

### Formato da gramática

- TODOS os símbolos devem ser separador por espaços.
- Cada produção deve ser feita em uma linha.
- O símbolo inicial da gramática deve ser o primeiro da primeira linha. 
- Exemplo:
    - Símbolo inicial: S.
    - Não terminais: S, A, B.
    - Terminais: a, b, c.
    ```
    S -> S c
    S -> A a
    S -> c
    A -> S a
    A -> B b
    A -> a
    B -> S c
    B -> B b    
    ```

---

## Objetivos

O modelo de analisador escolhido foi o preditivo LL(1).

- Algoritmos a serem implementados:
  - [x] Eliminação de recursão à esquerda.
  - [x] Fatoração.
  - [x] First.
  - [x] Follow.
  - [x] Geração da tabela de análise.
  - [x] Autômato de pilha.
  
- Interface de Projeto deve receber e validar a gramática livre de contexto que descreve a linguagem.
- Fluxo de Execução:
  - [x] Leitura token a token.
  - [x] Uso da tabela de análise para validação da sentença de entrada.
  - [x] Saída: mensagem validando ou invalidando o código.
  
---

## Observações

- Para notacionar o &epsilon; usar o &.
- A tabela de análise deve poder ser visualizada.

---
