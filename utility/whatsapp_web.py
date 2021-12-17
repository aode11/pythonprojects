import webbrowser, sys, pyperclip

sys.argv

# Checks if command line arguments were passed
if len(sys.argv) > 1:
    telefone = ' '.join(sys.argv[1:])
else:
    telefone = pyperclip.paste()

telefone = telefone.replace(' ','').replace('(','').replace(')','').replace('-','')

webbrowser.open('https://api.whatsapp.com/send?phone=55' + telefone)