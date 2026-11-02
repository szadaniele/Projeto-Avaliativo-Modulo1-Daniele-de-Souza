"""Testes sem banco: execute python -m pytest testes/ -v."""

from decimal import Decimal
from datetime import date
import pytest

from transformacoes import (
    data_br, decimal_br, dinheiro_nao_negativo, texto,
    transformar_viagem, transformar_trecho,
)


def test_decimal_brasileiro():
    assert decimal_br('1.272,97') == Decimal('1272.97')
    assert decimal_br('0,00') == Decimal('0.00')
    assert decimal_br('Sem informação') is None


def test_data_brasileira():
    assert data_br('31/03/2025') == date(2025, 3, 31)
    assert data_br('') is None
    with pytest.raises(ValueError):
        data_br('31/02/2025')


def test_campos_basicos():
    assert texto(' 0000029 ') == '0000029'
    with pytest.raises(ValueError):
        dinheiro_nao_negativo('-1,00')


def test_viagem_calcula_total_e_duracao():
    exemplo = {
        'id_viagem': '00001', 'num_proposta': '01', 'situacao': 'Realizada',
        'viagem_urgente': 'NÃO', 'cod_orgao_superior': '1',
        'nome_orgao_superior': 'Orgão Exemplo', 'nome_viajante': 'Exemplo',
        'cargo': 'Servidor', 'data_inicio': '01/03/2025',
        'data_fim': '03/03/2025', 'destinos': 'SC', 'motivo': 'Reuniao',
        'valor_diarias': '100,00', 'valor_passagens': '250,00',
        'valor_devolucao': '50,00', 'valor_outros_gastos': '20,00',
    }
    saida = transformar_viagem(exemplo)
    assert saida[0] == '00001'
    assert saida[-2] == Decimal('320.00')
    assert saida[-1] == 3


def test_trecho_converte_sequencia_e_diarias():
    trecho = {
        'id_viagem': '001', 'sequencia_trecho': '3',
        'origem_data': '02/03/2025', 'origem_uf': 'SC',
        'origem_cidade': 'Florianópolis', 'destino_data': '03/03/2025',
        'destino_uf': 'PR', 'destino_cidade': 'Curitiba',
        'meio_transporte': 'Rodoviário', 'numero_diarias': '1,50',
    }
    saida = transformar_trecho(trecho)
    assert saida[1] == 3
    assert saida[-1] == Decimal('1.50')
