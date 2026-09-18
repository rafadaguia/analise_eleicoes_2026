# Pesquisas eleitorais x resultado real — Brasil (2010–2026)

Script em Python que compara pesquisas eleitorais pré-eleição com o resultado
real nas urnas nas presidenciais brasileiras de 2010, 2014, 2018 e 2022, para
investigar se existe um viés sistemático de subestimação do bolsonarismo nas
pesquisas — e usa isso para projetar cenários para 2026.

## O que o script faz

1. **Ajusta um modelo de regressão** (pesquisa → resultado real) com dados
   agregados de 2018 e 2022, para 1º e 2º turno.
2. **Valida fora da amostra** (leave-one-election-out): treina com uma
   eleição, testa na outra, para medir o erro real de generalização — não
   só o ajuste dentro da própria amostra de treino.
3. **Calcula o viés histórico** (pesquisa − resultado real) restrito a dois
   grupos específicos: candidatos petistas (Haddad 2018, Lula 2022) e
   candidatos bolsonaristas (Bolsonaro 2018, Bolsonaro 2022) — não um viés
   genérico de "esquerda x direita".
4. **Usa 2010 e 2014 como referência histórica** (não entram no ajuste do
   modelo) para checar se esse viés já existia antes de 2018 ou é um
   fenômeno mais recente.
5. **Projeta cenários para 2026** com pesquisas disponíveis em setembro de
   2026, aplicando os dois modelos (regressão e viés por linhagem) e
   reportando intervalo de incerteza — não só um número-ponto.
6. Gera dois gráficos de dispersão (`consolidado_1turno_v2.png` e
   `consolidado_2turno_v2.png`) com os pontos de treino, ajuste e
   referência histórica.

## Principais achados

- No 2º turno, o viés de pesquisa contra o bolsonarismo é recente: em
  2010 e 2014 as pesquisas finais praticamente acertaram o resultado
  (erro médio de ~0,2 ponto); em 2018 e 2022, o erro sobe para ~1,3 ponto,
  sempre na mesma direção (subestimando o candidato bolsonarista).
- No 1º turno o quadro é mais misto: 2014 também teve um erro grande
  (Aécio Neves), mas por um mecanismo diferente — uma virada tática de
  última hora, não um viés sustentado ao longo de toda a janela
  pré-eleitoral, como parece ser o caso do bolsonarismo desde 2018.
- O viés específico de subestimação do bolsonarismo (~6,5 pontos) se
  repete de forma quase idêntica em 2018 e 2022 — o que sugere um padrão,
  não coincidência.

## Limitações (assumidas no próprio código, não escondidas)

- O modelo é treinado com apenas 2 eleições "no regime pós-2018" (2018 e
  2022) — estatisticamente é pouco dado, e os intervalos de incerteza
  reportados são propositalmente largos por causa disso.
- Pesquisas de 2026 usadas como entrada são anteriores à janela final de
  2 semanas antes do pleito (dado ainda não disponível na data da
  análise).
- Parte dos dados de pesquisa precisou ser recalculada para uma base
  comparável (votos válidos) a partir de estimativas de indecisos/brancos/
  nulos — essas linhas estão marcadas como `"ajustado"` no código, para
  ficarem rastreáveis e não se misturarem silenciosamente com valores
  publicados diretamente pelos institutos.

## Como rodar

```bash
pip install numpy scipy matplotlib
python3 analise_eleicoes_consolidado_v2.py
```

## Fontes dos dados

Pesquisas e resultados de 2018/2022: Datafolha, Ipec, XP/Ipespe,
PoderData, Paraná Pesquisas. Referência histórica de 2010/2014:
Datafolha e Ibope (via Wikipédia — "Opinion polling for the 2010
Brazilian presidential election" e "Eleição presidencial no Brasil em
2014"). Resultados oficiais: Tribunal Superior Eleitoral (TSE).

## Aviso

Isto é uma análise exploratória, não uma previsão eleitoral oficial. Os
números carregam incerteza estatística real (ver intervalos reportados
pelo próprio script) e não devem ser lidos como certeza sobre o
resultado de 2026.
