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
    
    234: # t, n, g = read_data(sys.argv[1])
i zakomentowac opcjonalnie
    
```
    229: t, n, m = [int(x) for x in input().split()]
    230:arr = []
    231: for i in range(n):
    232:     z = list(input())
    233:     arr.append([int(x) for x in z if x != '\n'])
    228: b = arr
```

i odpalic po prostu 
    
    python3 z3.py file_name
    
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