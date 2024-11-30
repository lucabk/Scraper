# Scraper

## 1 Ambienti di Sviluppo
### 1.1 WSL
Il progetto è realizzato, in parte, su sistema WSL. Per le configurazioni si faccia riferimento alla seguente <a href="https://github.com/lucabk/Progetto-Programmazione-Avanzata?tab=readme-ov-file#11-wsl">repository</a>. Il linguaggio di programmazione di riferimento utilizzato è Python. L'idea è quella di implementare Scraper dai più semplici, su siti statici, fino alla realizzazione di uno scraper per l'app Threads. Il progetto è diviso in cartelle. 

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

L'editor di sviluppo utilizzato è VSCode su WSL; inoltre, si è installata l'estensione "Python" e il motore di completamento di codice Jedi dalle impostazioni "settings.json" di VSCode:
```json
{
  "python.languageServer": "Jedi"
}
```
Come strumento di linting per aiuto allo sviluppo si fa uso di Pylint:
```bash
pip install pylint
```
Di conseguenza si modifica il già citato file di impostazioni:
```json
{
  "python.languageServer": "Jedi",
  "python.linting.pylintEnabled": true,
  "python.linting.enabled": true,
  "python.linting.lintOnSave": true
}
```
Si genera un file ".pylintrc":
```bash
pylint --generate-rcfile > .pylintrc
```
All'interno del file ci sono le regole da utilizzare.

### 1.2 Jupyter Notebook
Jupyter Notebook è un'applicazione web open source che consente di creare e condividere documenti che contengono codice live, equazioni, visualizzazioni e testo narrativo. Si deve quindi dapprima <a href="https://jupyter.org/install">installare Notebook</a>, comprensivo del kernel in modo tale da lavorare su un ambiente virtuale Python dedicato, al fine di evitare conflitti e di avere una gestione più pulita dei pacchetti installati. Questa parte di sviluppo verrà realizzata su sistema Windows e si consiglia di utilizzare ```cmd``` per i seguenti comandi invece di  ```PowerShell```, perché potrebbe applicare delle restrizioni.

Per prima cosa si crea l'ambiente virtuale; bisogna verificare prima che Python3 e pip3 siano correttamente installati:
```bash
C:\Users\luca>python --version
Python 3.12.4

C:\Users\luca>pip --version
pip 24.2 
```

Quindi si <a href="https://docs.python.org/3/library/venv.html">crea</a> l'ambiente virtuale:
```bash
python -m venv jupynote
```
e lo si attiva:
```bash
jupynote\Scripts\activate
```

