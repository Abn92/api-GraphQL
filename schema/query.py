import datetime
import decimal
import strawberry
from typing import List
from db.database import SessionLocal
from sqlalchemy import text
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent.parent / "db" / "querys"
JSON = strawberry.scalar(dict, name="JSON")


@strawberry.type
class Query:
    @strawberry.field
    def dados(self, offset: int = 0, limit: int = 100) -> List[JSON]:
        db = SessionLocal()
        sql_str = carregar_sql("get_all_itens.sql")
        resultado = db.execute(
            text(sql_str), {"offset": offset, "limit": limit})
        colunas = list(resultado.keys())

        dados = []
        for row in resultado:
            linha = {}
            for i, valor in enumerate(row):
                if isinstance(valor, (datetime.date, datetime.datetime)):
                    valor = valor.isoformat()
                elif isinstance(valor, decimal.Decimal):
                    valor = float(valor)
                linha[colunas[i]] = valor
            dados.append(linha)

        db.close()
        return dados

    @strawberry.field
    def dados_filtrados(
        self,
        campo: str,
        valor: str,
        offset: int = 0,
        limit: int = 100
    ) -> List[JSON]:
        db = SessionLocal()
        sql_str = carregar_sql("get_filtered_itens.sql").format(campo=campo)
        resultado = db.execute(
            text(sql_str), {"valor": valor, "offset": offset, "limit": limit})
        colunas = list(resultado.keys())

        dados = []
        for row in resultado:
            linha = {}
            for i, valor in enumerate(row):
                if isinstance(valor, (datetime.date, datetime.datetime)):
                    valor = valor.isoformat()
                elif isinstance(valor, decimal.Decimal):
                    valor = float(valor)
                linha[colunas[i]] = valor
            dados.append(linha)

        db.close()
        return dados


def carregar_sql(nome_arquivo: str) -> str:
    with open(SQL_DIR / nome_arquivo, encoding="utf-8") as f:
        return f.read()


schema = strawberry.Schema(query=Query)
