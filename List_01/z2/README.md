    t - czas dzialania programu, 
    n - ilosc miast
    g - abstrakcyjny graf
Uruchamiamy wykorzystujac bashowy skrypt 
tak jak jest napisane w wymaganiach formalnych Najpierw nalezy wykorzystac polecenie:
    
    make
W celu utworzenia skryptu i nadaniu mu odpowiednich praw

    ./main < In > Out 
  
 , gdzie In, Out to nazwy plikow.
Mimo wszystko uwazam, ze znacznie wygodniej jest odkomenttowac linijke
    
    130: # t, n, g = readData(sys.argv[1])
i zakomentowac opcjonalnie
    
    128: t, n = [int(x) for x in input().split()]
    129: g = [[int(x) for x in input().split()] for i in range(n)]

i odpalic po prostu 
    
    python3 z2.py file_name
    
Markup:
   1. Wczytuje plik z danymi
   2. Wchodzi w procedure main ktora przerywa dzialanie po okreslonym czasie t wczytanym z pliku.
   3. w czas dzialania w petli pracuje algorytm tabu-search z zadanym startowym wierzcholkiem src.
   4. Wstepnie program znajduje initialSolution bazujace na algorytmie zachlannym. 
   ( po po prostu bierze kolejne minimalne dystanse i pamieta do ktorch miast nie moze juz wstapic.)
    Nie jest dla mnie pewne co znaczy "pierwsze miasto",
     bo za pierwsze miasto moge chyba uznac dowolne, 
     wiec ja uznalem ze startuje z miasta 26,
      co nie powinno robic roznicy to w koncu cykl.
   5. Naszym x staje sie teraz initialSolution
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
