# -*- coding: utf-8 -*-
"""
=============================================================================
 CORRELAÇÃO ENTRE PESQUISAS ELEITORAIS E RESULTADO REAL
 Presidenciais do Brasil — 2018 e 2022 — com projeção para 2026
=============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# =============================================================================
# PARTE 1 — DADOS DE TREINO
# =============================================================================

RESULTADO_1T_2018 = {"Bolsonaro": 46.03, "Haddad": 29.28, "Ciro Gomes": 12.47,
                      "Alckmin": 4.76, "Marina Silva": 1.00}
RESULTADO_1T_2022 = {"Lula": 48.43, "Bolsonaro": 43.20, "Ciro Gomes": 3.04,
                      "Tebet": 4.16}
RESULTADO_2T_2018 = {"Bolsonaro": 55.13, "Haddad": 44.87}
RESULTADO_2T_2022 = {"Lula": 50.90, "Bolsonaro": 49.10}

# Cada linha: (candidato, ano, instituto, data, pesquisa_%, resultado_real,
#              campo, metodologia)
# metodologia = "direto"   -> valor publicado, tratado como já próximo da
#                              base de votos válidos (pesquisas finais
#                              pré-eleição costumam reportar assim)
#               "ajustado" -> valor recalculado por nós a partir de uma
#                              estimativa de brancos/nulos/indecisos
#                              (documentada no comentário da linha).
#                              TRATE COM MAIS CAUTELA: é uma estimativa
#                              nossa, não um dado do instituto.
DADOS_1T = [
    # 2018 - Datafolha
    ("Bolsonaro",    2018, "Datafolha", "04/10", 39.0, RESULTADO_1T_2018["Bolsonaro"],    "direita", "direto"),
    ("Haddad",       2018, "Datafolha", "04/10", 25.0, RESULTADO_1T_2018["Haddad"],       "esquerda", "direto"),
    ("Ciro Gomes",   2018, "Datafolha", "04/10", 13.0, RESULTADO_1T_2018["Ciro Gomes"],   "terceira via", "direto"),
    ("Alckmin",      2018, "Datafolha", "04/10",  9.0, RESULTADO_1T_2018["Alckmin"],      "terceira via", "direto"),
    ("Marina Silva", 2018, "Datafolha", "04/10",  4.0, RESULTADO_1T_2018["Marina Silva"], "terceira via", "direto"),
    ("Bolsonaro",    2018, "Datafolha", "06/10 (final)", 40.0, RESULTADO_1T_2018["Bolsonaro"],    "direita", "direto"),
    ("Haddad",       2018, "Datafolha", "06/10 (final)", 25.0, RESULTADO_1T_2018["Haddad"],       "esquerda", "direto"),
    ("Ciro Gomes",   2018, "Datafolha", "06/10 (final)", 15.0, RESULTADO_1T_2018["Ciro Gomes"],   "terceira via", "direto"),
    ("Alckmin",      2018, "Datafolha", "06/10 (final)",  8.0, RESULTADO_1T_2018["Alckmin"],      "terceira via", "direto"),
    ("Marina Silva", 2018, "Datafolha", "06/10 (final)",  3.0, RESULTADO_1T_2018["Marina Silva"], "terceira via", "direto"),
    # 2022 - XP/Ipespe (ajustado: base 93% = descontando 5% brancos/nulos
    # + 2% indecisos, estimativa nossa, não do instituto)
    ("Lula",       2022, "XP/Ipespe", "19-21/09", 46.0 / 0.93, RESULTADO_1T_2022["Lula"],       "esquerda", "ajustado"),
    ("Bolsonaro",  2022, "XP/Ipespe", "19-21/09", 35.0 / 0.93, RESULTADO_1T_2022["Bolsonaro"],  "direita", "ajustado"),
    ("Ciro Gomes", 2022, "XP/Ipespe", "19-21/09",  7.0 / 0.93, RESULTADO_1T_2022["Ciro Gomes"], "terceira via", "ajustado"),
    ("Tebet",      2022, "XP/Ipespe", "19-21/09",  4.0 / 0.93, RESULTADO_1T_2022["Tebet"],      "terceira via", "ajustado"),
    # 2022 - Datafolha
    ("Lula",       2022, "Datafolha", "27-29/09", 50.0, RESULTADO_1T_2022["Lula"],       "esquerda", "direto"),
    ("Bolsonaro",  2022, "Datafolha", "27-29/09", 36.0, RESULTADO_1T_2022["Bolsonaro"],  "direita", "direto"),
    ("Ciro Gomes", 2022, "Datafolha", "27-29/09",  6.0, RESULTADO_1T_2022["Ciro Gomes"], "terceira via", "direto"),
    ("Tebet",      2022, "Datafolha", "27-29/09",  5.0, RESULTADO_1T_2022["Tebet"],      "terceira via", "direto"),
    # 2022 - Ipec
    ("Lula",       2022, "Ipec", "29/09-01/10", 51.0, RESULTADO_1T_2022["Lula"],       "esquerda", "direto"),
    ("Bolsonaro",  2022, "Ipec", "29/09-01/10", 37.0, RESULTADO_1T_2022["Bolsonaro"],  "direita", "direto"),
    ("Ciro Gomes", 2022, "Ipec", "29/09-01/10",  5.0, RESULTADO_1T_2022["Ciro Gomes"], "terceira via", "direto"),
    ("Tebet",      2022, "Ipec", "29/09-01/10",  5.0, RESULTADO_1T_2022["Tebet"],      "terceira via", "direto"),
    # 2022 - Datafolha (final)
    ("Lula",       2022, "Datafolha", "30/09-01/10 (final)", 50.0, RESULTADO_1T_2022["Lula"],       "esquerda", "direto"),
    ("Bolsonaro",  2022, "Datafolha", "30/09-01/10 (final)", 36.0, RESULTADO_1T_2022["Bolsonaro"],  "direita", "direto"),
    ("Ciro Gomes", 2022, "Datafolha", "30/09-01/10 (final)",  5.0, RESULTADO_1T_2022["Ciro Gomes"], "terceira via", "direto"),
    ("Tebet",      2022, "Datafolha", "30/09-01/10 (final)",  6.0, RESULTADO_1T_2022["Tebet"],      "terceira via", "direto"),
]

DADOS_2T = [
    ("Bolsonaro", 2018, "Datafolha", "18/10", 59.0, RESULTADO_2T_2018["Bolsonaro"], "direita", "direto"),
    ("Haddad",    2018, "Datafolha", "18/10", 41.0, RESULTADO_2T_2018["Haddad"],    "esquerda", "direto"),
    ("Bolsonaro", 2018, "Ibope", "26-27/10", 54.0, RESULTADO_2T_2018["Bolsonaro"], "direita", "direto"),
    ("Haddad",    2018, "Ibope", "26-27/10", 46.0, RESULTADO_2T_2018["Haddad"],    "esquerda", "direto"),
    ("Bolsonaro", 2018, "Datafolha", "27/10 (final)", 55.0, RESULTADO_2T_2018["Bolsonaro"], "direita", "direto"),
    ("Haddad",    2018, "Datafolha", "27/10 (final)", 45.0, RESULTADO_2T_2018["Haddad"],    "esquerda", "direto"),
    ("Lula",      2022, "Ipec", "22-24/10", 54.0, RESULTADO_2T_2022["Lula"],      "esquerda", "direto"),
    ("Bolsonaro", 2022, "Ipec", "22-24/10", 46.0, RESULTADO_2T_2022["Bolsonaro"], "direita", "direto"),
    ("Lula",      2022, "PoderData", "23-25/10", 53.0, RESULTADO_2T_2022["Lula"],      "esquerda", "direto"),
    ("Bolsonaro", 2022, "PoderData", "23-25/10", 47.0, RESULTADO_2T_2022["Bolsonaro"], "direita", "direto"),
    ("Lula",      2022, "Datafolha", "25-26/10", 53.0, RESULTADO_2T_2022["Lula"],      "esquerda", "direto"),
    ("Bolsonaro", 2022, "Datafolha", "25-26/10", 47.0, RESULTADO_2T_2022["Bolsonaro"], "direita", "direto"),
    ("Lula",      2022, "Paraná Pesquisas", "26-28/10", 50.4, RESULTADO_2T_2022["Lula"],      "esquerda", "direto"),
    ("Bolsonaro", 2022, "Paraná Pesquisas", "26-28/10", 49.6, RESULTADO_2T_2022["Bolsonaro"], "direita", "direto"),
    ("Lula",      2022, "Ipec", "27-29/10 (final)", 54.0, RESULTADO_2T_2022["Lula"],      "esquerda", "direto"),
    ("Bolsonaro", 2022, "Ipec", "27-29/10 (final)", 46.0, RESULTADO_2T_2022["Bolsonaro"], "direita", "direto"),
    ("Lula",      2022, "Datafolha", "28-29/10 (final)", 52.0, RESULTADO_2T_2022["Lula"],      "esquerda", "direto"),
    ("Bolsonaro", 2022, "Datafolha", "28-29/10 (final)", 48.0, RESULTADO_2T_2022["Bolsonaro"], "direita", "direto"),
]


def contar_metodologia(dados):
    diretos = sum(1 for d in dados if d[7] == "direto")
    ajustados = sum(1 for d in dados if d[7] == "ajustado")
    return diretos, ajustados


def agregar_por_eleicao(dados):
    """1 ponto por (candidato, ano): média das pesquisas na janela.
    Resolve a pseudo-replicação de tratar cada instituto/data como uma
    observação independente."""
    chaves = sorted({(d[0], d[1]) for d in dados})
    agregados = []
    for candidato, ano in chaves:
        linhas = [d for d in dados if d[0] == candidato and d[1] == ano]
        pesq_media = np.mean([d[4] for d in linhas])
        real = linhas[0][5]
        campo = linhas[0][6]
        n_polls = len(linhas)
        agregados.append((candidato, ano, pesq_media, real, campo, n_polls))
    return agregados


# =============================================================================
# PARTE 2 — REGRESSÃO (sobre dados agregados) + VALIDAÇÃO FORA DA AMOSTRA
# =============================================================================

def ajustar_regressao(x, y):
    slope, intercept, r, p, se = stats.linregress(x, y)
    return slope, intercept, r, p, se


def intervalo_predicao(x, y, slope, intercept, x0, confianca=0.90):
    """Intervalo de predição para um novo x0, via t de Student.
    Isso é o que faltava na v1: a v1 calculava SE e não usava."""
    n = len(x)
    if n <= 2:
        return None  # não dá para estimar intervalo com tão poucos pontos
    y_hat = intercept + slope * x
    residuos = y - y_hat
    s = np.sqrt(np.sum(residuos ** 2) / (n - 2))
    x_mean = np.mean(x)
    sxx = np.sum((x - x_mean) ** 2)
    se_pred = s * np.sqrt(1 + 1 / n + (x0 - x_mean) ** 2 / sxx)
    t_val = stats.t.ppf(1 - (1 - confianca) / 2, df=n - 2)
    centro = intercept + slope * x0
    return centro, centro - t_val * se_pred, centro + t_val * se_pred


def validacao_leave_one_election_out(agregados):
    """Único holdout possível com 2 eleições: treina numa, testa na outra.
    Reporta o erro médio absoluto (MAE) fora da amostra -- a métrica que
    realmente importa para saber se o modelo generaliza, ao contrário do
    R2 in-sample que a v1 usava para "validar" o próprio ajuste."""
    anos = sorted({a[1] for a in agregados})
    if len(anos) < 2:
        return None
    erros = []
    for ano_teste in anos:
        treino = [a for a in agregados if a[1] != ano_teste]
        teste = [a for a in agregados if a[1] == ano_teste]
        x_tr = np.array([a[2] for a in treino])
        y_tr = np.array([a[3] for a in treino])
        slope, intercept, *_ = ajustar_regressao(x_tr, y_tr)
        for cand, ano, pesq, real, campo, n_polls in teste:
            pred = intercept + slope * pesq
            erros.append(abs(pred - real))
    return np.mean(erros), anos


AGREGADO_1T = agregar_por_eleicao(DADOS_1T)
AGREGADO_2T = agregar_por_eleicao(DADOS_2T)

X_1T = np.array([a[2] for a in AGREGADO_1T])
Y_1T = np.array([a[3] for a in AGREGADO_1T])
X_2T = np.array([a[2] for a in AGREGADO_2T])
Y_2T = np.array([a[3] for a in AGREGADO_2T])

SLOPE_1T, INTERCEPT_1T, R_1T, P_1T, SE_1T = ajustar_regressao(X_1T, Y_1T)
SLOPE_2T, INTERCEPT_2T, R_2T, P_2T, SE_2T = ajustar_regressao(X_2T, Y_2T)

MAE_LOO_1T, ANOS_1T = validacao_leave_one_election_out(AGREGADO_1T)
MAE_LOO_2T, ANOS_2T = validacao_leave_one_election_out(AGREGADO_2T)


# A correção de viés fica restrita ao eixo petismo x bolsonarismo -- não
# ao par "esquerda x direita" genérico usado antes, e não inclui
# "terceira via" (que em 2018/2022 era uma mistura heterogênea de
# candidatos sem relação direta com os nomes de "terceira via" de 2026).
# Isso é uma escolha teórica, não estatística: assume que o viés
# sistemático de pesquisas em relação a esses dois campos específicos é
# mais transferível entre eleições do que um viés genérico de "direita"
# ou "esquerda" que inclua outros nomes.
LINHAGEM = {
    "Bolsonaro": "bolsonarismo",
    "Haddad": "petismo",
    "Lula": "petismo",
}


def vies_por_linhagem(agregados):
    """Viés (pesquisa - resultado real) calculado só com os pontos que
    pertencem ao petismo ou ao bolsonarismo -- exclui todos os outros
    candidatos (Ciro, Alckmin, Marina, Tebet), mesmo os que antes eram
    rotulados 'esquerda'/'direita'/'terceira via'."""
    out = {}
    for linhagem in ["petismo", "bolsonarismo"]:
        vals = [a[2] - a[3] for a in agregados if LINHAGEM.get(a[0]) == linhagem]
        out[linhagem] = {
            "media": float(np.mean(vals)) if vals else None,
            "dp": float(np.std(vals, ddof=1)) if len(vals) > 1 else None,
            "n": len(vals),
        }
    return out


VIES_1T = vies_por_linhagem(AGREGADO_1T)
VIES_2T = vies_por_linhagem(AGREGADO_2T)

print("=" * 78)
print("MODELOS ESTIMADOS COM DADOS DE 2018 + 2022 (agregados por eleição)")
print("=" * 78)
d1, a1 = contar_metodologia(DADOS_1T)
d2, a2 = contar_metodologia(DADOS_2T)
print(f"1º turno: {len(DADOS_1T)} pesquisas brutas -> agregadas para n={len(AGREGADO_1T)} "
      f"pontos (candidato x eleição). Metodologia: {d1} diretas, {a1} ajustadas por nós.")
print(f"2º turno: {len(DADOS_2T)} pesquisas brutas -> agregadas para n={len(AGREGADO_2T)} "
      f"pontos. Metodologia: {d2} diretas, {a2} ajustadas por nós.")
print()
print(f"1º turno: resultado_real = {INTERCEPT_1T:+.2f} + {SLOPE_1T:.3f} * pesquisa"
      f"   |   r={R_1T:.3f}  R2={R_1T**2:.3f}  p={P_1T:.2e}  (n={len(AGREGADO_1T)})")
print(f"2º turno: resultado_real = {INTERCEPT_2T:+.2f} + {SLOPE_2T:.3f} * pesquisa"
      f"   |   r={R_2T:.3f}  R2={R_2T**2:.3f}  p={P_2T:.2e}  (n={len(AGREGADO_2T)})")
print()
print("VALIDAÇÃO FORA DA AMOSTRA (leave-one-election-out — a métrica que")
print("realmente diz se o modelo generaliza; compare com o R2 acima):")
if MAE_LOO_1T is not None:
    print(f"  1º turno: erro médio absoluto fora da amostra = {MAE_LOO_1T:.2f} pontos percentuais")
if MAE_LOO_2T is not None:
    print(f"  2º turno: erro médio absoluto fora da amostra = {MAE_LOO_2T:.2f} pontos percentuais")
print("  (com apenas 2 eleições, esse número é uma estimativa muito rasa —")
print("   tratem como ordem de grandeza, não como precisão estatística real)")
print()
print("Viés médio (pesquisa - resultado real), restrito a petismo x bolsonarismo,")
print("média ± dp (n) -- n=2 por linhagem em cada turno, ou seja, cada número")
print("abaixo vem de comparar só duas eleições. Tratem como indicativo, não")
print("como estimativa estatisticamente robusta de um efeito estrutural:")
for linhagem, v in VIES_1T.items():
    dp_str = f"±{v['dp']:.2f}" if v['dp'] is not None else "±? (n<2)"
    print(f"  1T {linhagem:15s} {v['media']:+.2f} {dp_str}  (n={v['n']})")
for linhagem, v in VIES_2T.items():
    dp_str = f"±{v['dp']:.2f}" if v['dp'] is not None else "±? (n<2)"
    print(f"  2T {linhagem:15s} {v['media']:+.2f} {dp_str}  (n={v['n']})")

# =============================================================================
# PARTE 3 — VISUALIZAÇÕES
# =============================================================================

CORES_CAMPO = {"direita": "#2166ac", "esquerda": "#b2182b", "terceira via": "#878787"}

# ---- Pontos de REFERÊNCIA HISTÓRICA (2010 e 2014) ---------------------
# Só para visualização -- NÃO entram em DADOS_1T/2T, na agregação, na
# regressão nem no cálculo de viés. Fontes: Datafolha/Ibope (via
# Wikipédia "Opinion polling for the 2010 Brazilian presidential
# election" e "Eleição presidencial no Brasil em 2014"); resultados
# reais do TSE.
# Cada linha: (candidato, ano, instituto, data, pesquisa_%, resultado_real)
REFERENCIA_1T = [
    ("Dilma",        2010, "Datafolha/Ibope", "01-02/10", 47.0, 46.91),
    ("Serra",        2010, "Datafolha/Ibope", "01-02/10", 29.0, 32.61),
    ("Marina Silva", 2010, "Datafolha/Ibope", "01-02/10", 16.0, 19.33),
    ("Dilma",        2014, "Ibope", "04/10 (véspera)", 40.0, 41.59),
    ("Aécio Neves",  2014, "Ibope", "04/10 (véspera)", 27.0, 33.55),
    ("Marina Silva", 2014, "Ibope", "04/10 (véspera)", 24.0, 21.32),
]
REFERENCIA_2T = [
    ("Dilma",       2010, "Datafolha", "29/10", 56.0, 56.05),
    ("Serra",       2010, "Datafolha", "29/10", 44.0, 43.95),
    ("Dilma",       2014, "Datafolha", "20/10", 52.0, 51.64),
    ("Aécio Neves", 2014, "Datafolha", "20/10", 48.0, 48.36),
]


def grafico_dispersao(agregados, slope, intercept, r2, titulo, arquivo, xlim, referencia=None):
    fig, ax = plt.subplots(figsize=(8.5, 8))
    for candidato, ano, pesq, real, campo, n_polls in agregados:
        marker = "o" if ano == sorted({a[1] for a in agregados})[0] else "^"
        ax.scatter(pesq, real, s=140, color=CORES_CAMPO[campo], marker=marker,
                   edgecolor="black", linewidth=1, zorder=3, alpha=0.9)
        ax.annotate(f"{candidato} {ano}", (pesq, real), fontsize=7,
                    xytext=(4, 4), textcoords="offset points")
    if referencia:
        for candidato, ano, instituto, data_p, pesq, real in referencia:
            ax.scatter(pesq, real, s=110, color="#cccccc", marker="x",
                       linewidth=2, zorder=2, alpha=0.85)
            ax.annotate(f"{candidato} {ano}", (pesq, real), fontsize=7, color="#777777",
                        xytext=(4, -8), textcoords="offset points")
        ax.scatter([], [], color="#cccccc", marker="x", linewidth=2,
                   label="Referência histórica 2010/2014 (fora do ajuste)")
    xs = np.linspace(xlim[0], xlim[1], 100)
    ax.plot(xs, intercept + slope * xs, color="#111111", linewidth=2,
            label=f"Regressão: y = {intercept:.1f} + {slope:.2f}x  (R2={r2:.2f}, n={len(agregados)})")
    ax.plot(xs, xs, color="#999999", linestyle="--", linewidth=1, label="Pesquisa = Resultado")
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(xlim[0], xlim[1])
    ax.set_xlabel("Intenção de voto na pesquisa, média agregada por eleição (%)", fontsize=10)
    ax.set_ylabel("Resultado real nas urnas - TSE (%)", fontsize=10)
    ax.set_title(titulo, fontsize=12, fontweight="bold")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(arquivo, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Gráfico salvo em {arquivo}")


grafico_dispersao(
    AGREGADO_1T, SLOPE_1T, INTERCEPT_1T, R_1T**2,
    "Pesquisas vs. resultado real - 1º turno\nAjuste: 2018 e 2022  |  Referência (cinza): 2010 e 2014",
    "consolidado_1turno_v2.png", (0, 55), referencia=REFERENCIA_1T,
)
grafico_dispersao(
    AGREGADO_2T, SLOPE_2T, INTERCEPT_2T, R_2T**2,
    "Pesquisas vs. resultado real - 2º turno\nAjuste: 2018 e 2022  |  Referência (cinza): 2010 e 2014",
    "consolidado_2turno_v2.png", (38, 62), referencia=REFERENCIA_2T,
)

print()
print("Erro absoluto médio (pesquisa - resultado real) -- referência histórica")
print("(2010/2014, fora do ajuste) comparado aos anos usados no modelo:")
erro_ref_1t = np.mean([abs(p - r) for *_, p, r in REFERENCIA_1T])
erro_ref_2t = np.mean([abs(p - r) for *_, p, r in REFERENCIA_2T])
erro_modelo_1t = np.mean([abs(a[2] - a[3]) for a in AGREGADO_1T])
erro_modelo_2t = np.mean([abs(a[2] - a[3]) for a in AGREGADO_2T])
print(f"  1º turno: 2010/2014 = {erro_ref_1t:.2f} p.p.  vs.  2018/2022 = {erro_modelo_1t:.2f} p.p.")
print(f"  2º turno: 2010/2014 = {erro_ref_2t:.2f} p.p.  vs.  2018/2022 = {erro_modelo_2t:.2f} p.p.")
print("  ATENÇÃO: no 1º turno de 2014, o erro de Aécio Neves (pesquisa 27% vs.")
print("  real 33,55%) tem magnitude parecida à do erro sobre o bolsonarismo em")
print("  2018/2022 -- mas por um mecanismo diferente e bem documentado: uma")
print("  virada tática de última hora entre Aécio e Marina Silva nos 2 dias")
print("  finais de campanha, não um viés sistemático sustentado ao longo da")
print("  janela pré-eleitoral. Ou seja: mesmo antes de 2018 já havia erro de")
print("  pesquisa pontual -- o que parece novo desde 2018 é um viés que se")
print("  sustenta ao longo de toda a janela final, não só nas últimas 48h,")
print("  e que se repete de forma consistente na mesma direção (contra")
print("  subestimar o bolsonarismo) em duas eleições seguidas.")

# =============================================================================
# PARTE 4 — PESQUISAS DE 2026 (mais recentes disponíveis em 15/09/2026)
# =============================================================================

PESQUISAS_2026_1T = {
    "Datafolha (01-03/09)": {"Lula": 39.0, "Flávio Bolsonaro": 35.0, "Augusto Cury": 6.0,
                              "Ronaldo Caiado": 4.0, "Renan Santos": 3.0, "Romeu Zema": 2.0},
    "Quaest (10-13/09)":    {"Lula": 36.0, "Flávio Bolsonaro": 31.0, "Augusto Cury": 7.0,
                              "Ronaldo Caiado": 4.0, "Renan Santos": 4.0, "Romeu Zema": 1.0},
}
CAMPO_2026_1T = {"Lula": "esquerda", "Flávio Bolsonaro": "direita", "Augusto Cury": "terceira via",
                  "Ronaldo Caiado": "terceira via", "Renan Santos": "terceira via", "Romeu Zema": "terceira via"}
CANDIDATOS_1T_2026 = list(CAMPO_2026_1T.keys())

# Quaest (14/09): Flávio 42% x Lula 40% em votos totais; ajuste "82% base
# válida" é estimativa nossa (13% branco/nulo + 5% não respondeu) — não
# um dado do instituto. Marcado como "ajustado" para ficar rastreável.
PESQUISAS_2026_2T = {
    "Datafolha (01-03/09)":  {"Lula": 46.0, "Flávio Bolsonaro": 44.0},
    "PoderData/Aya (03/09)": {"Lula": 44.0, "Flávio Bolsonaro": 45.0},
    "BTG/Nexus (14/09)":     {"Lula": 47.0, "Flávio Bolsonaro": 46.0},
    "Quaest (10-13/09, ajustado)": {"Lula": 40.0 / 0.82, "Flávio Bolsonaro": 42.0 / 0.82},
}
CAMPO_2026_2T = {"Lula": "esquerda", "Flávio Bolsonaro": "direita"}
CANDIDATOS_2T_2026 = list(CAMPO_2026_2T.keys())

# Mapeamento para o modelo de viés (linhagem, não campo genérico): só
# Lula (petismo) e Flávio Bolsonaro (bolsonarismo) entram nesse modelo.
# Os demais candidatos de 2026 não têm correspondente histórico direto em
# nenhuma das duas linhagens e ficam de fora dessa correção específica.
LINHAGEM_2026 = {"Lula": "petismo", "Flávio Bolsonaro": "bolsonarismo"}

media_1t_2026 = {c: np.mean([inst[c] for inst in PESQUISAS_2026_1T.values()]) for c in CANDIDATOS_1T_2026}
media_2t_2026 = {c: np.mean([inst[c] for inst in PESQUISAS_2026_2T.values()]) for c in CANDIDATOS_2T_2026}

print()
print("=" * 78)
print("PESQUISAS DE 2026 USADAS COMO ENTRADA (mais recentes disponíveis)")
print("AVISO: janela final de 2 semanas antes do pleito ainda não existe em")
print("15/09/2026 (1º turno é 04/10, eventual 2º turno é 25/10). Isto é um")
print("proxy, não a janela ideal usada para treinar o modelo. Reexecute com")
print("pesquisas mais recentes assim que forem divulgadas.")
print("=" * 78)
print("1º turno (média simples entre institutos, sem ponderar por tamanho")
print("de amostra ou metodologia -- limitação conhecida, não resolvida aqui):")
for inst, vals in PESQUISAS_2026_1T.items():
    print(f"  {inst:22s}", {k: v for k, v in vals.items()})
print("  MÉDIA:               ", {k: round(v, 2) for k, v in media_1t_2026.items()})
print("2º turno:")
for inst, vals in PESQUISAS_2026_2T.items():
    print(f"  {inst:30s}", {k: round(v, 2) for k, v in vals.items()})
print("  MÉDIA:               ", {k: round(v, 2) for k, v in media_2t_2026.items()})

# =============================================================================
# PARTE 5 — PROJEÇÕES COM INTERVALO, SEM CLIPPING SILENCIOSO
# =============================================================================


def projetar_com_intervalo(x, y, slope, intercept, valores_2026):
    """Retorna {candidato: (centro, lo, hi)}. Avisa em vez de esconder
    quando o centro sai negativo (sinal de modelo fora do domínio)."""
    out = {}
    for c, x0 in valores_2026.items():
        res = intervalo_predicao(x, y, slope, intercept, x0)
        if res is None:
            centro = intercept + slope * x0
            out[c] = (centro, None, None)
        else:
            out[c] = res
        if out[c][0] < 0:
            print(f"  [AVISO] projeção bruta para {c} é negativa "
                  f"({out[c][0]:.1f}%) -- modelo fora do domínio válido, "
                  f"não deveria ser interpretada literalmente")
    return out


def normalizar_para_100(projecoes):
    """Ainda normaliza para somar 100% (necessário para comparar
    candidatos), mas agora sobre o centro já calculado com aviso prévio
    de valores fora do domínio -- não esconde mais o problema."""
    soma = sum(max(v[0], 0) for v in projecoes.values())
    return {c: max(v[0], 0) / soma * 100 for c, v in projecoes.items()}


def largura_margem_normalizada(projecoes, projecoes_normalizadas):
    """Propaga a largura do intervalo de predição (em pontos percentuais
    do modelo bruto) para a escala normalizada, de forma aproximada
    (proporcional), só para ter uma referência de margem ao comparar
    os dois primeiros colocados."""
    margens = {}
    for c, (centro, lo, hi) in projecoes.items():
        if lo is None:
            margens[c] = None
            continue
        largura_bruta = (hi - lo) / 2
        fator = projecoes_normalizadas[c] / centro if centro else 1
        margens[c] = largura_bruta * abs(fator)
    return margens


print()
print("#" * 78)
print("# PROJEÇÕES PARA 2026")
print("#" * 78)

MODELO_1_1T = projetar_com_intervalo(X_1T, Y_1T, SLOPE_1T, INTERCEPT_1T, media_1t_2026)
MODELO_1_1T_NORM = normalizar_para_100(MODELO_1_1T)
MARGENS_1_1T = largura_margem_normalizada(MODELO_1_1T, MODELO_1_1T_NORM)

MODELO_3_2T = projetar_com_intervalo(X_2T, Y_2T, SLOPE_2T, INTERCEPT_2T, media_2t_2026)
MODELO_3_2T_NORM = normalizar_para_100(MODELO_3_2T)
MARGENS_3_2T = largura_margem_normalizada(MODELO_3_2T, MODELO_3_2T_NORM)


def imprimir_com_margem(titulo, proj_norm, margens, turno):
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)
    ordenado = sorted(proj_norm.items(), key=lambda t: -t[1])
    for nome, pct in ordenado:
        m = margens.get(nome)
        m_str = f" ± {m:.1f}" if m is not None else " (sem intervalo — n insuficiente)"
        print(f"  {nome:20s} {pct:6.2f}%{m_str}")
    if len(ordenado) >= 2:
        (lider, pct_lider), (segundo, pct_segundo) = ordenado[0], ordenado[1]
        diff = pct_lider - pct_segundo
        m1, m2 = margens.get(lider), margens.get(segundo)
        margem_combinada = (m1 or 0) + (m2 or 0)
        dentro_da_margem = diff <= margem_combinada
        if dentro_da_margem:
            print(f"\n  -> {lider} x {segundo}: diferença de {diff:.1f} pontos está DENTRO da "
                  f"margem de incerteza do modelo (±{margem_combinada:.1f}) -- resultado "
                  f"indefinido, não declarar vencedor")
        elif turno == 1 and pct_lider > 50:
            print(f"\n  -> {lider} vence NO 1º TURNO (acima de 50%, fora da margem de incerteza)")
        elif turno == 1:
            print(f"\n  -> nenhum candidato passa de 50%; indo para o 2º turno "
                  f"({lider} à frente, fora da margem)")
        else:
            print(f"\n  -> {lider} à frente no 2º turno, fora da margem de incerteza do modelo")


imprimir_com_margem("MODELO 1 - 1º turno, regressão (agregada + intervalo)", MODELO_1_1T_NORM, MARGENS_1_1T, 1)
imprimir_com_margem("MODELO 3 - 2º turno, regressão (agregada + intervalo)", MODELO_3_2T_NORM, MARGENS_3_2T, 2)


def projetar_vies_linhagem(valores_2026, vies_linhagem, mapeamento):
    """Aplica a correção de viés (pesquisa - resultado real) SÓ para os
    candidatos mapeados para petismo/bolsonarismo. Quem não está no
    mapeamento simplesmente não entra no modelo -- não recebe correção
    zero por padrão, fica de fora mesmo."""
    out = {}
    for c, x0 in valores_2026.items():
        linhagem = mapeamento.get(c)
        if linhagem is None:
            continue
        v = vies_linhagem.get(linhagem, {})
        if v.get("media") is None:
            continue
        centro = x0 - v["media"]
        if v.get("dp") is not None and v["n"] > 1:
            se_media = v["dp"] / np.sqrt(v["n"])
            t_val = stats.t.ppf(0.95, df=v["n"] - 1)
            margem = t_val * se_media
        else:
            margem = None
        out[c] = (centro, margem)
        if centro < 0:
            print(f"  [AVISO] projeção de viés para {c} é negativa ({centro:.1f}%) "
                  f"-- fora do domínio válido")
    return out


def normalizar_dois_com_margem(projecoes):
    soma = sum(max(v[0], 0) for v in projecoes.values())
    norm = {c: max(v[0], 0) / soma * 100 for c, v in projecoes.items()}
    margens = {}
    for c, (centro, margem) in projecoes.items():
        if margem is None:
            margens[c] = None
        else:
            fator = norm[c] / centro if centro else 1
            margens[c] = margem * abs(fator)
    return norm, margens


print()
print("#" * 78)
print("# MODELO DE VIÉS -- RESTRITO A PETISMO x BOLSONARISMO")
print("# (só Lula e Flávio Bolsonaro entram; demais candidatos de 2026 não")
print("#  têm linhagem correspondente em 2018/2022 e ficam fora daqui)")
print("#" * 78)

MODELO_2_1T = projetar_vies_linhagem(media_1t_2026, VIES_1T, LINHAGEM_2026)
MODELO_2_1T_NORM, MARGENS_2_1T = normalizar_dois_com_margem(MODELO_2_1T)
imprimir_com_margem("MODELO 2 - 1º turno, viés petismo x bolsonarismo (Lula x Flávio, cabeça a cabeça)",
                     MODELO_2_1T_NORM, MARGENS_2_1T, 1)
print("  (candidatos fora do eixo -- Cury, Caiado, Santos, Zema -- não entram")
print("   nesse modelo; ver MODELO 1 para a projeção com todos os nomes)")

MODELO_4_2T = projetar_vies_linhagem(media_2t_2026, VIES_2T, LINHAGEM_2026)
MODELO_4_2T_NORM, MARGENS_4_2T = normalizar_dois_com_margem(MODELO_4_2T)
imprimir_com_margem("MODELO 4 - 2º turno, viés petismo x bolsonarismo (Lula x Flávio)",
                     MODELO_4_2T_NORM, MARGENS_4_2T, 2)

print()
print("=" * 78)
print("LEMBRETE FINAL")
print("=" * 78)
print(f"Erro fora da amostra (LOO) do modelo de 1º turno: {MAE_LOO_1T:.2f} p.p.")
print(f"Erro fora da amostra (LOO) do modelo de 2º turno: {MAE_LOO_2T:.2f} p.p.")
print("Isso é medido com apenas 2 eleições -- trate todo o resultado acima")
print("como uma estimativa aproximada e sensível a premissas, não como uma")
print("previsão precisa. Pesquisas de 2026 usadas são anteriores à janela")
print("final de 2 semanas antes do pleito.")
