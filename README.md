# Metaheuristic alghoritms


1. Hill Climbing With Random Restarts (Shotgun hill climbing)
2. Local Search (own modification)
2. Tabu Seach
	- tabu list
3. Simulated Annealing
	- temperature
4. Particle Swarm
	- velocity vector
	- does not select parents
5. Genetic Alghorithm
	- tournament selection
	- quality selection(random)
	- two-point crossover

## List 01
### Task 01 - Shotgun hill climbing  ( griewank, happycat functions)

#### Hill Climbing With Random Restarts
1. Losowane jest inicjalne rozwiązanie z hiperkostki n^4 na przedziale (-5,5)
2. Dopóki mamy czas global_time:
    1. Losujemy przedział czasowy ( mniejszy niż odgórne t) local_time:
    2. Dopóki mamy czas local_time:
        1. Generujemy sąsiada zaburzując wektor x o zmienną losową z przedziału (-1,1)^4
        2. Badamy jakość sąsiada jęsli jest lepsza to przechodzimy do niego, jeśli nie zostajemy przy S.
    3. Porównujemy besta z lokalnym wynikiem i losujemy zupełnie nowy start ( random restart)

#### Local Search
1. Losowane jest inicjalne rozwiązanie z hiperkostki n^4 na przedziale (-5,5)
2. Dopóki mamy czas t:
    1. generujemy n sąsiadów bieżącego rozwiązania zaburzując wektor x o zmienną losową z przedziału (-1,1)^4 n razy
    2. wybieramy minimalnego pod względem quality function sąsiada i do niego przechodzimy.
    3. jeśli utknęliśmy w lokalnym optimum- random restart



   
### Task 02 - Finding minimal distance path between cities(TSP)
    
#### Standard
1. Znajdź rozwiązanie inicjalne - algorytm zachłanny :
    - wchodzi w kolejne miasta biorąc minimalne dystanse
2. Dopóki jest czas:
    1. sprawdź długość Tabu, jeśli jest zbyt duże pozbądź się najstarszych ścieżek.
    2. Wybierz sąsiada R - transpozycja dowolnych dwóch miast
    3. Tweak n razy:
        - wybierz sąsiada W rozwiązania R - transpozycja.
    4. Wybierz najlepszego z n x W u R
    5. Dołącz najlepszego z nich do Tabu List.
    6. Porównaj besty.
    7. Jeśli dopusczone są resety to co m- iterację wróć do najlepsego miasta.
    8. Jeśli dopusczone są teleportację co k- iterację zacznij poszukiwania od nowo wylosowanego miasta.

#### My modification TSP Tabu Search
1. Znajdź rozwiązanie inicjalne - algorytm zachłanny :
    - wchodzi w kolejne miasta biorąc minimalne dystanse
2. Dopóki jest czas:
    1. Stwórz wszystkie kombinacje ścieżek bazujące tylko na transpozycjach.
    3. Wybierz z nich najlepszego
    4. Dodaj najlepszego do tabu
    4. Porównaj z bestem.

  
### Task 03 - Finding exit in labyrinth ( no walls inside)

#### Standard
1. Generujemy rozwiązanie początkowe:
    - agent dochodzi do górnej ściany, a później podąża za ścianą dopóki nie napotka wyjścia.
2. Dopóki jest czas:
    1. Sprawdzaj rozmiar tabu list i wyrzucaj najstrasze ścieżki
    2. Wybierz losową transpozycję R rozwiązania S i usuwamy punkty stałe
    3. Tweak n razy:
        1. Wybierz najlepszego z wszystkich tweaków W( transpozycje na R) i usuwamy punkty stałe
        2. jeśli rozwiązanie nowe W nie jest w tabu i jest lepsze od R to przechodzimy do niego
    4. jeśli rozwiązanie nie jest w tabu to dołączamy go 
    5. sprawdzamy poprawność rozwiązania.

#### My modification tabu search maze exiting ( no walls)
1. Generujemy rozwiązanie początkowe:
    - agent dochodzi do górnej ściany, a później podąża za ścianą dopóki nie napotka wyjścia.
2. Dopóki jest czas:
    1. Losujemy wszystkie transpzycje scieżki i usuwamy punkty stałe
    2. prawdzamy poprawność ścieżki i wybieramy minimalną z nich
    3. Porównujemy z bestem
    4. Dołączamy do Tabu

    
