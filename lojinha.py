import uvicorn
from fastapi import FastAPI

app = FastAPI()


loja = {
    'categorias': {},
    'depositos': {},
    'clientes': {},
    'cupons': {}
}
#atalhos
categorias = loja['categorias']
depositos = loja['depositos']
clientes = loja['clientes']
cupons = loja['cupons']

 
@app.get('/cadastrar-categoria')
def cadastrar_categoria(nome):
    global loja
    loja['categorias'][nome] = [] #adicionar produtos depois
    return loja


@app.get('/adicionar-produto')
def adicionar_produto(categoria, nome, preco):
    produto = {
        'nome': nome,
        'preco': preco
    }
    if categoria not in categorias:
        return "Categoria não existe"
    
    lista = loja['categorias'][categoria]
    lista.append(produto)
    
    return loja


@app.get('/cadastrar-deposito')
def cadastrar_deposito(nome_deposito, cidade):

    deposito = {
        'nome': nome_deposito,
        'cidade': cidade,
        'itens': {}
    }
    depositos[nome_deposito] = deposito

    return loja


@app.get('/abastecer-estoque')
def abastecer_estoque(nome_deposito, item, quantidade):
    erros = []

    if nome_deposito not in depositos:
        erros.append('Depósito não existe')

    quantidade = int(quantidade)

    if quantidade < 0:
        erros.append('A quantidade deve ser positiva')

    if len(erros) > 0:
        return erros
    
    itens = depositos[nome_deposito]['itens']
    if item in itens:
        quantidade = quantidade + itens[item]['quantidade']

    itemFinal =  {
        'item': item,
        'quantidade': quantidade
    }
    itens[item] = itemFinal

    return loja


@app.get('/cadastrar-cliente')
def cadastro(nome, email):
    global loja

    cliente = {
        'nome': nome,
        'email': email,
        'pedidos': []
    }

    clientes[email] = cliente

    return loja

@app.get('/criar-pedido')
def criar(email, id_pedido):
    cliente = clientes[email]

    pedido = {
        'id pedido': id_pedido,
        'itens': []
    }

    cliente['pedidos'].append(pedido)

    return loja


@app.get('/adicionar-item-pedido')
def adicionar(email, id_pedido, produto, valor):
    cliente = clientes[email]

    try:
        valor = valor.replace(',', '.')
        valor = float(valor)
    except:
        return 'Valor do produto inválido'

    pedido_encontrado = None
    for pedido in cliente['pedidos']:
        if pedido['id pedido'] == id_pedido:
            pedido_encontrado = pedido

    if pedido_encontrado is None:
        return "Erro: pedido não encontrado"

    produto_venda = {
        'produto': produto,
        'valor': valor
    }
    pedido_encontrado['itens'].append(produto_venda)

    return loja

@app.get('/criar-cupom')
def criar(codigo, desconto):
    desconto = int(desconto)
    cupons[codigo] = desconto
    return loja


@app.get('/aplicar-cupom-produto')
def aplicar_cupom_produto(categoria, nome_produto, codigo_cupom):
    if codigo_cupom not in cupons:
        return 'Cupom não existe'

    if categoria not in categorias:
        return 'Categoria não existe'

    for produto in categorias[categoria]:
        if produto['nome'] == nome_produto:
            desconto = cupons[codigo_cupom]
            preco_original = float(produto['preco'])
            produto['preco'] = preco_original * (1 - desconto / 100)
            return loja

    return 'Produto não existe'


@app.get('/')
def ver_loja():
    return loja


if __name__ == '__main__':
    uvicorn.run(
        'lojinha:app',
        port=80,
        reload=True
    )