Con la'mbiente virtuale attivo, si installa Jupyter Notebook e il kernel, in modo tale da poterlo <a href="https://medium.com/@kishanck/virtual-environments-for-jupyter-notebooks-847b7a3b4da0">utilizzare con un suo ambiente virtuale dedicato</a>:
```bash
pip install notebook ipykernel 
```
Si aggiunge manualmente il nostro virtual env come kernel alternativo per Jupyter Notebook, oltre a quello che utilizza di default:
```bash
python -m ipykernel install --user --name=jupynote
```
Il Notebook può essere lanciato tramite il comando:
```bash
jupyter notebook
```
Si aprirà una pagina web con cui dialogare con il Notebook che gira, di default, sulla porta 8888. Ora si può creare un nuovo notebook selezionando il kernel appena creato: ```kernel>change kernel```:
![image](https://github.com/user-attachments/assets/74eec0d1-cc7d-4d26-b8d8-03ae5ec0b6dd)

Per disattivare l'ambiente virtuale, come in Linux, si esegue da terminale:
```bash
deactivate
```

## 2. Applicazioni Web Statiche
### 2.1 - Un primo esempio di Scraping: ```scraper1```
Nella cartella  ```/scraper1 ``` è contenuto il primo esempio di scraper in Python. Il sito di riferimento è il seguente: https://books.toscrape.com/. In questo primo progetto si farà uso delle librerie <a href="https://www.python-httpx.org/">httpx</a> e <a href="https://github.com/rushter/selectolax">selectolax</a>; la prima è una alternativa alla classica libreria <a href="https://pypi.org/project/requests/">requests</a>, la seconda un'alternativa a <a href="https://pypi.org/project/beautifulsoup4/">beautifulsoup</a> per il parsing delle risposte HTML, ma permette unicamente di catturare i selettori CSS. Queste due scelte sono state utilizzate per garantire un approccio più moderno al web scraping.

### 2.2 - Introduzione a Scrapy: ```scraper2```
Un approccio migliore è quello di utilizzare <a href="https://docs.scrapy.org/en/latest/index.html">Scrapy</a>, un framework per lo scraping in Python. Si installa prima Scrapy:
```bash
pip install scrapy
```
La documentazione consiglia fortemente di installarlo in un ambiente virtuale Python dedicato, come quello creato in precedenza. Per creare un nuovo progetto:
```bash
scrapy startproject project_name
```
Una volta fatto ciò, come suggerisce il framework, si entra nel progetto e si crea lo spider:
```bash
cd project01
scrapy genspider books books.toscrape.com
```

Si inizia dal file ```settings.py``` decommentando la variabile USER_AGENT e cambiandola con il proprio user agent, il quale si ottiene cercando: "my user agent" sul browser.
Inoltre, per facilitare lo sviluppo si mette a false la variabile inerenti le regole di crawling del sito:
```python
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```

Il programma principale si trova nel file ```books.py``` che rappresente lo scheletro dello spider:
```python
import scrapy
class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        pass
```

Si utilizza il <a href="https://docs.scrapy.org/en/latest/topics/spiders.html#crawlspider">crawl spider</a> per accedere ad ogni libro e scorrere tutte le pagine del sito. Si setta lo url di partenza, si definiscono le rules ed il parser. Per lanciare il crawler:
```bash
scrapy crawl books
```

Si può fare un'analisi interattiva tramite la shell di scrapy
```bash
scrapy shell https://books.toscrape.com/catalogue/in-her-wake_980/index.html
```
ed interagire con i risultati. Ad esempio, per recuperare il titolo:
```bash
>>> response.css("h1")
[<Selector query='descendant-or-self::h1' data='<h1>In Her Wake</h1>'>]
>>> response.css("h1::text").get()
'In Her Wake'
>>> 
```
Questo selettore può essere successivamente utilizzato nel parser. Per semplicità, come nello scraper01 verranno recuperati unicamente titolo e prezzo di ogni libro, ma questa volta con la differenza di accedere ad ogni link specifico per libro, scorrendo tutte le pagine. 

Si farà uso anche degli Scrapy Items, utili per definire la struttura dei dati estratti. Questo permette di manipolare e pulire i dati raccolti in modo più effeciente. Quindi, si apre il file "items.py" e si va a definire lo schema dei dati estratti; nel caso d'esempio: titolo e prezzo del libro.
```python
import scrapy
class BookItem(scrapy.Item):
    title = scrapy.Field()  
    price = scrapy.Field() 
```
L'item poi verrà importato nello spider per essere popolato tramite l'<a href="https://docs.scrapy.org/en/latest/topics/loaders.html">item loaders</a>. Nel file "items.py" gli item possono essere <a href="https://docs.scrapy.org/en/latest/topics/loaders.html#declaring-input-and-output-processors">manipolati</a>.

Per visualizzare il risultato in un file JSON eseguire il comando:
```bash
scrapy crawl books -o books.json
```
Un estratto del risultato è riportato di seguito:
```python
[
{"title": "The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull", "price": "£17.93"},
{"title": "The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics", "price": "£22.60"},
{"title": "Soumission", "price": "£50.10"},
{"title": "Tipping the Velvet", "price": "£53.74"},
{"title": "The Dirty Little Secrets of Getting Your Dream Job", "price": "£33.34"},
{"title": "Sharp Objects", "price": "£47.82"},
{"title": "Sapiens: A Brief History of Humankind", "price": "£54.23"},
...
]
```

#### Riferimenti: 
Web scraping YT: https://www.youtube.com/playlist?list=PLRzwgpycm-FiTz9bGQoITAzFEOJkbF6Qp


### 2.3 Scrapy FCC


## 3. Applicazioni Web Dinamiche
### 3.1 Selenium: ```scraper3```
In questa sezione si utilizzerà <a href="https://www.selenium.dev/documentation/">Selenium</a> come primo esempioi di scraping dinamico su <a href="https://www.threads.net/?hl=en">Threads</a>. In questa
sezione  si farà uso di Jupyter Notebook per lo sviluppo. Si faccia riferimento ai capitoli precedenti per le impostazioni generali. all'interno dell'ambiente virtuale creato in precedenza si può <a href="https://pypi.org/project/selenium/">installre selenium</a>:
```bash
pip install selenium
```
Il file verrà caricato direttamente dall'interfaccia grafica di Github, senza passa per git. Ricordarsi di fare il ```pip freeze```.
