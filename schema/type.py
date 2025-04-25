import strawberry


@strawberry.type
class ContratoAnalitico:
    id: int
    codigo: str
    nome: str
    data_criacao: str
    ativo: bool
    valor_total: float
    categoria: str
    usuario_criacao: str
    ultima_atualizacao: str
    status: str
