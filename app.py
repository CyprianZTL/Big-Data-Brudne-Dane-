import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re

# "brudne dane"

np.random.seed(42)

n = 500
klienci = [
    "Anna Kowalska", "  Jan Nowak", "Anna Kowalska", "PIOTR WIŚNIEWSKI",
    "katarzyna lewandowska", "Tomasz Zieliński ", "Marta Wójcik",
    "anna kowalska ", "Krzysztof Kamiński", " Magdalena Dąbrowska"
]

produkty = [
    "Laptop", "Mysz", "Klawiatura", "Monitor", "laptop", "MYSZ",
    "Słuchawki", "Pendrive", "monitor", "Webcam"
]

kategorie = [
    "Elektronika", "elektronika", "ELEKTRONIKA",
    "Akcesoria", "akcesoria", "Akcesoria "
]

miasta = [
    "Warszawa", "Kraków", "warszawa", "Gdańsk",
    "WROCŁAW", "Poznań", "Łódź ", " Warszawa", "kraków"
]

start_date = datetime(2025, 1, 1)

daty_iso = [
    (start_date + timedelta(days=int(d))).strftime("%Y-%m-%d")
    for d in np.random.randint(0, 300, n // 2)
]

daty_pl = [
    (start_date + timedelta(days=int(d))).strftime("%d.%m.%Y")
    for d in np.random.randint(0, 300, n // 2)
]

daty = daty_iso + daty_pl
np.random.shuffle(daty)

df_generate = pd.DataFrame({
    "order_id": range(1001, 1001 + n),
    "klient": np.random.choice(klienci, n),
    "produkt": np.random.choice(produkty, n),
    "kategoria": np.random.choice(kategorie, n),
    "miasto": np.random.choice(miasta, n),
    "ilosc": np.random.choice(
        [1, 2, 3, 5, -1, 0],
        n,
        p=[0.5, 0.2, 0.15, 0.1, 0.025, 0.025]
    ),
    "cena_jednostkowa": np.random.choice(
        ["199.99", "299,99", "1 499.00", "89.50", "2999", "399.00 zł", None, "abc"],
        n
    ),
    "data_zamowienia": daty,
    "email": np.random.choice(
        [
            "anna@gmail.com",
            "JAN@WP.PL",
            "piotr.w@onet",
            "marta@gmail.com",
            "tomasz@interia.pl",
            None,
            "krzysztof.k@gmail.com",
            "brak"
        ],
        n
    )
})

# dodanie braków
for col in ["miasto", "kategoria", "data_zamowienia"]:
    df_generate.loc[
        df_generate.sample(frac=0.05, random_state=1).index,
        col
    ] = np.nan

# duplikaty
df_generate = pd.concat(
    [df_generate, df_generate.sample(20, random_state=2)],
    ignore_index=True
)

# zapis "brudnych danych"
df_generate.to_csv("zamowienia_messy.csv", index=False)
print(f"Wygenerowano plik 'zamowienia_messy.csv' — {len(df_generate)} wierszy")


#eksploracja

df = pd.read_csv("zamowienia_messy.csv")

print("\n" + "=" * 50)
print("EKSPLORACJA DANYCH")
print("=" * 50)

print("\nShape:")
print(df.shape)

print("\nInfo:")
print(df.info())

print("\nDescribe:")
print(df.describe(include="all"))

print("\nBraki danych:")
print(df.isnull().sum())

print("\nLiczba duplikatów:")
print(df.duplicated().sum())

print("\nUnikalne wartości w kolumnie 'kategoria':")
print(df["kategoria"].value_counts(dropna=False))

print("\nUnikalne wartości w kolumnie 'miasto':")
print(df["miasto"].value_counts(dropna=False))

print("\nProblemy z jakością danych:")
print("1. Duplikaty wierszy")
print("2. Brakujące wartości")
print("3. Niespójne wielkości liter")
print("4. Dodatkowe spacje")
print("5. Różne formaty dat")
print("6. Niepoprawne ceny (np. 'abc', '399.00 zł')")
print("7. Niepoprawne ilości (0 lub wartości ujemne)")
print("8. Niepoprawne adresy email")


#czyszczenie

# usuniecie duplikatów
df = df.drop_duplicates()

# standaryzacja
df["klient"] = df["klient"].str.strip().str.title()
df["produkt"] = df["produkt"].str.strip().str.title()
df["kategoria"] = df["kategoria"].str.strip().str.lower()
df["miasto"] = df["miasto"].str.strip().str.title()

# konwersja dat
df["data_zamowienia"] = pd.to_datetime(
    df["data_zamowienia"],
    format="mixed",
    errors="coerce"
)

# czyszcze z konwersja ceny
df["cena_jednostkowa"] = (
    df["cena_jednostkowa"]
    .astype(str)
    .str.replace("zł", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

df["cena_jednostkowa"] = pd.to_numeric(
    df["cena_jednostkowa"],
    errors="coerce"
)

# usunienie brakow
df = df.dropna(subset=["cena_jednostkowa", "data_zamowienia"])

# uzupelnienie
df["miasto"] = df["miasto"].fillna("Unknown")
df["kategoria"] = df["kategoria"].fillna("unknown")
df["email"] = df["email"].fillna("brak_emaila")

# kasowanie bledych ilosci
df = df[df["ilosc"] > 0]


#transformacja

# wartosc zamowienia
df["wartosc_zamowienia"] = df["ilosc"] * df["cena_jednostkowa"]

df["rok"] = df["data_zamowienia"].dt.year
df["miesiac"] = df["data_zamowienia"].dt.month
df["nazwa_dnia"] = df["data_zamowienia"].dt.day_name()

# walidacja
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
df["email_poprawny"] = df["email"].str.match(
    email_pattern,
    na=False
)


#analiza

print("\n" + "=" * 50)
print("ANALIZA DANYCH")
print("=" * 50)

# laczna wartosc - miesiac
monthly_sales = (
    df.groupby("miesiac")["wartosc_zamowienia"]
    .sum()
    .sort_index()
)

print("\nŁączna wartość zamówień w każdym miesiącu:")
print(monthly_sales)

# topka klientow
top_clients = (
    df.groupby("klient")["wartosc_zamowienia"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTop 5 klientów:")
print(top_clients)

# srednia wartosc zamowienia
avg_category = (
    df.groupby("kategoria")["wartosc_zamowienia"]
    .mean()
    .sort_values(ascending=False)
)

print("\nŚrednia wartość zamówienia w każdej kategorii:")
print(avg_category)


#wizualizacja danych

plt.figure(figsize=(10, 5))
plt.bar(monthly_sales.index.astype(str), monthly_sales.values)
plt.title("Łączna wartość zamówień w każdym miesiącu")
plt.xlabel("Miesiąc")
plt.ylabel("Wartość zamówień")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


#zapis do csv

df.to_csv("zamowienia_clean.csv", index=False)

print("\nOczyszczone dane zapisano do pliku 'zamowienia_clean.csv'")
print(f"Liczba rekordów po czyszczeniu: {len(df)}")
print(f"Liczba kolumn: {df.shape[1]}")