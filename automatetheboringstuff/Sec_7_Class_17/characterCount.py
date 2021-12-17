import pprint

message = input()
count = {} # 'r': 12

for character in message.upper():
	count.setdefault(character, 0)
	count[character] = count[character] + 1

rjtext = pprint.pformat(count)
print('Quantidade de caracteres total: ' + length(message) + '.' + rjtext)
