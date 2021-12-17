import webbrowser, sys, pyperclip

sys.argv

# Checks if command line arguments were passed
if len(sys.argv) > 1:
    champion_name = ' '.join(sys.argv[1:])
else:
    champion_name = pyperclip.paste()

champion_name = champion_name.replace(' ', '').replace("'", '')

webbrowser.open('https://op.gg/champion/' + champion_name)