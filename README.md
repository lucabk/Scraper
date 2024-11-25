# Scraper

Il progetto è realizzato su sistema WSL. Per le configurazioni si faccia riferimento alla seguente <a href="https://github.com/lucabk/Progetto-Programmazione-Avanzata?tab=readme-ov-file#11-wsl">repository</a>. Il linguaggio di programmazione di riferimento utilizzato è Python. L'idea è quella di implementare Scraper dai più semplici, su siti statici, fino alla realizzazione di uno scraper per l'app Threads. Il progetto è diviso in cartelle. 

E' necessaria l'installazione di Python3, pip3 e dell'ambiente virtuale. Si può far riferimento alla seguente <a href="https://learn.microsoft.com/it-it/windows/python/web-frameworks#install-python-pip-and-venv">guida</a>. Ubuntu su WSL dovrebbe avere Python già installato. I comandi da lanciare sono:
```bash
sudo apt install python3-pip
sudo apt install python3-venv
```
per installare pip e l'ambiente virtuale. Per controllare la versione di Python e di pip, eseguire: ``` pip3 --version ``` e ``` python3 --version ``` rispettivamente. Successivamente, si crea l'ambiente virtuale con il comando:
```bash
python3 -m venv scraper_env
```
e si attiva con:
```bash
source scraper_env/bin/activate
```
Per installare le dipendenze si utilizza il comando: ``` pip install -r requirements.txt ```. Per aggiornare il file dei requisiti: ``` pip freeze > requirements.txt ```

 ## 1. Applicazioni Web Statiche
 ### 1.1 - Un primo esempio di Scraping
 Nella cartella "/scraper1" è contenuto il primo esempio di scraper in Python. Il sito di riferimento è il seguente: https://books.toscrape.com/. In questo primo progetto si farà uso delle librerie <a href="https://www.python-httpx.org/">httpx</a> e <a href="https://github.com/rushter/selectolax">selectolax'</a>; la prima è una alternativa alla classica libreria <a href="https://pypi.org/project/requests/">requests</a>, la seconda un'alternativa a <a href="https://pypi.org/project/beautifulsoup4/">beautifulsoup</a> per il parsing delle risposte HTML, ma permette unicamente di catturare i selettori CSS. Queste due scelte sono state utilizzate per garantire un approccio più moderno al web scraping.
