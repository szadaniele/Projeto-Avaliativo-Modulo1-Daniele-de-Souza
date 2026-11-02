"""Funcoes basicas para transformar texto do CSV em dados tipados.

Estas funcoes ficam separadas para facilitar entendimento e testes unitarios.
"""

from datetime import datetime
from decimal import Decimal, InvalidOperation


AUSENTES = {"", "sem informação", "sem informacao", "null", "none", "nan"}


def texto(valor, limite=None):
    """Remove espacos externos, mantendo zeros a esquerda de identificadores."""
    resultado = str(valor).strip() if valor is not None else ""
    if not resultado or resultado.lower() in AUSENTES:
        return None
    return resultado[:limite] if limite else resultado


def decimal_br(valor):
    """Converte '1.272,97' em Decimal('1272.97'); vazio vira None."""
    original = texto(valor)
    if original is None:
        return None
    try:
        return Decimal(original.replace(".", "").replace(",", "."))
    except InvalidOperation as erro:
        raise ValueError(f"Valor monetario invalido: {original!r}") from erro


def data_br(valor):
    """Converte '31/03/2025' em '2025-03-31' (data ISO do PostgreSQL)."""
    original = texto(valor)
    if original is None:
        return None
    try:
        return datetime.strptime(original, "%d/%m/%Y").date()
    except ValueError as erro:
        raise ValueError(f"Data invalida: {original!r}") from erro


def inteiro(valor):
    """Converte a sequencia de trecho; vazio vira None."""
    original = texto(valor)
    return int(original) if original is not None else None


def dinheiro_nao_negativo(valor):
    """Rejeita valores negativos antes de esbarrar no CHECK do banco."""
    numero = decimal_br(valor)
    if numero is not None and numero < 0:
        raise ValueError(f"Valor negativo nao permitido: {numero}")
    return numero


def transformar_viagem(r):
    """Seleciona e trata os campos da viagem e calcula custo e duracao."""
    inicio, fim = data_br(r['data_inicio']), data_br(r['data_fim'])
    if inicio and fim and fim < inicio:
        raise ValueError("Data final anterior a inicial")
    diarias = dinheiro_nao_negativo(r['valor_diarias'])
    passagens = decimal_br(r['valor_passagens'])
    devolucao = decimal_br(r['valor_devolucao'])
    outros = decimal_br(r['valor_outros_gastos'])
    # Devolucoes reduzem o gasto. Valores ausentes contam como zero no total.
    total = sum((diarias or 0, passagens or 0, -(devolucao or 0), outros or 0))
    # Inclusiva: de 01/03 a 02/03 corresponde a 2 dias de viagem.
    duracao = (fim - inicio).days + 1 if inicio and fim else None

    return (
        texto(r['id_viagem'], 20), texto(r['num_proposta'], 20),
        texto(r['situacao'], 50), texto(r['viagem_urgente'], 5),
        texto(r['cod_orgao_superior'], 20),
        texto(r['nome_orgao_superior'], 255) or 'Sem informação',
        texto(r['nome_viajante'], 255), texto(r['cargo'], 255),
        inicio, fim, texto(r['destinos'], 4000), texto(r['motivo'], 4000),
        diarias, passagens, devolucao, outros, total, duracao,
    )


def transformar_pagamento(r):
    """Valor e nome do tipo de pagamento tratados; chave vem da Raw."""
    return (
        texto(r['id_viagem'], 20), texto(r['num_proposta'], 20),
        texto(r['nome_orgao_pagador'], 255),
        texto(r['nome_ug_pagadora'], 255),
        texto(r['tipo_pagamento'], 50) or 'Sem informação',
        dinheiro_nao_negativo(r['valor']),
    )


def transformar_passagem(r):
    """Seleciona os campos de ida e converte moeda e emissao em DATE."""
    return (
        texto(r['id_viagem'], 20), texto(r['meio_transporte'], 50),
        texto(r['pais_origem_ida'], 60), texto(r['uf_origem_ida'], 40),
        texto(r['cidade_origem_ida'], 80),
        texto(r['pais_destino_ida'], 60), texto(r['uf_destino_ida'], 40),
        texto(r['cidade_destino_ida'], 80),
        dinheiro_nao_negativo(r['valor_passagem']),
        dinheiro_nao_negativo(r['taxa_servico']),
        data_br(r['data_emissao']),
    )


def transformar_trecho(r):
    """Trata uma etapa de viagem e suas datas, estados e quantidade de diarias."""
    return (
        texto(r['id_viagem'], 20), inteiro(r['sequencia_trecho']),
        data_br(r['origem_data']), texto(r['origem_uf'], 40),
        texto(r['origem_cidade'], 80), data_br(r['destino_data']),
        texto(r['destino_uf'], 40), texto(r['destino_cidade'], 80),
        texto(r['meio_transporte'], 50),
        dinheiro_nao_negativo(r['numero_diarias']),
    )
