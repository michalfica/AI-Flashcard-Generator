## Przydatne linki z dokumentacją

https://googleapis.github.io/python-genai/#mix-types-in-contents

https://git.sr.ht/~foosoft/anki-connect

## Nowe słówka: 

- SDK (Software Development Kit) - zestaw narzędzi pomocnych przy tworzeniu aplikacji i oprogramowania. W sklad SDK wchodzi między innymi: biblioteka i pliki kodu, dokumentacja, przykłady kodu. 
- adhere - trzymać się, stosować się do czegoś 

## Etapy 
### Co dziś mam zrobić? / Na jakim etapie jestem teraz? 

<!-- <li><input type="checkbox" disabled> Generowanie kontentu z konfiguracją batch_config. </li> -->

1. [ ] Zrozumieć jak działa generowanie kontentu z konfiguracją batch_config.
- Dlaczego muszę parsować odpowiedź modelu.
- W jakim formacie dostaje odpowiedź, czy to jest słownik, czy to jest json?
- Czym jest json?

- 1.1 Dodać generowanie przykładowego zdania, w którym uyte jest dane słówko.

2. [ ] Zrozumieć jak dział logger. 
- Skąd ma tyle róźnych informacji, które zapisuje mi do pliku. 
- Dlaczego zmiana levelu nie od filtrowuje mi nie potrzebnych informacji?
- Jak odfiltrowywać i nie zapisywać tylu informacji do pliku z logami. 

3. [ ] Poczytać jak mogę zwiększyć czcione, zmienić kolor itp fiszki za pomocą gen anki. 

- 3.1 Jak dodać kolejne pole do fiszki? (pole z użyciem słowa w zdaniu)

 
## Problem jakie napotykam podczas pisania projektu :
### I. Tłumaczenie listy słów lub listy fraz.

Pytania jak to zrobić, aby działało poprawnie?

- Tłumaczenie kazdego słowa z listy oddzielne - osobne zapytania.
    - duzo zapytani do modelu - kosztowne
- Zadawanie 1 zapytania do modelu aby przetłumaczył listę. 
    - Gdy podam liste słów jako ciąg napisów odzielonych spacjami, model nie wie czy to fraza czy pojedyncze słowa.
    - Przydatne jest **structured output**

### II. Logger - jak zapisywać i czytać informacje o tym co dzieje się w kodzie. 
