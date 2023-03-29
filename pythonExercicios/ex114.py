import urllib.request

try:
    site = urllib.request.urlopen('http://www.pudim.com.br')
except urllib.error.URLError:
    print(f'\033[1;31mERRO ! O site não está acessível no momento.\033[m')
else:
    print(f'\033[1;32mConsegui acessar o site PUDIM com sucesso.\033[m')
