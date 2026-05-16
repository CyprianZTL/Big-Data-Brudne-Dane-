# 🛒 Czyszczenie i analiza zamówień e-commerce (Big Data)

## 📜 Opis projektu

Projekt przedstawia kompletny proces przygotowania danych do analizy:

**Generowanie danych → Eksploracja → Czyszczenie → Transformacje → Analiza → Wizualizacja → Zapis**

Program tworzy sztuczny zbiór brudnych danych o zamówieniach e-commerce, wykrywa problemy jakości danych, oczyszcza je, a następnie odpowiada na kluczowe pytania biznesowe.

---

## 🏗️ Struktura projektu

🗂️ `app.py` – główny skrypt zawierający cały pipeline danych
🗂️ `zamowienia_messy.csv` – wygenerowany plik z brudnymi danymi
🗂️ `zamowienia_clean.csv` – oczyszczony plik gotowy do analizy

---

## ⚙️ Etapy przetwarzania danych

### 🧪 1. Generowanie danych

Tworzenie realistycznego zbioru zawierającego:

* duplikaty,
* brakujące wartości,
* błędne formaty cen,
* różne formaty dat,
* niepoprawne adresy e-mail,
* błędne ilości produktów.

### 🔍 2. Eksploracja danych

Analiza struktury danych przy użyciu:

* `shape`
* `info()`
* `describe()`
* `isnull().sum()`
* `value_counts()`

### 🧹 3. Czyszczenie danych

* usunięcie duplikatów,
* standaryzacja tekstu,
* konwersja dat i cen,
* obsługa braków,
* usunięcie błędnych ilości.

### 🔄 4. Transformacje

Dodanie nowych kolumn:

* `wartosc_zamowienia`
* `rok`
* `miesiac`
* `nazwa_dnia`
* `email_poprawny`

### 📊 5. Analiza biznesowa

* łączna wartość zamówień w każdym miesiącu,
* Top 5 klientów,
* średnia wartość zamówienia w każdej kategorii.

### 📈 6. Wizualizacja

Wykres słupkowy przedstawiający wartość zamówień w kolejnych miesiącach.

### 💾 7. Zapis wyników

Eksport oczyszczonych danych do pliku `zamowienia_clean.csv`.

---

## 🛠️ Wykorzystane technologie

🐍 Python
📦 pandas – analiza i transformacja danych
🔢 numpy – generowanie danych
📊 matplotlib – wizualizacja danych
🧮 re – walidacja adresów e-mail

---

## 🧩 Wykryte problemy jakości danych

* duplikaty rekordów,
* brakujące wartości,
* niespójne wielkości liter,
* zbędne spacje,
* dwa formaty dat,
* niepoprawne ceny (`abc`, `399.00 zł`),
* błędne ilości (`0`, `-1`),
* niepoprawne adresy e-mail.

---

## 📈 Przykładowe analizy

* sprzedaż miesięczna,
* najlepsi klienci,
* porównanie kategorii produktowych,
* walidacja poprawności e-maili.

---

## 🚀 Jak uruchomić projekt

Zainstaluj wymagane biblioteki:

```bash
pip install pandas numpy matplotlib
```

Uruchom program:

```bash
python app.py
```

---

## 📂 Pliki wynikowe

Po uruchomieniu programu zostaną utworzone:

* `zamowienia_messy.csv`
* `zamowienia_clean.csv`

---

## 🎯 Cele projektu

Projekt realizuje pełny proces Data Cleaning i Data Preparation zgodnie z wymaganiami przedmiotu **Zarządzanie Big Data**.

---

## 👤 Autor

Cyprian
