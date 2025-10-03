import re

def markdown_para_html(texto):
    linhas = texto.split("\n")
    html = []
    dentro_lista = False

    for linha in linhas:
        # #Exemplo -> <h1>Exemplo</h1>
        if linha.startswith("### "):
            html.append(f"<h3>{linha[4:]}</h3>")
        elif linha.startswith("## "):
            html.append(f"<h2>{linha[3:]}</h2>")
        elif linha.startswith("# "):
            html.append(f"<h1>{linha[2:]}</h1>")

        # Lista numerada
        elif re.match(r"^\d+\.\s", linha):
            if not dentro_lista:
                html.append("<ol>")
                dentro_lista = True
            item = linha.split(". ", 1)[1]
            html.append(f"<li>{item}</li>")

        else:
            if dentro_lista:
                html.append("</ol>")
                dentro_lista = False

            #Como se vê na imagem seguinte: `![imagem dum coelho](http://www.coellho.com) -> Como se vê na imagem seguinte: <img src="http://www.coellho.com" alt="imagem dum coelho"/>
            linha = re.sub(r"!\[(.*?)\]\((.*?)\)", r'<img src="\2" alt="\1"/>', linha)

            # Como pode ser consultado em [página da UC](http://www.uc.pt) -> Como pode ser consultado em <a href="http://www.uc.pt">página da UC</a>
            linha = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', linha)

            # Este é um **exemplo** -> Este é um <b>exemplo<b>
            linha = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", linha)

            # Este é um *exemplo* -> Este é um <i>exemplo<i>
            linha = re.sub(r"\*(.*?)\*", r"<i>\1</i>", linha)

            html.append(linha)

    if dentro_lista:
        html.append("</ol>")

    return "\n".join(html)

       