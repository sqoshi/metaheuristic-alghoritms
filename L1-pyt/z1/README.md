t - czas dzialania programu 
b - happycat dla 0, else griewank
output_filename - nazwa pliku docelowego outputu

python3 t b output_filename

example:
python3 Finder.py 60 0 hcE


program wykorzystuje metode HillClimbing.
Najpierw z kwadrau//szescianu o wymiarach -size,size sa losowane wspolrzedne startowe x'.
Nastepnie obliczane sa wspolrzedne sasiada.
Kolejno obliczane sa wartosci zadanej funkcji dla x' i sasiada n.
Badana jest roznica pomiedzy tymi wartosciami. Jesli wartosc sasiada jest mniejsza od aktualnej, ustalamy  now x' jako wlasnie porownywanego sasiada.
Jesli wpadniemy w lokalne minimum program jest resetowany w nowych wspolrzednych.
Poprzednie minimum lokalne jest pamietane, i nadpisywane w razie znalezienia mniejszej wartosci.
Program konczy sie po okreslonej ilosci czasu t.