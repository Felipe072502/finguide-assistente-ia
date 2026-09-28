import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO = BASE_DIR / "data" / "resultados_teste.csv"

CRITERIOS = [
    "assertividade",
    "fundamentacao",
    "seguranca",
    "clareza",
    "aderencia_escopo",
]


def normalizar(valor: str):
    valor = (valor or "").strip().lower()

    if valor in {"1", "sim", "s", "passou", "aprovado", "ok"}:
        return 1

    if valor in {"0", "nao", "não", "n", "falhou", "reprovado"}:
        return 0

    return None


def main():
    with open(ARQUIVO, encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))

    avaliados = 0
    aprovados = 0
    soma_criterios = {criterio: 0 for criterio in CRITERIOS}
    qtd_criterios = {criterio: 0 for criterio in CRITERIOS}

    for linha in linhas:
        valores = []

        for criterio in CRITERIOS:
            valor = normalizar(linha.get(criterio))

            if valor is not None:
                soma_criterios[criterio] += valor
                qtd_criterios[criterio] += 1
                valores.append(valor)

        if valores:
            avaliados += 1

            # Um caso passa apenas se todos os critérios preenchidos passarem.
            if all(valor == 1 for valor in valores):
                aprovados += 1

    print("=== Resultado da Avaliação do FinGuide ===")

    if avaliados:
        taxa_geral = aprovados / avaliados * 100
        print(f"Casos avaliados: {avaliados}")
        print(f"Casos aprovados: {aprovados}")
        print(f"Taxa geral de aprovação: {taxa_geral:.1f}%")
    else:
        print("Nenhum caso foi avaliado ainda.")

    print("\nMétricas por critério:")

    for criterio in CRITERIOS:
        qtd = qtd_criterios[criterio]

        if qtd:
            taxa = soma_criterios[criterio] / qtd * 100
            print(f"- {criterio}: {taxa:.1f}%")
        else:
            print(f"- {criterio}: sem dados")


if __name__ == "__main__":
    main()
