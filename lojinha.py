import uvicorn
from fastapi import FastAPI

app = FastAPI()


loja = {
    'categorias': {},
    'depositos': {},
    'clientes': {}
}
#atalhos
categorias = loja['categorias']
depositos = loja['depositos']
clientes = loja['clientes']

 
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
        'pedidos': {}
    }

    clientes[email] = cliente

    return loja

@app.get('/criar-pedido')
def criar(email, id_pedido):
    cliente = clientes[email]   # 'cliente' é apenas 1 cliente, enquanto 'clientes' é todos 

    pedido = {
        'id pedido': id_pedido,
        'itens': {}
    }
    pedidos = cliente['pedidos']
    
    pedidos[id_pedido] = pedido

    return loja


@app.get('/adicionar-produto-pedido')
def adicionar(email, id_pedido, produto, valor):
    cliente = clientes[email]
    pedido = cliente['pedidos'][id_pedido]

    produto_venda = {
        'produto': produto,
        'valor': valor
    }
    pedido['itens'][produto] = produto_venda

    return loja


@app.get('/')
def ver_loja():
    return loja


if __name__ == '__main__':
    uvicorn.run(
        'lojinha:app',
        port=80,
        reload=True
    )
