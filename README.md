# PrefixTrees

- usar array: muita memória
              só seria bom se estivesse tudo nas folhas mas perdia-se informação dos nós intermédios: apenas um acesso

- delete: iterativo vs recursivo vs guardar último
          iterativo:

https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=749256

https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-98-59.pdf

http://cseweb.ucsd.edu/~varghese/PAPERS/TOCS99.pdf

http://conferences.sigcomm.org/sigcomm/1997/papers/p182.pdf

http://www.cs.cmu.edu/~dga/15-744/S07/papers/D+97.pdf


ORTC

melhorias implementadas:
- fazer o passo 1 e 2 juntos
- no passo 3 escolher o que já lá estava: ao concatenarmos sempre e escolhermos o primeiro, fazemos isso
- não haver e: cria-se um nexthop dummy "drop" e no fim retira-se se tiver ficado na root. se não tiver ficado, este é descartado no lookup