## List 02
### Task 03 - Simulated Annealing For Salomon's Function
0. Temperatura początkowa zostaje zainicjowana na wysoką wartość np.: 100, 1000, 10000
1. Program działa w pętli dopóki nie przekroczy limitu czasowego, lub T osiąggnie wartość 0.
2. Wyliczamy wartość funkcji Salomon'a ( quality function) na podstawie rozwiązania początkowego i zapisujemy do "historii best'ów".
3. Generujemy sąsiada neighbour aktualnego rozwiązania x.( możemy zaburzać względem wiekości wektora
np x_i = x_i*(1+random.uniform(-e,e)) lub statycznie x_i = x_i + random.uniform(k,k))
( w moim przypadku robię to naprzemiennie, wtedy wiem, że ze przy skalowaniu nie utknę w 0^4)
4. Wyznaczamy wartości funkcji Salomon'a dla neighbour oraz x, wyznaczamy deltę( róznicę między tymi wartościami.)
5. Losujemy liczbę zmiennoprzecinkową z przedziału (0,1)
6. Obliczamy probability z wzoru podanego na wykładzie p=e^{\frac{-delta}{T}}
7. Jeśli wylosowana wartość(0,1) jest mniejsza od wyliczonej probability to przechodzimy do sąsiada tzn, ustalamy x = neighbour.
8. Zmniejszamy T( temperaturę ) w określony sposób ( jeden z wykładów np T_{i+1}= T_i/log(i))
9. Sprawdzamy czy aktualna wartość jest lepsza od najlepszej dotychczas znalezionej best, jeśli tak dodajemy do historii.
10. Wracamy do 3.


- Funkcja Kosztu: Funkcja Salamon'a.

- Sąsiedztwo: Naprzemienne zaburzenia wektora V^4 względem jego samego(losowe odchylenia) lub skalowanie.


W programie została zaimplementowana również możliwość reset'ów. 
Tzn jeśli wpadniemy w lokalne minimum lub wpadniemy po prostu na "złą trasę"
to restartujemy, tzn cofnięcia się do naszego dotychczas najlepszego rozwiązania i wylosowanie nowego sąsiada, 
wtedy być może pójdźiemy w innym kierunku
niż ostatnio i uciekniemy w taki sposób z minimum lokalnego.
Ewentualnie można też zrobić losowy spawn na określonym przedziale np(-10,10)(chyba), ale wydaje się to mniej ciekawe.
Została też zaimplementowana możliwość rysowania wykresów funkcji kosztu
, czy nawet zmian samych współrzędnych wektora.( graphs = True w mainie aby wyświetlić)

### Task 02 - Simulated Annealing For Limited Zoom
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

### Task 03 - Simulated Annealing for finding exit in labyrinth
Generalnie udało mi się zaimplementować na 4 różne sąsiedztwa,
 z czego 2 były chyba zbyt losowe(bardzo wolne), dlatego ich nie publikuję.
Po wpisaniu make będziemy korzystać z tego opartego na preffixach.( w mainie można przestawić na transpozycje)

Algorytm został zaimplementowany na dwa sposoby wyboru sąsiedztwa pierwszy na zasadzie transpozycji, 
a drugi  na podstawie usuwania losowego suffixu. Chciałbym od razu podkreślić, że wydaje mi się, że ten pierwszy
bazujący na transpozycjach może nie być do końca SA, bo w teorii nie mogę znaleźć przez transpozycję sąsiada o długości większej
czyli o gorszej jakości, chyba że rozwiązanie o tej samej długości można uznać za gorsze( a tak chyba można założyć?).
Dlatego własnie pushuje na dwa sposoby.

##### Algorytm bazujący na na usuwaniu suffixów:
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
    1. Losujemy losowy index. Ten do którego prefix ma zostać zachowany.
    2. Do prefixu dołączamy, losowy path.
    3. Jeśli przez dany path napotkamy ściąnę, losujemy kolejnego sąsiada.(powrót do 5.1)
6. Jeśli uda nam się przejść acceptance_prob przechodzimy do sąsiada. Current = neighbour.
7. Zapisujemy wynik do bestów, jeśli je``st lepszy od ostatniego besta.
8. Wracamy do 5.

