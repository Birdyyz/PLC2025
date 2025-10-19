import json
from datetime import datetime

FICHEIRO_STOCK = "stock.json"
MOEDAS = {
    "2e": 200, "1e": 100,
    "50c": 50, "20c": 20, "10c": 10,
    "5c": 5, "2c": 2, "1c": 1
}

stock = []
saldo = 0

def carregar_stock():
    global stock
    data = datetime.now()
    data_formatada = data.strftime("%Y-%m-%d")
    try:
        with open(FICHEIRO_STOCK, "r", encoding="utf-8") as f:
            stock = json.load(f)
        print(f"maq: {data_formatada}, Stock carregado, Estado atualizado.")
    except FileNotFoundError:
        print("maq: 'stock.json' não encontrado. Novo stock.")
        stock = []

def guardar_stock():
    with open(FICHEIRO_STOCK, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=2, ensure_ascii=False)

def listar_produtos():
    print("maq:\n" \
          f"{'cod':<5} | {'nome':<20} | {'quantidade':<10} | {'preço':<6}\n" \
          + "-" * 55)
    for produto in stock:
        print(f"{produto['cod']:<5} | {produto['nome']:<20} | {produto['quantidade']:<10} | {produto['preco']:<.2f}")


def formatar_saldo(saldo_em_centimos):
    euros = saldo_em_centimos // 100
    centimos = saldo_em_centimos % 100
    return f"{euros}e{centimos:02d}c"

def inserir_moeda(entrada):
    global saldo
    entrada = entrada.replace(".", "").strip()
    lista_codigos = [moeda.strip() for moeda in entrada.split(",")]
    for moeda in lista_codigos:
        if moeda in MOEDAS:
            saldo += MOEDAS[moeda]
        else:
            print(f"maq: Moeda '{moeda}' inválida.")
    print(f"maq: Saldo = {formatar_saldo(saldo)}")

def selecionar_produto(codigo):
    global saldo
    codigo = codigo.strip()
    for produto in stock:
        if produto['cod'] == codigo:
            if produto['quantidade'] <= 0:
                print(f"maq: Produto '{produto['nome']}' esgotado.")
                return
            preco_centimos = int(produto['preco'] * 100)
            if saldo >= preco_centimos:
                saldo -= preco_centimos
                produto['quantidade'] -= 1
                print(f"maq: Pode retirar o produto dispensado: '{produto['nome']}'")
                print(f"maq: Saldo = {formatar_saldo(saldo)}")
            else:
                print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
                print(f"maq: Saldo = {formatar_saldo(saldo)}; Pedido = {formatar_saldo(preco_centimos)}")
            return
    print(f"maq: Produto com código '{codigo}' não encontrado.")

def calcular_troco():
    global saldo
    MOEDAS_DISPONIVEIS = ["2e", "1e", "50c", "20c", "10c", "5c", "2c", "1c"]
    VALORES_CENTIMOS = {
        "2e": 200, "1e": 100,
        "50c": 50, "20c": 20, "10c": 10,
        "5c": 5, "2c": 2, "1c": 1
    }
    troco = {}
    restante = saldo

    for moeda in MOEDAS_DISPONIVEIS:
        valor = VALORES_CENTIMOS[moeda]
        quantidade = restante // valor
        if quantidade > 0:
            troco[moeda] = quantidade
            restante -= quantidade * valor

    if troco:
        partes = [f"{qtd}x {moeda}" for moeda, qtd in troco.items()]
        print("maq: Pode retirar o troco: " + ", ".join(partes) + ".")
    else:
        print("maq: Não há troco a devolver.")
    
    saldo = 0  

def adicionar_produto(args):
    if len(args) == 2:
        cod, quant = args[0], args[1]
        for produto in stock:
            if produto["cod"] == cod:
                try:
                    produto["quantidade"] += int(quant)
                    print(f"maq: Quantidade de '{produto['nome']}' atualizada para {produto['quantidade']}.")
                except ValueError:
                    print("maq: Quantidade inválida.")
                return
        print(f"maq: Produto com código '{cod}' não encontrado.")

    elif len(args) >= 4:
        cod = args[0]
        quant = args[-2]
        preco = args[-1]
        nome = " ".join(args[1:-2])
        try:
            novo = {
                "cod": cod,
                "nome": nome,
                "quantidade": int(quant),
                "preco": float(preco)
            }
            stock.append(novo)
            print(f"maq: Produto '{nome}' adicionado com sucesso.")
        except ValueError:
            print("maq: Quantidade ou preço inválido.")
    else:
        print("maq: Formato inválido. Use:\n - ADICIONAR <cod> <quant>\n - ADICIONAR <cod> <nome> <quant> <preco>")

def main():
    carregar_stock()
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    while True:
        comando = input(">> ").strip()
        if comando.upper() == "LISTAR":
            listar_produtos()
        elif comando.upper().startswith("MOEDA"):
            moedas = comando[6:].strip()
            inserir_moeda(moedas)
        elif comando.upper().startswith("SELECIONAR"):
            cod = comando[10:].strip()
            selecionar_produto(cod)
        elif comando.upper().startswith("ADICIONAR"):
            args = comando[10:].strip().split()
            adicionar_produto(args)
        elif comando.upper() == "SAIR":
            calcular_troco()
            guardar_stock()
            print("maq: Até à próxima")
            break
        else:
            print("maq: Comando não reconhecido.")

if __name__ == "__main__":
    main()
