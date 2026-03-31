import pandas as pd
import matplotlib.pyplot as plt

# Ścieżka do pliku z danymi
file_path = 'LAB2 - Zad2 - dane svp_Zatoka Gdańska.asvp'

# Wczytanie danych
# sep='\s+' obsługuje spacje jako separator
# skiprows=2 pomija dwie pierwsze linie nagłówka
# header=None brak nagłówka w danych
# names nadaje nazwy kolumnom
df = pd.read_csv(file_path, sep='\s+', skiprows=2, header=None, names=['Glebokosc', 'Predkosc'])

# Oczyszczanie danych
# Usuwamy ewentualne wiersze z brakującymi wartościami (np. niekompletne linie na końcu)
df = df.dropna()
# Usuwamy wiersze z wartościami -1 (oznaczające błąd/koniec)
df = df[(df['Glebokosc'] != -1) & (df['Predkosc'] != -1)]

# Konwersja na liczby
df['Glebokosc'] = pd.to_numeric(df['Glebokosc'])
df['Predkosc'] = pd.to_numeric(df['Predkosc'])

# Rysowanie wykresu
plt.figure(figsize=(8, 10))
# Wykres liniowo-punktowy: marker='.' dodaje punkty, linestyle='-' rysuje linię
plt.plot(df['Predkosc'], df['Glebokosc'], marker='.', linestyle='-', linewidth=0.8, markersize=3, label='Profil prędkości dźwięku')

# Odwrócenie osi Y (głębokość rośnie w dół)
plt.gca().invert_yaxis()

plt.title('Zależność prędkości dźwięku w wodzie od głębokości\n(Zatoka Gdańska)')
plt.xlabel('Prędkość dźwięku [m/s]')
plt.ylabel('Głębokość [m]')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.show()
