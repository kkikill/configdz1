import unittest
from io import StringIO
import sys

class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.hostname = "localhost"
        self.tar_path = "/path/to/vfs.tar"
        self.emulator = ShellEmulator(self.hostname, self.tar_path)

    def test_ls(self):
        # Тестирование команды ls
        self.emulator.current_dir = "/home"
        result = self.emulator.execute_command("ls")
        self.assertIn("file1.txt", result)

    def test_cd(self):
        # Тестирование команды cd
        self.emulator.execute_command("cd /home/user")
        self.assertEqual(self.emulator.current_dir, "/home/user")
        result = self.emulator.execute_command("ls")
        self.assertIn("file4.txt", result)

    def test_history(self):
        # Тестирование команды history
        self.emulator.execute_command("ls")
        self.emulator.execute_command("cd /home/user")
        result = self.emulator.execute_command("history")
        self.assertIn("ls", result)
        self.assertIn("cd /home/user", result)

if __name__ == "__main__":
    unittest.main()
