## Simulated Annealing for finding exit in labyrinth
1. Wyznaczenie czasu zakończenia.
2. Ustalenie temperatury początkowej.
3. Znalezienie pozycji startowej.
4. Wyznaczenie rozwiązania inicjalnego.
    - Jak wyznaczone jest rowiązanie intuicyjne?
    1. Losujemy path długości 2*(m+n-1)
    2. Idziemy wzdłuż dopóki nie napotkamy ściany lub wyjścia.
    3. Jeśli napotkamy ścianę losujemy nowy path z miejsca, w którym ostatnio się zatrzymaliśmy.
    4. Powtarzamy dopóki nie znajdziemy wyjścia.
5. Losujemy sąsiada.
    1. Wyznaczamy sąsiada zamieniając miejscami 2 elementy z initial_path( Transpozycja)
    2. Usuwamy punkty stałe, tzn UD LR RL DU z pathu.
    3. Jeśli przez dany path napotkamy ściąnę, losujemy kolejnego sąsiada.(powrót do 5.1)
6. Jeśli uda nam się przejść acceptance_prob przechodzimy do sąsiada. Current = neighbour.
7. Zapisujemy wynik do bestów, jeśli jest lepszy od ostatniego besta.
8. Wracamy do 5.

Została zaimplementowana również możliwość stworzenia wykresu bestów od kolejnych kroków.

- Funkcja Kosztu: Długość ścieżki.
- Sąsiedztwo: Transpozycje danej ścieżki. np LLU , neigh = LUL itd.