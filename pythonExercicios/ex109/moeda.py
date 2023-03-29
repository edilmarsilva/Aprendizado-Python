def aumentar(p=0, taxa=0, formato=False):
    res = p + (p * taxa / 100)
    if formato is False:
        return res
    else:
        return moeda(res)

def diminuir(p=0, taxa=0, formato=False):
    res = p - (p * 13 / 100)
    if formato is False:
        return res
    else:
        return moeda(res)


def dobro(p=0, formato=False):
    res = p * 2
    if formato is False:
        return res
    else:
        return moeda(res)


def metade(p=0, formato=False):
    res = p / 2
    if formato is False:
        return res
    else:
        return moeda(res)


def moeda(p=0, moeda='R$', format=False):
    return f'{moeda} {p:.2f}'.replace('.', ',')

