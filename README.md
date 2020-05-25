# Metaheuristic alghoritms

1. Local Search
2. Hill Climbing (shotgun hill climbing)
3. Tabu Seach
	- tabu list
4. Simulated Annealing
	- temperature
5. Particle Swarm
	- velocity vector
	- does not select parents
6. Genetic Alghorithm
	- tournament selection
	- quality selection(random)
	- two-point crossover

## List 01
### Task 01 - shotgun local serach, hill climbing

Program wykorzystuje metode HillClimbing.
   1. Najpierw z kwadratu//szescianu o wymiarach -size,size sa losowane wspolrzedne startowe x'.
   2. Nastepnie obliczane sa wspolrzedne sasiada.
   3. Kolejno obliczane sa wartosci zadanej funkcji dla x' i sasiada n.
   4. Badana jest roznica pomiedzy tymi wartosciami. 
   5. Jesli wartosc sasiada jest mniejsza od aktualnej, ustalamy  nowy x' jako wlasnie porownywanego sasiada.
   6. Jesli wpadniemy w lokalne minimum program jest resetowany w nowych wspolrzednych.
   7. Poprzednie minimum lokalne jest pamietane, i nadpisywane w razie znalezienia mniejszej wartosci.
   8. Program konczy sie po okreslonej ilosci czasu t i zwraca exception TimeOut.
   
### Task 02 - tsp tabu serach cities minimal distance
    
Markup:
   1. Wczytuje plik z danymi
   2. Wchodzi w procedure main ktora przerywa dzialanie po okreslonym czasie t wczytanym z pliku.
   3. w czas dzialania w petli pracuje algorytm tabu-search z zadanym startowym wierzcholkiem src.
   4. Wstepnie program znajduje get_initial bazujace na algorytmie zachlannym. 
   ( po po prostu bierze kolejne minimalne dystanse i pamieta do ktorch miast nie moze juz wstapic.)
    Nie jest dla mnie pewne co znaczy "pierwsze miasto",
     bo za pierwsze miasto moge chyba uznac dowolne, 
     wiec ja uznalem ze startuje z miasta 26,
      co nie powinno robic roznicy to w koncu cykl.
   5. Naszym x staje sie teraz get_initial
   6. algorytm zamyka sie w petli dopoki nie przerwie go timeout.
    Jednak co LIMIT przejsc petli 
    algorytm moze wpasc w lokalne
   minima i wtedy warto uzyc resetu 
   to znaczy losowego zespawnowania od nowa 
   i rozpoczecia algorytmu z uwzglednieniem ostatniego przeszukiwania,
    najlepszy wynik dotychczas jest zapisany, nie utracimy go.
   8. Generowani sa sasiedzi aktualnego x 
   czyli po prostu wszystkie inwersje.
   7. za aktualnego minVal ustawiamy 
   pierwszego sasiada (to tylko chwilowe, 
    chyba ze nie znajdzie sie lepszy)
   9 Przechodzimy po kazdym z sasiadow, ktory nie jest w Tabu 
   i porowujemy jego calkowity dystans z aktualnym minimum
   10. jesli jest mniejszy to aktualnym x'em staje 
   sie terazniejszy sasiad
   11 jednoczesnie sprawdzamy czy ten wynik 
   jest wynikiem lepszym od naszego 
   najmniejszego minimum jesli tak nadpisujemy wartosc.
   12. Minimalne wyniki caly czas zapisuje w liscie BestSolutions, i wybiore najkrotszy path, ze wszystkich resetow.

Co do tych resetow, nie jestem pewien czy
 dokladnie tak to ma wygladac, ale jesli okazalby sie 
ze to jest bledne wystarczy zakomentowac linijki, 
ale skoro miasta sa w cyklu i jesli odlegosc 
od miasta A do miasta B bylaby zerem to znaczy ze miasto A=B, wiec resety z innych poczatkow 
i tak powinni schodzic do tej samej drogi - (miasto startowe nie ma znaczenia?)

    # 99 : cycles += 1
    # 116 : tabu_search(graph, n, random.randint(0, n))  # resetuje wyszukiwanie w innym wierzcholku jesli wpadl w lokalne min

Wtedy, resety sa wylaczone i algorytm skupia sie na dokladnie jednym wierzcholku i sciezce.
Bez resetow wyniki dochodza do  srednio 400-440, a z resetami spadaja nawet do 350 dla data1:),
natomiast sciezka dla data jest, tak szybko znajdowana, ze resety nie maja chyba nawet sensu.
Zdaje sobie sprawe rowniez z magicznych liczb jakimi sa iteracje LIMIT, ale bez 
```
    limit = 100
    if n < 25:
        limit = 10000
```
Bez tego urywka, wszystko jest ok dla wylaczonych resetow, z resetami dla malej ilosc miast, 
program wykonuje sie tak szybko, ze ilosc mozliwych wywolan rekursji jest przekroczona i wyskakuje poza dobrym wynikiem, error.


### Task 03 - maze exit tabu search
Markup:
   1. Znajduje rozwiazanie poczatkowe idac do gory do sciany, pozniej w prawo, dol, lewo i znowu gora, Jesli spotka wyjscie wychodzi.
   2. Nastepnie ustalamy je jako currentBest
   3. zapamietujemy ostatni ruch bo jest on staly, nie da sie wejsc inaczej do 8mki lezacej po prawej stronie niz R.
   4. ustawiamy tabu na pusty
   5. teraz performujemy swapy pozycji. 
   6. W wyniku 5. pojawiaja sie sekwencje LR RL, ktore sa staniem w miejscu.
   7. Problem tkwi w tym, ze mozemy przejsc za sciane w wyniku takiego algorytmu.
   8. przegladamy kazdego sasiada ktory nie jest w Tabu, i sprawdzamy na podstawie ilosci krokow,
    czy znalezlismy lepsze rozwiazanie, i jednoczesnie czy to rozwiazanie nie przechodzi przez sciane, tzn trasa konczy sie w odpowiednim miejscu.
   9. jesli przekracza nasza aktualna minimalna trasne to podmieniamy,
    a probkowane dodajemu do tabu.
    
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
```
c, s = simulated_annealing_prefixes(50, b, T0=1000, graph=False)
```

	
