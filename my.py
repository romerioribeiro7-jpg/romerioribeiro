from datetime import datetime
import math
import re


def calcular(expressao):
    padrao = re.compile(
        r"\s*(\d+(?:[.,]\d*)?|[.,]\d+|\*\*|//|[()+\-*/%^]|"
        r"mais|menos|vezes|dividido\s+por|mod(?:ulo)?)",
        re.IGNORECASE,
    )
    tokens = []
    posicao = 0

    while posicao < len(expressao):
        correspondencia = padrao.match(expressao, posicao)
        if correspondencia is None:
            raise ValueError(f"Caractere inválido na posição {posicao + 1}.")

        token = correspondencia.group(1).lower()
        posicao = correspondencia.end()
        if token == "mais":
            token = "+"
        elif token == "menos":
            token = "-"
        elif token == "vezes":
            token = "*"
        elif token.startswith("dividido"):
            token = "/"
        elif token in ("mod", "modulo"):
            token = "%"
        tokens.append(token)

    if not tokens:
        raise ValueError("Digite uma conta.")

    indice = 0

    def expressao_soma():
        nonlocal indice
        resultado = expressao_multiplicacao()
        while indice < len(tokens) and tokens[indice] in ("+", "-"):
            operador = tokens[indice]
            indice += 1
            direita = expressao_multiplicacao()
            resultado = resultado + direita if operador == "+" else resultado - direita
        return resultado

    def expressao_multiplicacao():
        nonlocal indice
        resultado = expressao_unaria()
        while indice < len(tokens) and tokens[indice] in ("*", "/", "//", "%"):
            operador = tokens[indice]
            indice += 1
            direita = expressao_unaria()

            if operador in ("/", "//", "%") and direita == 0:
                raise ZeroDivisionError
            if operador == "*":
                resultado *= direita
            elif operador == "/":
                resultado /= direita
            elif operador == "//":
                resultado //= direita
            else:
                resultado %= direita
        return resultado

    def expressao_unaria():
        nonlocal indice
        if indice < len(tokens) and tokens[indice] in ("+", "-"):
            operador = tokens[indice]
            indice += 1
            valor = expressao_unaria()
            return valor if operador == "+" else -valor
        return expressao_potencia()

    def expressao_potencia():
        nonlocal indice
        resultado = valor_primario()
        if indice < len(tokens) and tokens[indice] in ("^", "**"):
            indice += 1
            resultado **= expressao_unaria()
        return resultado

    def valor_primario():
        nonlocal indice
        if indice >= len(tokens):
            raise ValueError("A conta está incompleta.")

        token = tokens[indice]
        if token == "(":
            indice += 1
            resultado = expressao_soma()
            if indice >= len(tokens) or tokens[indice] != ")":
                raise ValueError("Falta fechar um parêntese.")
            indice += 1
            return resultado

        if token in (")", "+", "-", "*", "/", "//", "%", "^", "**"):
            raise ValueError("A conta está incompleta ou mal formatada.")

        indice += 1
        return float(token.replace(",", "."))

    resultado = expressao_soma()
    if indice != len(tokens):
        raise ValueError("Verifique os operadores e parênteses da conta.")
    if isinstance(resultado, complex) or not math.isfinite(resultado):
        raise ValueError("O resultado precisa ser um número real finito.")
    return resultado


print("Bem-vindo à sua assistente virtual!")

nome = input("Digite seu nome: ").strip()
if not nome:
    nome = "usuário"

print(f"Olá, {nome}! Seja bem-vindo!")

while True:
    print("\nMenu: oi, nome, hora, data, calcular, sair")
    comando = input("Escolha uma opção: ").strip().lower()

    if comando == "sair":
        print("Até logo!")
        break
    elif comando == "oi":
        print(f"Oi, {nome}! Como posso ajudar?")
    elif comando == "nome":
        print(f"Seu nome é {nome}.")
    elif comando == "hora":
        print(f"Agora são {datetime.now().strftime('%H:%M:%S')}.")
    elif comando == "data":
        print(f"Hoje é {datetime.now().strftime('%d/%m/%Y')}.")
    elif comando == "calcular":
        conta = input(
            "Digite a conta: "
        ).strip()
        try:
            resultado = calcular(conta)
        except ZeroDivisionError:
            print("Não é possível dividir por zero.")
        except (ValueError, OverflowError) as erro:
            print(f"Não foi possível calcular: {erro}")
        else:
            print(f"Resultado: {resultado:.15g}")
    else:
        print("Opção inválida. Escolha uma opção do menu.")
