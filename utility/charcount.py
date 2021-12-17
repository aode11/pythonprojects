import pprint
import sys
from tkinter import Tk

# se um argumento foi passado, cria uma string concatenando com espaços, caso contrário, apenas usa a área de cópia do windows
if len(sys.argv) > 1:
	message = ' '.join(sys.argv[1:])
else:
	message = Tk().clipboard_get()

# cria um dicionário em branco que iremos preencher com o método abaixo
count = {}

# passa todos os caracteres para maiúsculo, e conta cada caractere único
for character in message.upper():
	count.setdefault(character, 0)
	count[character] = count[character] + 1

# conta a quantidade de palavras
if len(sys.argv) > 1:
	palavras = len(sys.argv[1:])
else:
	palavras = count[' '] + 1

# imprime as contagens relevantes
print('String original: "' + message + '"')
print('Total de caracteres: ' + str(len(message)))
print('Total de palavras: ' + str(palavras))
pprint.pprint(count)