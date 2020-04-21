##Simulated Annealing For Salomon's Function
0. Temperatura początkowa zostaje zainicjowana na wysoką wartość np.: 100, 1000, 10000
1. Program działa w pętli dopóki nie przekroczy limitu czasowego, lub T osiąggnie wartość 0.
2. Wyliczamy wartość funkcji Salomon'a ( quality function) na podstawie rozwiązania początkowego i zapisujemy do "historii best'ów".
3. Generujemy sąsiada neighbour aktualnego rozwiązania x.( możemy zaburzać względem wiekości wektora np x_i = x_i*(1+random.uniform(-0.99,0.99)) 
lub statycznie x_i = x_i + random.uniform(0.99,0.99))
4. Wyznaczamy wartości funkcji Salomon'a dla neighbour oraz x, wyznaczamy deltę( róznicę między tymi wartościami.)
5. Losujemy liczbę zmiennoprzecinkową z przedziału (0,1)
6. Obliczamy probability z wzoru podanego na wykładzie <img src="https://latex.codecogs.com/svg.latex? p=e^{\frac{delta}{T}}"/>
7. Jeśli wylosowana wartość(0,1) jest mniejsza od wyliczonej probability to przechodzimy do sąsiada tzn, ustalamy x = neighbour.
8. Zmniejszamy T( temperaturę ) w określony sposób ( jeden z wykładów np T_{i+1}= T_i/log(i))
9. Sprawdzamy czy aktualna wartość jest lepsza od najlepszej dotychczas znalezionej best, jeśli tak dodajemy do historii.
10. Wracamy do 3.


W programie została zaimplementowana również możliwość reset'ów. Tzn jeśli wpadniemy w lokalne minimum lub wpadniemy po prostu na "złą trasę"
to restartujemy, tzn cofnięcia się do naszego dotychczas najlepszego rozwiązania i wylosowanie nowego sąsiada, wtedy być może pójdźiemy w innym kierunku
niż ostatnio i uciekniemy w taki sposób z minimum lokalnego.
Ewentualnie można też zrobić losowy spawn na określonym przedziale np(-10,10)(chyba), ale wydaje się to mniej ciekawe.
Została też zaimplementowana możliwość rysowania wykresów funkcji kosztu, czy nawet zmian samych współrzędnych wektora.