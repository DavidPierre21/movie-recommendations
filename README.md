# Sistema de recomendação simples utilizando KNN

## Requerimentos
* Python2

## Como executar
Clone este repositório, navegue até o diretório do projeto e execute

`python recommender.py`


## Modificando a entrada do algoritmo
Abra o arquivo ratings.dat, que está dentro da pasta ml-1m
Vá até as últimas linhas do arquivo. O usuário está configurado como o id 6041
Modifique o arquivo.

```6041::1::4::Toy Story
6041::110::5::Braveheart
6041::1732::5::The Big Lebowski
6041::157::2::Canadian Bacon
6041::182::1::Moonlight and Valentino
6041::1693::3::Amistad
6041::393::1::Street Fighter
```

[ID DO USUARIO]::[ID DO FILME]::[NOTA]::[TIMESTAMP, MAS COMO NÃO É USADO, COLOQUE O NOME DO FILME PARA FICAR MAIS FÁCIL A LEITURA E MODIFICAÇÃO]

Os filmes e seus respectivos IDs se encontram no arquivo movies.dat

Para mais informações, olhe o arquivo README da pasta ml-1m
