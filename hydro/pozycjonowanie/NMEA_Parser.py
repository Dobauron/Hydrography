import math


class NMEAParser:
    """Klasa do parsowania i walidacji sentencji protokołu NMEA 0183."""

    def __init__(self):
        self.talker_id = ""
        self.msg_type = ""
        # Mapowanie nadawców dla lepszej czytelności
        self.talkers = {
            'GP': 'GPS (USA)',
            'GL': 'GLONASS (Rosja)',
            'GA': 'Galileo (UE)',
            'BD': 'Beidou (Chiny)',
            'GN': 'System Mieszany (GNSS)'
        }

    def validate_checksum(self, sentence: str) -> bool:
        """Oblicza i weryfikuje sumę kontrolną XOR."""
        if not sentence.startswith('$') or '*' not in sentence:
            return False

        try:
            star_index = sentence.find('*')
            # Dane do obliczeń znajdują się między '$' a '*'
            data_to_check = sentence[1:star_index]
            provided_checksum = sentence[star_index + 1: star_index + 3]

            calculated_checksum = 0  # zmienna inicjalna
            for char in data_to_check:  # iteracja po każdym znaku sentencji NMEA
                # Porównywanie bitowej sumy obecnego znaku iteracji z poprzednim
                calculated_checksum ^= ord(char)

                # Konwersja na format hexadecymalny i porównanie z ostatnimi dwoma znakami NMEA, także w HEXA
            print(f"DEBUG: Otrzymany HEX: {provided_checksum.upper()}")
            print(f"DEBUG: Wyliczony HEX: {calculated_checksum:02X}")

            return f"{calculated_checksum:02X}" == provided_checksum.upper()
        except Exception:
            return False

    def _convert_to_dms(self, value: str, direction: str) -> str:
        """Konwertuje format NMEA (DDMM.MMMM) na format DMS (Stopnie Minuty Sekundy)."""
        if not value or not direction:
            return "Brak danych"
        try:
            dot_index = value.find('.')
            degrees_part = value[:dot_index - 2]
            minutes_part = value[dot_index - 2:]
            degrees = int(degrees_part)
            full_minutes = float(minutes_part)
            minutes = int(full_minutes)
            seconds = (full_minutes - minutes) * 60
            return f"{degrees}° {minutes}' {seconds:.4f}\" {direction}"
        except:
            return "Błąd formatu"

    def _parse_time(self, raw_time: str) -> str:
        """Formatuje surowy czas NMEA na format HH:MM:SS."""
        if len(raw_time) >= 6:
            return f"{raw_time[:2]}:{raw_time[2:4]}:{raw_time[4:]}"
        return raw_time

    def process_sentence(self, sentence: str):
        """Główna metoda przetwarzająca wejściowy ciąg znaków."""
        sentence = sentence.strip()

        if not sentence.startswith('$'):
            print(f"Zdanie w czystej postaci: {sentence} ***")
            return

        if not self.validate_checksum(sentence):
            print(f"BŁĄD: Niepoprawna suma kontrolna dla: {sentence}")
            return

        # czyszczenie wiadomości od 2 znaku do *
        content = sentence[1:sentence.find('*')]
        parts = content.split(',')
        header = parts[0]
        self.talker_id = header[:2]  # np. GP dla GPS
        self.msg_type = header[2:]  # np. GGA

        print("\n" + "=" * 40)
        print(f"Nadawca: {self.talkers.get(self.talker_id, self.talker_id)}")
        print(f"Typ wiadomości: {self.msg_type}")
        print("-" * 20)

        # --- LOGIKA DLA RÓŻNYCH TYPÓW SEKWENCJI ---

        # 1. Obsługa typu: GGA (Pozycja, jakość, wysokość)
        if self.msg_type == "GGA" and len(parts) >= 11:
            quality = parts[6]
            quality_desc = "Brak fixu" if quality == "0" else "GPS Fix" if quality == "1" else "DGPS Fix"

            print(f"Czas (UTC):      {self._parse_time(parts[1])}")
            print(f"Szerokość (DMS): {self._convert_to_dms(parts[2], parts[3])}")
            print(f"Długość (DMS):   {self._convert_to_dms(parts[4], parts[5])}")
            print(f"Status sygnału:  {quality_desc}")
            print(f"Satelity:        {parts[7]}")
            print(f"Wysokość n.p.m.: {parts[9]} {parts[10]}")

        # 2. Obsługa typu: RMC (Zalecane minimum danych)
        elif self.msg_type == "RMC" and len(parts) >= 10:
            status = "Aktywny" if parts[2] == "A" else "Ostrzeżenie (V)"
            print(f"Status:          {status}")
            print(f"Czas (UTC):      {self._parse_time(parts[1])}")
            print(f"Szerokość (DMS): {self._convert_to_dms(parts[3], parts[4])}")
            print(f"Długość (DMS):   {self._convert_to_dms(parts[5], parts[6])}")
            print(f"Prędkość:        {parts[7]} węzłów")
            print(f"Data:            {parts[9][:2]}.{parts[9][2:4]}.20{parts[9][4:]}")

        # 3. Obsługa typu: VTG (Kurs i prędkość km/h)
        elif self.msg_type == "VTG" and len(parts) >= 8:
            print(f"Kurs (True):     {parts[1]}°")
            print(f"Prędkość:        {parts[7]} km/h")

        # 4. Obsługa typu: GSA (Dokładność DOP i aktywne satelity)
        elif self.msg_type == "GSA" and len(parts) >= 17:
            mode = "3D" if parts[2] == "3" else "2D"
            print(f"Tryb ustalania:  {mode}")
            print(f"PDOP (Ogólna):   {parts[15]}")
            print(f"HDOP (Poziom):   {parts[16]}")

        else:
            print(f"INFO: Otrzymano poprawną ramkę {self.msg_type}, ale brak instrukcji wyświetlania szczegółów.")

        print("=" * 40)


if __name__ == "__main__":
    parser = NMEAParser()
    print("--- KOMPLEKSOWY PARSER NMEA 0183 ---")

    while True:
        user_input = input("\nPodaj sentencję (lub 'q' aby wyjść): ")
        if user_input.lower() in ['q', 'exit', 'quit']:
            break
        parser.process_sentence(user_input)