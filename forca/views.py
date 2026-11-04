
from django.shortcuts import render, redirect
import random
from .palavras import palavras


def inicio(request):

    # 1. Reiniciar a partida quando clicar em Nova Partida
    if request.method == "POST" and "nova_partida" in request.POST:
        for chave in ["palavra", "dica", "letras"]:
            request.session.pop(chave, None)

        return redirect("inicio")

    # 2. Sortear uma palavra se ainda nao existir partida
    if "palavra" not in request.session:
        sorteada = random.choice(palavras)

        request.session["palavra"] = sorteada["palavra"]
        request.session["dica"] = sorteada["dica"]
        request.session["letras"] = []

    # 3. Recuperar os dados da partida
    palavra = request.session["palavra"]
    letras = request.session.get("letras", [])

    # 4. Verificar se a partida ja terminou
    erros_atuais = sum(1 for letra in letras if letra not in palavra)

    ganhou_antes = all(letra in letras for letra in palavra)
    perdeu_antes = erros_atuais >= 6

    # 5. Receber uma nova tentativa somente se o jogo nao terminou
    if request.method == "POST" and not ganhou_antes and not perdeu_antes:

        letra = request.POST.get("letra", "").strip().upper()

        if len(letra) == 1 and letra.isalpha() and letra not in letras:
            letras.append(letra)
            request.session["letras"] = letras

    # 6. Montar os espacos da palavra secreta
    espacos = []

    for letra in palavra:
        if letra in letras:
            espacos.append(letra)
        else:
            espacos.append("_")

    # 7. Contar os erros
    erros = 0

    for letra in letras:
        if letra not in palavra:
            erros += 1

    # 8. Verificar vitoria ou derrota
    ganhou = "_" not in espacos
    perdeu = erros >= 6
    terminou = ganhou or perdeu

    # 9. Enviar os dados para o HTML
    return render(request, "forca/index.html", {
        "dica": request.session["dica"],
        "espacos": espacos,
        "letras": letras,
        "erros": erros,
        "ganhou": ganhou,
        "perdeu": perdeu,
        "terminou": terminou,
        "palavra": palavra if perdeu else ""
    })
