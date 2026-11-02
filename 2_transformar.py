"""FASE 2: ler Raw em blocos, converter e inserir na Silver.

A transformacao e atomica: erro geral desfaz a carga Silver.
"""

import csv
import io
from collections import Counter

from banco import conectar
from config import TAMANHO_BLOCO
from transformacoes import (
    transformar_viagem, transformar_pagamento,
    transformar_passagem, transformar_trecho,
)

# Colunas de destino NA ORDEM das tuplas retornadas pelas funcoes acima.
COLUNAS = {
    'viagem': (
        'id_viagem', 'num_proposta', 'situacao', 'viagem_urgente',
        'cod_orgao_superior', 'nome_orgao_superior', 'nome_viajante', 'cargo',
        'data_inicio', 'data_fim', 'destinos', 'motivo', 'valor_diarias',
        'valor_passagens', 'valor_devolucao', 'valor_outros_gastos',
        'valor_total', 'duracao_dias',
    ),
    'pagamento': (
        'id_viagem', 'num_proposta', 'nome_orgao_pagador',
        'nome_ug_pagadora', 'tipo_pagamento', 'valor',
    ),
    'passagem': (
        'id_viagem', 'meio_transporte', 'pais_origem_ida', 'uf_origem_ida',
        'cidade_origem_ida', 'pais_destino_ida', 'uf_destino_ida',
        'cidade_destino_ida', 'valor_passagem', 'taxa_servico', 'data_emissao',
    ),
    'trecho': (
        'id_viagem', 'sequencia_trecho', 'origem_data', 'origem_uf',
        'origem_cidade', 'destino_data', 'destino_uf', 'destino_cidade',
        'meio_transporte', 'numero_diarias',
    ),
}
FUNCOES = {
    'viagem': transformar_viagem,
    'pagamento': transformar_pagamento,
    'passagem': transformar_passagem,
    'trecho': transformar_trecho,
}


def copiar_linhas(cursor, entidade, linhas):
    """Insere muitas linhas Silver sem sobrecarregar o computador."""
    memoria = io.StringIO()
    escritor = csv.writer(memoria, delimiter=';', lineterminator='\n')
    for linha in linhas:
        valores = []
        for valor in linha:
            # COPY CSV com NULL '\N': numeros e datas ja sao convertidos.
            valores.append('\\N' if valor is None else str(valor))
        escritor.writerow(valores)
    memoria.seek(0)
    campos = ', '.join(COLUNAS[entidade])
    consulta = (
        f'COPY silver_{entidade} ({campos}) FROM STDIN '
        "WITH (FORMAT CSV, DELIMITER ';', NULL '\\N')"
    )
    cursor.copy_expert(consulta, memoria)


def ler_e_transformar(conexao_leitura, conexao_escrita, entidade,
                       ids_validos, sequencias_vistas):
    """Busca blocos de Raw e grava blocos tipados na Silver."""
    contagem = Counter()
    # O cursor comum devolve os nomes das colunas mesmo sem trazer linhas.
    # LIMIT 0 consulta somente a estrutura, sem carregar o CSV na memoria.
    with conexao_leitura.cursor() as cursor_colunas:
        cursor_colunas.execute(f'SELECT * FROM raw_{entidade} LIMIT 0')
        nomes_colunas = [coluna.name for coluna in cursor_colunas.description]

    # O cursor NOMEADO percorre milhoes de linhas em blocos (sem estourar RAM).
    # Em psycopg2, description pode ser None neste cursor antes de fetchmany().
    leitura = conexao_leitura.cursor(name=f'leitura_{entidade}')
    leitura.itersize = TAMANHO_BLOCO
    leitura.execute(f'SELECT * FROM raw_{entidade}')
    escrita = conexao_escrita.cursor()
    bloco = []

    try:
        while True:
            linhas_raw = leitura.fetchmany(TAMANHO_BLOCO)
            if not linhas_raw:
                break
            for linha in linhas_raw:
                contagem['lidas'] += 1
                registro = dict(zip(nomes_colunas, linha))
                try:
                    convertido = FUNCOES[entidade](registro)
                    id_viagem = convertido[0]
                    if not id_viagem:
                        contagem['sem_identificador'] += 1
                        continue
                    if entidade == 'viagem':
                        if id_viagem in ids_validos:
                            contagem['duplicadas'] += 1
                            continue
                        ids_validos.add(id_viagem)
                    elif id_viagem not in ids_validos:
                        contagem['sem_viagem_pai'] += 1
                        continue

                    if entidade == 'trecho':
                        # CHECK de sequencia unica por viagem, declarada no SQL.
                        if convertido[1] is None:
                            contagem['sequencia_vazia'] += 1
                            continue
                        par = (id_viagem, convertido[1])
                        if par in sequencias_vistas:
                            contagem['duplicadas'] += 1
                            continue
                        sequencias_vistas.add(par)

                    bloco.append(convertido)
                    if len(bloco) >= TAMANHO_BLOCO:
                        copiar_linhas(escrita, entidade, bloco)
                        contagem['inseridas'] += len(bloco)
                        bloco.clear()
                except (ValueError, OverflowError) as erro:
                    contagem['invalidas'] += 1
                    if contagem['invalidas'] <= 3:
                        print(f'  Exemplo de linha rejeitada em {entidade}: {erro}')

        if bloco:
            copiar_linhas(escrita, entidade, bloco)
            contagem['inseridas'] += len(bloco)
        print(f'silver_{entidade}: {dict(contagem)}')
        return contagem
    finally:
        leitura.close()
        escrita.close()


def main():
    leitor = escritor = None
    try:
        leitor = conectar()
        escritor = conectar()
        with escritor.cursor() as cursor:
            # Reinicio seguro de todas as tabelas Silver respeitando as FKs.
            cursor.execute('TRUNCATE TABLE silver_pagamento, silver_passagem, '
                           'silver_trecho, silver_viagem RESTART IDENTITY')

        ids_validos = set()
        sequencias_vistas = set()
        relatorio = {}
        # Sempre carregar a tabela pai antes das tabelas filhas.
        for entidade in ('viagem', 'pagamento', 'passagem', 'trecho'):
            relatorio[entidade] = ler_e_transformar(
                leitor, escritor, entidade, ids_validos, sequencias_vistas
            )
        escritor.commit()
        print('\nFASE 2 finalizada! Dados limpos e FKs preservadas.')
        print('Resumo dos registros importados:')
        for entidade, numeros in relatorio.items():
            print(f"- {entidade}: {numeros['inseridas']:,} registros Silver")
    except Exception as erro:
        if escritor:
            escritor.rollback()
        print(f'ERRO na Fase 2: {erro}')
        raise
    finally:
        if leitor:
            leitor.close()
        if escritor:
            escritor.close()


if __name__ == '__main__':
    main()
