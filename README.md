Primeiro, instale as bibliotecas necessárias:

pip install watchdog pyautogui

Certifique-se de ter instalado as SDK Sign Tools do windows na maquina em que o script vai rodar.

E baixe o driver necessario e ajuste o campo de senha / ou certificado que deseja utilizar.


Certifique-se de mudar o diretorio da pasta que deseja monitorar.

Diretórios
WATCH_DIRECTORY = r"C:\Caminho\Para\Sua\Pasta\Monitorada"

Mudar caso necessário conforme no titulo da janela
windows = pyautogui.getWindowsWithTitle("Token Logon") #
