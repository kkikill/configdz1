import os
import tarfile
import sys
from collections import deque

class ShellEmulator:
    def __init__(self, hostname, tar_path):
        self.hostname = hostname
        self.tar_path = tar_path
        self.virtual_fs = {}
        self.current_dir = "/"
        self.history = deque(maxlen=10)  # Сохраняем последние 10 команд
        self.load_virtual_filesystem()

    def load_virtual_filesystem(self):
        # Проверяем, что TAR-архив существует и является файлом
        if not os.path.isfile(self.tar_path):
            print(f"Error: {self.tar_path} не является файлом.")
            sys.exit(1)

        # Извлекаем TAR-архив во временную директорию
        with tarfile.open(self.tar_path, 'r') as tar_ref:
            tar_ref.extractall("/tmp/vfs")
        self.virtual_fs = self.build_fs_structure("/tmp/vfs")

    def build_fs_structure(self, path):
        fs_structure = {}
        for dirpath, dirnames, filenames in os.walk(path):
            rel_path = os.path.relpath(dirpath, path)
            rel_path = "/" if rel_path == "." else f"/{rel_path}".replace("\\", "/")
            fs_structure[rel_path] = {
                "dirs": dirnames,
                "files": filenames
            }
        return fs_structure

    def list_directory(self):
        contents = self.virtual_fs.get(self.current_dir, {})
        dirs = contents.get("dirs", [])
        files = contents.get("files", [])
        return dirs + files

    def change_directory(self, new_dir):
        new_dir = new_dir.replace('\\', '/')
        if new_dir == "..":
            if self.current_dir != "/":
                self.current_dir = os.path.dirname(self.current_dir.rstrip('/'))
                if not self.current_dir:
                    self.current_dir = "/"
        else:
            if not new_dir.startswith("/"):
                new_dir = os.path.normpath(os.path.join(self.current_dir, new_dir))
                new_dir = new_dir.replace("\\", "/")
            if new_dir in self.virtual_fs:
                self.current_dir = new_dir
            else:
                return "No such directory."

    def history_command(self):
        return "\n".join(self.history)

    def uniq_command(self):
        files = self.list_directory()
        return "\n".join(sorted(set(files)))

    def tail_command(self):
        files = self.list_directory()
        return "\n".join(files[-10:])  # последние 10 строк

    def who(self):
        return self.hostname

    def rev(self):
        return self.current_dir[::-1]

    def execute_command(self, command):
        command = command.replace('\\', '/')
        parts = command.strip().split()
        if not parts:
            return ""
        cmd = parts[0]

        # Добавляем команду в историю
        self.history.append(command)

        if cmd == "ls":
            return "\n".join(self.list_directory())
        elif cmd == "cd":
            if len(parts) > 1:
                return self.change_directory(parts[1])
            else:
                return "No directory specified."
        elif cmd == "exit":
            sys.exit(0)
        elif cmd == "who":
            return self.who()
        elif cmd == "rev":
            return self.rev()
        elif cmd == "history":
            return self.history_command()
        elif cmd == "uniq":
            return self.uniq_command()
        elif cmd == "tail":
            return self.tail_command()
        else:
            return "Command not found."

def run_emulator(hostname, tar_path):
    emulator = ShellEmulator(hostname, tar_path)

    while True:
        # Выводим приглашение для ввода команды
        command = input(f"{emulator.hostname}:{emulator.current_dir}$ ").strip()

        if command:
            output = emulator.execute_command(command)
            if output:
                print(output)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <hostname> <tar_path>")
        sys.exit(1)

    hostname = sys.argv[1]
    tar_path = sys.argv[2]
    
    run_emulator(hostname, tar_path)
