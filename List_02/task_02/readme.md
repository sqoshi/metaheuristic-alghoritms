##Simulated Annealing For Limited Zoom
1. Określamy czas zakończenia.
2. Nakładamy abstrakcyjną siatkę, tworząc po tym rozwiązanie inicjalne. 
- Dzielimy taką siatką macierz na bloki 
k+1 x k+1 elementowe, lub większe.
 - Czemu nie kxk? Bo wtedy mamy większą swobodę ruchu, lepszy wybór sąsiada, bardziej swobodny.
3. Inicjujemy nasze najlepsze wyniki jako w listach.
4. Dopóki temperatura jest większa od zera i nie skończył się czas.
5. Wylosuj sąsiada. W jaki sposób jest losowany?
    1. Zmieniamy kolor losowego bloku na losowy.
    2. Losowo wyznaczmy blok, który będziemy poszerzać kosztem innego sąsiedniego do niego(Zachowany warunek min blok kxk)
    3. Tworzymy nowy board na podstawie nowych zmienonych współrzędnych(zawsze zwiększamy jeden o 1 kolumnę/wiersz inny zmniejszając).
    4. Sprawdzamy Koszt.
    5. Niestety nieraz możemy rozszeerzyć blok składający się z wartości 32 kosztem bloku o tej samej wartości lub po prostu żaden z sąsiadów bloku nie ma odpowiednich wymiarów lub nie jest w odpowiednich kolumnach
    , wtedy globalnie nic się nie zmieniło i koszt jest zerem więc musimy wybrać  inne rozszerzanie ( wracamy do i.)
6. Sprawdzamy acceptance_probability jeśli uda się przejść warunek > random.uniform(0,1)
to updateujemy wartości " przechodzimy do wygenerowanego sąsiada "
7. Jeśli wynik jest lepszy od ostatniego najlepszego zapisujemy.


i wtedy będzie wykres kolejnych wartości przez, które rzeczywiście przeszliśmy.    

- Funkcja Kosztu: compute_distance() (zadana w poleceniu zadania)

- Sąsiedztwo: Zmiana wartości( koloru) losowego bloku i/lub rozszerzenia losowego bloku kosztem innego bloku lub/i swap wartości losowych bloków.
 Tzn jeśli mamy np maksymalnie prawy górny
 blok wiekości (założmy Wysokość x Szerokość) k+1 x k+1 i jego  sąsiadów lewego L i dolnego D, to sprawdzamy, czy dane bloki
 mają odpowiednie wymiary, tj czy po ucięciu kolumny czy też wiersza będą nadal większe niz k x k. Losujemy np Lewego Sprawdzamy,
  czy lewy leży na tej samej wysokości, i potem czy po zjedzeniu kolumny jego wymiar szerokość będzie większa niż k. 


Została również zaimplementowana możliwość rysowania wykresu funkcji kosztu, 
naturalnie jest zaimplementowana dla niepowtarzających się kosztów ( w celu zachowania przyjemnego wyglądu SA).