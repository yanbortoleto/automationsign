import os
import time
import shutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pyautogui

# Diretórios
WATCH_DIRECTORY = r"C:\Assinador"
SIGNED_DIRECTORY = os.path.join(WATCH_DIRECTORY, "signed")

# Configuração do signtool e senha
TOKEN_PASSWORD = "SENHA DO TOKEN" #Existem algumas versoes que utilizam senha.

# Verificar se a pasta signed existe, caso contrário, criar
if not os.path.exists(SIGNED_DIRECTORY):
    os.makedirs(SIGNED_DIRECTORY)

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.lower().endswith(".exe"):
            self.handle_new_file(event.src_path)

    def handle_new_file(self, file_path):
        print(f"Novo arquivo detectado: {file_path}")
        time(30)
        self.sign_file(file_path)

    def sign_file(self, file_path):
        print(f"Assinando arquivo: {file_path}")
        while True:
            try:
                # Verificar se o signtool está no PATH
                signtool_path = shutil.which("signtool")
                if signtool_path is None:
                    print(f"Variável PATH atual: {os.environ['PATH']}")
                    raise FileNotFoundError("signtool não foi encontrado no PATH.")

                # Comando para assinar o arquivo
                command = [
                    signtool_path, "sign", "/tr", "http://timestamp.sectigo.com",
                    "/td", "sha256", "/fd", "sha256", "/a", file_path
                ]
                process = subprocess.Popen(command)

                # Esperar um pouco para a janela do SafeNet aparecer
                time.sleep(2)

                # Digitar a senha na janela do SafeNet
                windows = pyautogui.getWindowsWithTitle("Token Logon")
                if windows:
                    windows[0].activate()
                    pyautogui.typewrite(TOKEN_PASSWORD)
                    pyautogui.press('enter')
                else:
                    raise Exception("Janela 'Token Logon' não encontrada.")

                # Esperar o término do processo
                process.wait()

                # Mover o arquivo para a pasta signed
                signed_file_path = os.path.join(SIGNED_DIRECTORY, os.path.basename(file_path))
                shutil.move(file_path, signed_file_path)
                print(f"Arquivo assinado e movido para: {signed_file_path}")
                break  # Sair do loop se tudo correr bem

            except Exception as e:
                print(f"Erro ao assinar o arquivo: {e}")
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)  # Esperar antes de tentar novamente

if __name__ == "__main__":
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
    observer.start()
    print(f"Monitorando a pasta: {WATCH_DIRECTORY}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
