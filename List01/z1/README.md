    t - czas dzialania programu, 
    b - happycat dla 0, else griewank

Uruchamiamy wykorzystujac bashowy skrypt 
tak jak jest napisane w wymaganiach formalnych Najpierw nalezy wykorzystac polecenie:
    
    make
W celu utworzenia skryptu i nadaniu mu odpowiednich praw

    ./main < In > Out 
  
 , gdzie In, Out to nazwy plikow.
Mimo wszystko uwazam, ze znacznie wygodniej jest odkomenttowac linijke
 126 : # main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
i odpalic po prostu 
    
    python3 z1.py 60 0 output_filename


Program wykorzystuje metode HillClimbing.
   1. Najpierw z kwadratu//szescianu o wymiarach -size,size sa losowane wspolrzedne startowe x'.
   2. Nastepnie obliczane sa wspolrzedne sasiada.
   3. Kolejno obliczane sa wartosci zadanej funkcji dla x' i sasiada n.
   4. Badana jest roznica pomiedzy tymi wartosciami. 
   5. Jesli wartosc sasiada jest mniejsza od aktualnej, ustalamy  nowy x' jako wlasnie porownywanego sasiada.
   6. Jesli wpadniemy w lokalne minimum program jest resetowany w nowych wspolrzednych.
   7. Poprzednie minimum lokalne jest pamietane, i nadpisywane w razie znalezienia mniejszej wartosci.
   8. Program konczy sie po okreslonej ilosci czasu t i zwraca exception TimeOut.