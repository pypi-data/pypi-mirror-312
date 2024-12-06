# Env Protector

`env-protector` to Pythonowa paczka, która ułatwia zarządzanie plikami konfiguracyjnymi, takimi jak `.env`, w projektach Git. Automatyzuje szyfrowanie i odszyfrowywanie wielu plików przy użyciu hooków Git, zapewniając bezpieczeństwo poufnych danych.

---

## Motywacja

W projektach programistycznych pliki konfiguracyjne, takie jak `.env`, `config.json` czy `secrets.txt`, często zawierają poufne informacje. Ich przypadkowe dodanie do repozytorium może prowadzić do wycieków danych. 

**Env Protector** został stworzony, aby:
- Ułatwić zarządzanie wieloma plikami konfiguracyjnymi w sposób bezpieczny.
- Zapobiec przypadkowemu udostępnieniu poufnych informacji.
- Uprościć proces szyfrowania i odszyfrowywania, eliminując potrzebę ręcznej obsługi.
- Zautomatyzować procesy przy użyciu hooków Git.

---

## Funkcje

- **Automatyczne szyfrowanie wielu plików** przy każdym `git commit`.
- **Automatyczne odszyfrowywanie wielu plików** po `git pull` lub `git merge`.
- Obsługa plików `.gpg` przy użyciu GPG (`GNU Privacy Guard`).
- Odczyt hasła GPG i listy plików do szyfrowania z pliku `.env_protector`.
- Automatyczne dodawanie plików konfiguracyjnych do `.gitignore`.
- **Komenda systemowa `env-protector`** do łatwego konfigurowania hooków.

---

## Instalacja

1. Zainstaluj paczkę za pomocą pip:
   ```bash
   pip install env-protector
   ```

2. Upewnij się, że masz zainstalowane GPG:
   - **Linux/macOS**: GPG jest zazwyczaj preinstalowany. Jeśli nie, zainstaluj go:
     ```bash
     sudo apt install gnupg  # Ubuntu
     brew install gnupg     # macOS
     ```
   - **Windows**: Pobierz [GPG for Windows](https://gnupg.org/download/).

---

## Konfiguracja

1. **Utwórz plik `.env_protector`:**

   Plik `.env_protector` powinien zawierać hasło GPG oraz listę plików do szyfrowania:
   ```text
   GPG_PASSWORD=YOURPASS
   FILES=[.env, config.json, secrets.txt]
   ```

2. **Skonfiguruj hooki Git za pomocą komendy `env-protector`:**

   W terminalu, w katalogu swojego projektu, wykonaj:
   ```bash
   env-protector
   ```

   Komenda ta automatycznie:
   - Dodaje wymienione pliki oraz ich zaszyfrowane wersje (`.gpg`) do `.gitignore`.
   - Tworzy hooki `pre-commit` i `post-merge`.

---

## Użycie

1. **Dodaj pliki do repozytorium:**
   - Utwórz pliki konfiguracyjne, które chcesz zabezpieczyć:
     ```bash
     echo "API_KEY=123456" > .env
     echo '{"key": "value"}' > config.json
     echo "SECRET=abcd" > secrets.txt
     ```
   - Dodaj pliki do repozytorium:
     ```bash
     git add .env config.json secrets.txt
     git commit -m "Szyfrowanie plików"
     ```

   Pliki zostaną automatycznie zaszyfrowane jako `.gpg`.

2. **Odszyfrowanie plików:**
   Po wykonaniu `git pull` lub `git merge` zaszyfrowane pliki `.gpg` zostaną automatycznie odszyfrowane do ich oryginalnych wersji.

---

## Przykład działania

1. **Konfiguracja hooków Git:**
   ```bash
   env-protector
   ```

   Wyjście w terminalu:
   ```text
   Konfigurowanie hooków Git...
   Dodano .env, config.json, secrets.txt do .gitignore.
   Dodano .env.gpg, config.json.gpg, secrets.txt.gpg do .gitignore.
   Utworzono hook Git: .git/hooks/pre-commit
   Utworzono hook Git: .git/hooks/post-merge
   Konfiguracja zakończona!
   ```

2. **Dodawanie i szyfrowanie plików:**
   ```bash
   echo "API_KEY=example_key" > .env
   git add .env
   git commit -m "Szyfrowanie pliku .env"
   ```

3. **Odszyfrowanie plików:**
   Po wykonaniu `git pull`:
   ```text
   Rozszyfrowywanie pliku .env.gpg...
   Rozszyfrowywanie pliku config.json.gpg...
   Rozszyfrowywanie pliku secrets.txt.gpg...
   ```
---

## Wymagania

- Python >= 3.6
- Zainstalowany GPG

---

## Problemy i pytania

Jeśli napotkasz jakiekolwiek problemy lub masz pytania, utwórz zgłoszenie w repozytorium GitHub.

---

## Licencja

Projekt jest dostępny na licencji [MIT](LICENSE).