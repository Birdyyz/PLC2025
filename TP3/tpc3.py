import sys
import json
import re

def main():
    if len(sys.argv) < 2:
        print("Uso: python tpc3.py <query.txt>")
        sys.exit(1)

    try:
        with open('tokens.json', 'r', encoding='utf-8') as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print("Erro: ficheiro 'tokens.json' não encontrado.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Erro: ficheiro 'tokens.json' não é um JSON válido.")
        sys.exit(1)
        
    filename = sys.argv[1]
    tokens_regex = '|'.join([f"(?P<{t['id']}>{t['expreg']})" for t in tokens])

    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Erro: ficheiro '{filename}' não encontrado.")
        sys.exit(1)

    reconhecidos = []
    linha = 1

    for m in re.finditer(tokens_regex, code, re.IGNORECASE):
        dic = m.groupdict()
        token = None

        for t in tokens:
            if dic.get(t['id']):
                token = (t['id'], dic[t['id']], linha, m.span())
        if token is None:
            token = ("UNKNOWN", m.group(), linha, m.span())

        reconhecidos.append(token)

    for tok in reconhecidos:
        print(tok)

if __name__ == "__main__":
    main()
