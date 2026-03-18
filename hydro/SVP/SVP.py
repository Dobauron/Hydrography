import pandas as pd
import matplotlib.pyplot as plt

# 1. Wczytanie pliku - jeśli opisy są w pierwszym wierszu, używamy skiprows
df = pd.read_excel('SVP.xlsx', skiprows=1)

# 2. Upewnienie się, że dane to na pewno liczby (to usunie ewentualny tekst)
# Zakładając, że Twoje dane są teraz w kolumnach o indeksach 2 i 3
glebokosc = pd.to_numeric(df.iloc[:, 2], errors='coerce')
predkosc = pd.to_numeric(df.iloc[:, 3], errors='coerce')

# Usuwamy wiersze, które po konwersji stały się puste (NaN)
df_clean = pd.DataFrame({'V': predkosc, 'D': glebokosc}).dropna()

# 3. Wykres
plt.figure(figsize=(6, 9))
plt.plot(df_clean['V'], df_clean['D'], marker='o', color='royalblue', markersize=4)

plt.gca().invert_yaxis()  # Głębokość rośnie w dół
plt.title('Profil prędkości dźwięku (CTD)')
plt.xlabel('Prędkość [m/s]')
plt.ylabel('Głębokość [m]')
plt.grid(True, alpha=0.3)

plt.show()