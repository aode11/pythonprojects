import webbrowser, sys, pyperclip

sys.argv

# Checks if command line arguments were passed
if len(sys.argv) > 1:
    search_term = ' '.join(sys.argv[1:])
else:
    search_term = pyperclip.paste()

webbrowser.open('https://www.google.com/search?q=' + search_term)