import datetime
import decimal
import strawberry
from typing import List, Optional
from db.database import SessionLocal
from sqlalchemy import text
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent.parent / "db" / "querys"
JSON = strawberry.scalar(dict, name="JSON")


@strawberry.type
class Query:
    @strawberry.field
    def dados(
        self,
        offset: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = "asc",
        where: Optional[JSON] = None
    ) -> List[JSON]:
        db = SessionLocal()
        sql_str = carregar_sql("get_all_itens.sql")

        query = text(sql_str)

        if where:
            conditions = []
            for column, filters in where.items():
                for operator, value in filters.items():
                    if operator == "eq":
                        conditions.append(f"{column} = :{column}_value")
                    elif operator == "dif":
                        conditions.append(f"{column} != :{column}_value")
                    elif operator == "maq":
                        conditions.append(f"{column} > :{column}_value")
                    elif operator == "meq":
                        conditions.append(f"{column} < :{column}_value")
                    elif operator == "maig":
                        conditions.append(f"{column} >= :{column}_value")
                    elif operator == "meig":
                        conditions.append(f"{column} <= :{column}_value")
                    elif operator == "like":
                        conditions.append(f"{column} LIKE :{column}_value")
                    elif operator == "in":
                        conditions.append(f"{column} IN :{column}_value")

            if conditions:
                where_clause = " AND ".join(conditions)
                sql_str = f"SELECT * FROM (SELECT * FROM ({sql_str}) subquery WHERE {where_clause}) subquery"

        if order_by:
            direction = "DESC" if order_direction and order_direction.lower() == "desc" else "ASC"
            sql_str = f"SELECT * FROM ({sql_str}) subquery ORDER BY {order_by} {direction}"

        sql_str = f"{sql_str} OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY"

        params = {"offset": offset, "limit": limit}

        if where:
            for column, filters in where.items():
                for operator, value in filters.items():
                    params[f"{column}_value"] = value

        resultado = db.execute(text(sql_str), params)
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
