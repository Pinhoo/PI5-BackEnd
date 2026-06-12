# REPORT

## Jogador Inteligente – Estratégia

Fizemso nossa IA utilizando busca em árvores de decisão, com o objetivo de selecionar a melhor jogada possível a cada turno com base no estado do jogo

### Visão Geral

A estratégia foi feita implementando **Minimax com poda Alpha-Beta** por vários motivos, mas o principai sendo de que é um bom algoritmo para jogos de tabuleiro determinísticos. A cada turno, o agente testa as jogadas dele e do adversário e busca qual a melhor jogada possível.

### Algoritmo Utilizado

#### Minimax

O algoritmo Minimax vê o jogo como uma árvore de decisões composta por dois jogadores e a IA busca maximizar sua pontuação enquanto assume que o adversário tomará sempre a melhor decisão possível (O que é melhor ainda considerando que o adversário também é uma IA)

Utilizamos a profundidade de busca 2 por questão de ser a maior profundidade possível antes do algoritmo dar timeout durante os nossos testes

### Função Heurística

A pontuação das jogadas é calculada levando em base:

#### 1. Altura Atual do Professor

Professores posicionados em níveis mais altos recebem maior pontuação.

Já que posições maiores aproximam o jogador das condições de vitória.

#### 2.  Células de Nível 2 adjacentes

A função avalia a quantidade de células de nível 2 adjacentes aos professores, considerando oportunidades de vitória nos próximos turnos.

#### 3. Controle do Centro

Assim como no xadrez, o centro do tabuleiro possui maior mobilidade e acesso a mais posições.

#### 4. Ameaças Imediatas

Professores oponentes que podem subir para o Nível 3 são uma ameaça imediata, o que reduz a pontuação final da jogada

### Condições de Vitória

Antes de aplicar a heuristica o jogador identifica se não tem nenhuma chance de subir uma casa para o nivel 3, vencendo o jogo.
É importante ignorar a heuristica nesse caso pois garante que o jogo vai ser ganho na primeira chance

### Estratégia de Setup

O algoritmo busca casas livres com menor distância do centro do tabuleiro eq uando existem múltiplas posições equivalentes, a escolha é realizada de forma aleatória para evitar previsibilidade.

### Processo de Testes

Os testes foram realizados por meio de partidas simuladas entre diferentes configurações do agente.

Durante o desenvolvimento o maior problema que enfrentamos foi o debug no simulador original, já que era dificil vizualizar o que estava acontecendo, então apenas criamos um codigo em loop que testava 200 partidas e dizia quantas cada time venceu quando eram concluidas todas as rodadas
Outro problema que enfrentamos foi de que, quando começamos a testar via API, o jogador estava dando timeout por conta de uma profundidade muito grande na busca, por isso a profundidade foi definida para 2.
