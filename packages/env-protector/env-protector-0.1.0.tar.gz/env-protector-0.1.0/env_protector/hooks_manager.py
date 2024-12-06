import os
import subprocess

class HooksManager:
    def __init__(self, env_file=".env", encrypted_file=".env.gpg", config_file=".env_protector"):
        self.env_file = env_file
        self.encrypted_file = encrypted_file
        self.config_file = config_file
        self.gitignore_path = ".gitignore"
        self.pre_commit_hook_path = ".git/hooks/pre-commit"
        self.post_merge_hook_path = ".git/hooks/post-merge"

    def get_gpg_password(self):
        """Odczytaj hasło GPG z pliku konfiguracyjnego."""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Plik konfiguracyjny {self.config_file} nie istnieje.")
        
        with open(self.config_file, "r") as file:
            for line in file:
                if line.startswith("GPG_PASSWORD="):
                    return line.strip().split("=", 1)[1]
        
        raise ValueError(f"Nie znaleziono klucza GPG_PASSWORD w pliku {self.config_file}.")

    def add_to_gitignore(self):
        """Dodaje pliki .env i .env_protector do .gitignore."""
        ignored_files = [self.env_file, self.config_file]

        if not os.path.exists(self.gitignore_path):
            with open(self.gitignore_path, "w") as f:
                for file in ignored_files:
                    f.write(f"{file}\n")
                print(f"Dodano {', '.join(ignored_files)} do .gitignore.")
        else:
            with open(self.gitignore_path, "r") as f:
                lines = f.readlines()

            with open(self.gitignore_path, "a") as f:
                for file in ignored_files:
                    if f"{file}\n" not in lines:
                        f.write(f"{file}\n")
                        print(f"Dodano {file} do .gitignore.")

    def create_git_hook(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as hook:
            hook.write(content)
        os.chmod(path, 0o755)
        print(f"Utworzono hook Git: {path}")

    def create_pre_commit_hook(self):
        content = f"""#!/bin/bash
if [ -f {self.env_file} ]; then
  echo "Szyfrowanie pliku {self.env_file}..."
  GPG_PASSWORD=$(grep GPG_PASSWORD {self.config_file} | cut -d '=' -f2)
  gpg --symmetric --cipher-algo AES256 --batch --yes --passphrase "$GPG_PASSWORD" {self.env_file}
  git add {self.encrypted_file}
  echo "Plik {self.env_file} został zaszyfrowany jako {self.encrypted_file}"
fi
"""
        self.create_git_hook(self.pre_commit_hook_path, content)

    def create_post_merge_hook(self):
        content = f"""#!/bin/bash
if [ -f {self.encrypted_file} ]; then
  echo "Rozszyfrowywanie pliku {self.encrypted_file}..."
  GPG_PASSWORD=$(grep GPG_PASSWORD {self.config_file} | cut -d '=' -f2)
  gpg --batch --yes --passphrase "$GPG_PASSWORD" -o {self.env_file} -d {self.encrypted_file}
  echo "Plik {self.encrypted_file} został rozszyfrowany do {self.env_file}"
fi
"""
        self.create_git_hook(self.post_merge_hook_path, content)

    def setup_hooks(self):
        self.add_to_gitignore()
        self.create_pre_commit_hook()
        self.create_post_merge_hook()
        print(f"Konfiguracja zakończona. Upewnij się, że plik {self.config_file} zawiera hasło GPG_PASSWORD.")


def main():
    """Główna funkcja wywoływana przez komendę systemową"""
    print("Konfigurowanie hooków Git...")
    manager = HooksManager()
    manager.setup_hooks()
    print("Konfiguracja zakończona!")