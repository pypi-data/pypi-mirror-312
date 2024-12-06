# Env Protector

`env-protector` to Pythonowa paczka, która ułatwia zarządzanie plikami `.env` w projektach Git. Automatyzuje szyfrowanie i odszyfrowywanie plików `.env` przy użyciu hooków Git, zapewniając bezpieczeństwo poufnych danych.

---

## Funkcje

- **Automatyczne szyfrowanie plików `.env`** przy każdym `git commit`.
- **Automatyczne odszyfrowywanie plików `.env`** po `git pull` lub `git merge`.
- Obsługa plików `.env.gpg` przy użyciu GPG (`GNU Privacy Guard`).
- Dodawanie plików `.env` do `.gitignore`, aby unikać przypadkowego dodania ich do repozytorium.

---

## Instalacja

1. Zainstaluj paczkę za pomocą pip:
   ```
   bash
   pip install env-protector
   ```

2. Upewnij się, że masz zainstalowane GPG:
   - **Linux/macOS**: GPG jest zazwyczaj preinstalowany. Jeśli nie, zainstaluj go:
     ```
     bash
     sudo apt install gnupg  # Ubuntu
     brew install gnupg     # macOS
     ```
   - **Windows**: Pobierz [GPG for Windows](https://gnupg.org/download/).

---

## Użycie

1. **Importuj paczkę:**
   ```
   python
   from env_protector import HooksManager
   ```

2. **Skonfiguruj hooki Git:**
   ```
   python
   manager = HooksManager()
   manager.setup_hooks()
   ```

   Funkcja `setup_hooks`:
   - Dodaje `.env` do `.gitignore`.
   - Tworzy hooki `pre-commit` i `post-merge`.

3. **Ustaw zmienną środowiskową dla hasła GPG:**
   ```
   bash
   export GPG_PASSWORD="twoje_haslo"
   ```

4. **Dodaj plik `.env` do repozytorium:**
   - Utwórz plik `.env` z konfiguracjami:
     ```
     text
     API_KEY=123456
     SECRET_KEY=my_secret_key
     ```
   - Dodaj plik `.env` do repozytorium:
     ```
     bash
     git add .env
     git commit -m "Dodano plik .env"
     ```

   Plik `.env` zostanie automatycznie zaszyfrowany jako `.env.gpg`.

5. **Odszyfrowanie pliku `.env`:**
   Po wykonaniu `git pull` lub `git merge` plik `.env.gpg` zostanie automatycznie odszyfrowany.

---

## Przykład

Poniżej pełny kod konfiguracji:

```
python
from env_protector import HooksManager

# Utwórz instancję klasy HooksManager
manager = HooksManager()

# Skonfiguruj hooki Git
manager.setup_hooks()
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
