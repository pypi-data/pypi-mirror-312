import os
import ast  # Do parsowania listy plików w formacie tekstowym

class HooksManager:
    def __init__(self, config_file=".env_protector"):
        self.config_file = config_file
        self.gitignore_path = ".gitignore"
        self.pre_commit_hook_path = ".git/hooks/pre-commit"
        self.post_merge_hook_path = ".git/hooks/post-merge"

    def get_config(self):
        """Odczytaj konfigurację z pliku .env_protector."""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Plik konfiguracyjny {self.config_file} nie istnieje.")
        
        config = {}
        with open(self.config_file, "r") as file:
            for line in file:
                key, value = line.strip().split("=", 1)
                if key == "FILES":
                    config[key] = ast.literal_eval(value)  # Parsuj jako listę
                else:
                    config[key] = value
        return config

    def add_to_gitignore(self, files):
        """Dodaj pliki do .gitignore."""
        if not os.path.exists(self.gitignore_path):
            with open(self.gitignore_path, "w") as f:
                for file in files:
                    f.write(f"{file}\n")
                print(f"Dodano {', '.join(files)} do .gitignore.")
        else:
            with open(self.gitignore_path, "r") as f:
                lines = f.readlines()

            with open(self.gitignore_path, "a") as f:
                for file in files:
                    if f"{file}\n" not in lines:
                        f.write(f"{file}\n")
                        print(f"Dodano {file} do .gitignore.")

    def create_git_hook(self, path, content):
        """Utwórz plik hooka Git."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as hook:
            hook.write(content)
        os.chmod(path, 0o755)
        print(f"Utworzono hook Git: {path}")

    def create_pre_commit_hook(self, files, password):
        """Tworzy hook pre-commit obsługujący wiele plików."""
        file_commands = "\n".join(
            f"""
if [ -f {file} ]; then
  echo "Szyfrowanie pliku {file}..."
  gpg --symmetric --cipher-algo AES256 --batch --yes --passphrase "{password}" {file}
  git add {file}.gpg
fi
            """
            for file in files
        )

        content = f"""#!/bin/bash
{file_commands}
"""
        self.create_git_hook(self.pre_commit_hook_path, content)

    def create_post_merge_hook(self, files, password):
        """Tworzy hook post-merge obsługujący wiele plików."""
        file_commands = "\n".join(
            f"""
if [ -f {file}.gpg ]; then
  echo "Rozszyfrowywanie pliku {file}.gpg..."
  gpg --batch --yes --passphrase "{password}" -o {file} -d {file}.gpg
fi
            """
            for file in files
        )

        content = f"""#!/bin/bash
{file_commands}
"""
        self.create_git_hook(self.post_merge_hook_path, content)

    def setup_hooks(self):
        """Główna funkcja do konfiguracji hooków."""
        config = self.get_config()
        password = config.get("GPG_PASSWORD")
        files = config.get("FILES", [])

        if not password or not files:
            raise ValueError("Plik .env_protector musi zawierać klucz GPG_PASSWORD i listę FILES.")

        self.add_to_gitignore(files + [f"{file}.gpg" for file in files])
        self.create_pre_commit_hook(files, password)
        self.create_post_merge_hook(files, password)
        print("Konfiguracja zakończona!")
