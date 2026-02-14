# Biblioteka 2.0

Aplikacja do zarzadzania ksiazkami.

## Funkcjonalnosci aplikacji:
1) Wyswietlanie listy ksiazek
2) Dodawanie nowej ksiazki
3) Edycja ksiazki
4) Przechowywanie książek i autorów (relacja wiele-do-wielu)
5) Informacja, czy ksiazka jest na polce, czy wypozyczona
6) Dodawanie wypozyczen i oznaczanie zwrotow ksiazek


## Uruchamianie aplikacji:
1) Skolonuj repozytorium
2) Zainstaluj wymagane biblioteki ("pip install -r requirements.txt")
3) Zainicjalizuj migracje i utwórz bazę (flask db init, flask db migrate -m "Initial migration", flask db upgrade)
3) Uruchom aplikacje ("flask run") -> aplikacja dostepna pod adresem "http://127.0.0.1:5000/books/"