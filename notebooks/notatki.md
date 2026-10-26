## Nowe słówka: 

- SDK (Software Development Kit) - zestaw narzędzi pomocnych przy tworzeniu aplikacji i oprogramowania. W sklad SDK wchodzi między innymi: biblioteka i pliki kodu, dokumentacja, przykłady kodu. 
- adhere - trzymać się, stosować się do czegoś 

## Etapy 
### Co dziś mam zrobić? / Na jakim etapie jestem teraz? 

1. Zrozumieć jak działa generowanie kontentu z konfiguracją batch_config.
- Dlaczego muszę parsować odpowiedź modelu.
- W jakim formacie dostaje odpowiedź, czy to jest słownik, czy to jest json?
- Czym jest json?

2. Zrozumieć jak dział logger. 
- Skąd ma tyle róźnych informacji, które zapisuje mi do pliku. 
- Dlaczego zmiana levelu nie od filtrowuje mi nie potrzebnych informacji?
- Jak odfiltrowywać i nie zapisywać tylu informacji do pliku z logami. 

3. Poczytać jak mogę zwiększyć czcione, zmienić kolor itp fiszki za pomocą gen anki. 
 
## Problem jakie napotykam podczas pisania projektu :
### I. Tłumaczenie listy słów lub listy fraz.

Pytania jak to zrobić, aby działało poprawnie?

- Tłumaczenie kazdego słowa z listy oddzielne - osobne zapytania.
    - duzo zapytani do modelu - kosztowne
- Zadawanie 1 zapytania do modelu aby przetłumaczył listę. 
    - Gdy podam liste słów jako ciąg napisów odzielonych spacjami, model nie wie czy to fraza czy pojedyncze słowa.
    - Przydatne jest **structured output**

### II. Logger - jak zapisywać i czytać informacje o tym co dzieje się w kodzie. 
