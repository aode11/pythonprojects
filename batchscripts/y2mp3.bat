@echo off

Rem Ativa o Anaconda Prompt no cmd. Dependências de módulos: youtube-dl e ffmpeg
	Echo Chamando Anaconda Prompt...
	call C:\Users\cross\anaconda3\Scripts\activate.bat C:\Users\cross\anaconda3\
	Echo.

Rem Roda a atualização do módulo youtube-dl, caso seja necessário
	Echo Atualizando o modulo youtube-dl...
	pip install --upgrade youtube-dl
	Echo.

Rem Roda a atualização do módulo ffmpeg, caso seja necessário
	Echo Atualizando o modulo ffmpeg...
	pip install --upgrade ffmpeg
	Echo.

Rem Muda a pasta em que o arquivo será salvo
	cd C:\Users\cross\PythonScripts\Youtube_Downloads

Rem Roda o script de download
Rem Nota: lista completa de comandos auxiliares do youtube-dl em https://github.com/ytdl-org/youtube-dl
	Echo Rodando o download como arquivo .mp3 pelo youtube-dl...
	@youtube-dl -i -x --geo-bypass --extract-audio --audio-format mp3 %*
	Echo.

Rem Mostra a pasta destino e a abre
	Echo Destino: %cd%
	start .