- Funkcja Kosztu: Długość ścieżki.
- Sąsiedztwo: Transpozycje danej ścieżki. np LLU , neigh = LUL itd.

##### Algorytm bazujący transpozycjach:

Różni się w zasadzie tylko losowaniem sąsiada, reszta jak wyżej.
5. Losujemy sąsiada.
    1. Wyznaczamy sąsiada zamieniając miejscami 2 elementy z initial_path( Transpozycja)
    2. Usuwamy punkty stałe, tzn UD LR RL DU z pathu.
    3. Jeśli przez dany path napotkamy ściąnę, losujemy kolejnego sąsiada.(powrót do 5.1)


- Funkcja Kosztu: Długość ścieżki.
- Sąsiedztwo: Ścieżki o wspólnym prefixie.

Została zaimplementowana również możliwość stworzenia wykresu, gdzie możemy zaoobserwować zaimplementowane wyżarzanie.
Wystarczy ustawic graph= na True w mainie.

## List 03

### Task 01 - Particle Swarm for X.S Yang function.
    :param x0: - start vector
    :param t: time limitation
    :param func: quality function
    :param swarm_size: quantity of swarms
    :param alpha: velocity retained
    :param beta: personal best retained
    :param gamma: best of informants' retained
    :param delta: global best retained
    :param epsilon: size of jumps
    :param plot: graphs
1. Iniciujemy populacje losowymi rozwiązaniami, i tworzymy losowe wektory prędkości dla każdego z nich.
2. Rejestrujemy listę personalnych bestów.
3. Wybieramy globalnego besta.
4. Wybieramy besta z bieżących rojów ( informowanych )
5. Zaburzamy każdy z wektorów zgodnie z współczynnikami i wzorem  
``                population[i][1][j] = alpha * vi[j] + b * (fittest_personal[j] - xi[j]) + c * (
                        fittest_informants[j] - xi[j]) + d * (fittest_all[j] - xi[j])
``
6. Zmieniamy prędkości zgodnie z epsilon i zaburzamy współrzędne wykraczające poza dziedzinę.
### Task 02 - Genetic algorithm to find words with given rules ( multiset ) from given dictionary of words.
#### Limited
    :param t: time limitation
    :param correct_words: set of correct words
    :param initial_words: initial correct words
    :param multiset:  dictionary of letter and frequencies (Acceptable freq)
    :param gen_times: quantity of children to be generated
1. Wczytujemy zbiór liter z wartościami - multiset.
2. Budujemy frequency table ( dopuszczalna ) restrykuje możliwe słowa do multisetu.
3. Budujemy słownik możliwych liter z wagami.
4. Wczytujemy słownik.txt i okrajamy nasz zbiór do słów prawidłowych dla frequency table.
5. Wybieramy rodziców licząć prawdopodobieństwa( f(x_i)/sum(quality(X))) w każdej iteracji szufladkując listę.
6. Krzyżujemy wybranych rodziców ( tworzymy zbiór liter z p1,p2 i próbujemy ułożyć słowo z poprawnych słów)
7. Mutujemy dziecko zachowując jego prefix lub suffix ( szukamy innego w słowniku  o tym samym suffixie/prefixie)
8. Podmieniamy starą populację na nową generację
#### Unlimited

### Task 03 - Genetic for finding exit in maze ( multiple exit ).
    :param t: time limitation
    :param n: board height
    :param m: board width
    :param s: quantity of initial solutions
    :param p: population quantity
    :param paths: initial solutions
    :param board: maze
    :param mutation: decide with function use to mixed_mutation
    :param selection: decide with function use to select parents
1. Wybieramy besta z ścieżek inicjalnych.
2. Wybieramy rodziców z populacji do skrzyżowania w sposób
    - tournament selection
    - licząć prawdopodobieństwa( f(x_i)/sum(quality(X))) w każdej iteracji szufladkując listę
3. Krzyżyujemy rodziców (two point crossover) wybierając losowe indexy i1,j1 ; i2,j2 i podmieniamy "środki" lub boki tworząc dzieci 
4. Mutujemy dzieci na sposób:
    - losowo podmieniamy dwa elementy ścieżki ( transpozycja )
    - wybieramy losowy preffix i losujemy losowej długości suffix

	
