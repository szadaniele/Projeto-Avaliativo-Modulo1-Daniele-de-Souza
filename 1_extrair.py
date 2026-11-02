"""FASE 1: importar os quatro CSVs originais para as tabelas raw_*."""

import csv
import io
import zipfile
import shutil
from pathlib import Path

from banco import conectar
from config import (
    ARQUIVOS, DRIVE_FILE_ID, DRIVE_FOLDER_ID, PASTA_DADOS, TAMANHO_BLOCO
)


NOME_ZIP = "viagens_2025_6meses.zip"


def obter_zip():
    """Usa o ZIP local ou, se ausente, baixa a copia disponibilizada no Drive."""
    PASTA_DADOS.mkdir(exist_ok=True)
    caminho = PASTA_DADOS / NOME_ZIP
    if caminho.is_file():
        print(f"Arquivo local encontrado: {caminho}")
        return caminho

    import gdown  # So precisa acessar a internet se nao houver ZIP local.
    print("Baixando os arquivos disponibilizados no Google Drive...")
    if DRIVE_FILE_ID:
        # Modo alternativo: usuario informa o ID de um arquivo especifico.
        gdown.download(id=DRIVE_FILE_ID, output=str(caminho), quiet=False)
    elif DRIVE_FOLDER_ID:
        # Link de PASTA do PDF: gdown.download(id=...) nao funciona com pastas.
        arquivos = gdown.download_folder(
            id=DRIVE_FOLDER_ID, output=str(PASTA_DADOS), quiet=False
        )
        zips = [Path(f) for f in (arquivos or [])
                if str(f).lower().endswith('.zip')]
        if len(zips) == 1 and zips[0].resolve() != caminho.resolve():
            shutil.move(str(zips[0]), str(caminho))
        elif len(zips) > 1:
            raise RuntimeError(
                'A pasta tem mais de um ZIP. Baixe a amostra correta para data/.'
            )
    else:
        raise FileNotFoundError(
            f"Coloque {NOME_ZIP} em data/ ou configure o Drive no .env."
        )
    if not caminho.is_file():
        raise RuntimeError(
            f'Nao foi possivel baixar {NOME_ZIP}. Confira o acesso ao Drive.'
        )
    return caminho


def carregar_csv(conexao, arquivo_zip, nome_csv, tabela):
    """Le em blocos e copia o conteudo exato de cada celula para a tabela Raw."""
    total = 0
    with arquivo_zip.open(nome_csv) as arquivo:
        texto = io.TextIOWrapper(arquivo, encoding="latin-1", newline="")
        leitor = csv.reader(texto, delimiter=";")
        cabecalho = next(leitor)

        with conexao.cursor() as cursor:
            # Todas as tabelas Raw foram criadas na mesma ordem das colunas do CSV.
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.columns "
                "WHERE table_schema = 'public' AND table_name = %s",
                (tabela,),
            )
            qtd_colunas = cursor.fetchone()[0]
            if len(cabecalho) != qtd_colunas:
                raise ValueError(
                    f"{nome_csv}: CSV tem {len(cabecalho)} colunas, "
                    f"mas {tabela} tem {qtd_colunas}."
                )

            # TRUNCATE torna a carga idempotente (sem duplicar em reexecucoes).
            cursor.execute(f"TRUNCATE TABLE {tabela}")
            bloco = []
            comando = (
                f"COPY {tabela} FROM STDIN "
                "WITH (FORMAT CSV, DELIMITER ';', NULL '\\N')"
            )

            for linha in leitor:
                if len(linha) != len(cabecalho):
                    raise ValueError(
                        f"Linha {total + 2} de {nome_csv} com tamanho incorreto."
                    )
                # Nao usar strip(), float(), replace() nem converter datas na RAW.
                bloco.append(linha)
                if len(bloco) == TAMANHO_BLOCO:
                    copiar_bloco(cursor, comando, bloco)
                    total += len(bloco)
                    bloco.clear()

            if bloco:
                copiar_bloco(cursor, comando, bloco)
                total += len(bloco)

    return total


def copiar_bloco(cursor, comando, linhas):
    """COPY e eficiente com grandes volumes e preserva zeros a esquerda."""
    memoria = io.StringIO()
    escritor = csv.writer(memoria, delimiter=";", lineterminator="\n")
    escritor.writerows(linhas)
    memoria.seek(0)
    cursor.copy_expert(comando, memoria)


def main():
    conexao = None
    try:
        caminho = obter_zip()
        conexao = conectar()
        with zipfile.ZipFile(caminho, "r") as arquivo_zip:
            nomes = set(arquivo_zip.namelist())
            esperados = {info["csv"] for info in ARQUIVOS.values()}
            if not esperados.issubset(nomes):
                raise ValueError(f"Arquivos ausentes no ZIP: {esperados - nomes}")

            for info in ARQUIVOS.values():
                try:
                    quantidade = carregar_csv(
                        conexao, arquivo_zip, info["csv"], info["tabela_raw"]
                    )
                    conexao.commit()  # Confirma somente apos cada arquivo completo.
                    print(f"{info['tabela_raw']}: {quantidade:,} linhas carregadas.")
                except Exception:
                    conexao.rollback()  # Uma carga parcial nao altera a tabela.
                    raise
        print("FASE 1 concluida: quatro tabelas Raw preenchidas!")
    except Exception as erro:
        print(f"ERRO na Fase 1: {erro}")
        raise
    finally:
        if conexao:
            conexao.close()


if __name__ == "__main__":
    main()
