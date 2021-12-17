import webbrowser, sys

try:
    # Encontra o separador de endereços
    separador = sys.argv.index(';')
    address1 = ' '.join(sys.argv[1:separador])
    address2 = ' '.join(sys.argv[separador+1:])

    # procura no google maps as rotas entre os endereços
    # https://www.google.com.br/maps/dir/<address1>/<address2>
    webbrowser.open('https://www.google.com.br/maps/dir/' + address1 + '/' + address2)
except:
    print('''O separador de endereços ';' não foi encontrado ou não estava isolado por espaços, tente novamente.''')