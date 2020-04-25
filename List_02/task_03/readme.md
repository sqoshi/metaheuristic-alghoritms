## Simulated Annealing for finding exit in labyrinth
Generalnie udało mi się zaimplementować na 4 różne sąsiedztwa,
 z czego 2 były chyba zbyt losowe(bardzo wolne), dlatego ich nie publikuję.
Po wpisaniu make będziemy korzystać z tego opartego na preffixach.( w mainie można przestawić na transpozycje)

Algorytm został zaimplementowany na dwa sposoby wyboru sąsiedztwa pierwszy na zasadzie transpozycji, 
a drugi  na podstawie usuwania losowego suffixu. Chciałbym od razu podkreślić, że wydaje mi się, że ten pierwszy
bazujący na transpozycjach może nie być do końca SA, bo w teorii nie mogę znaleźć przez transpozycję sąsiada o długości większej
czyli o gorszej jakości, chyba że rozwiązanie o tej samej długości można uznać za gorsze( a tak chyba można założyć?).
Dlatego własnie pushuje na dwa sposoby.

#####Algorytm bazujący na transpozycjach:
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

- Funkcja Kosztu: Długość ścieżki.
- Sąsiedztwo: Transpozycje danej ścieżki. np LLU , neigh = LUL itd.

#####Algorytm bazujący na usuwaniu suffixów:
Różni się w zasadzie tylko losowaniem sąsiada, reszta jak wyżej.

5. Losujemy sąsiada.
    1. Losujemy losowy index. Ten do którego prefix ma zostać zachowany.
    2. Do prefixu dołączamy, losowy path.
    3. Jeśli przez dany path napotkamy ściąnę, losujemy kolejnego sąsiada.(powrót do 5.1)

- Funkcja Kosztu: Długość ścieżki.
- Sąsiedztwo: Ścieżki o wspólnym prefixie.

Została zaimplementowana również możliwość stworzenia wykresu, gdzie możemy zaoobserwować zaimplementowane wyżarzanie.
Wystarczy ustawic graph= na True w mainie.
```
c, s = simulated_annealing_prefixes(50, b, T0=1000, graph=False)
```
