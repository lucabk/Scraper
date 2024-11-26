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


## 1. Applicazioni Web Statiche
### 1.1 - Un primo esempio di Scraping
Nella cartella  ```/scraper1 ``` è contenuto il primo esempio di scraper in Python. Il sito di riferimento è il seguente: https://books.toscrape.com/. In questo primo progetto si farà uso delle librerie <a href="https://www.python-httpx.org/">httpx</a> e <a href="https://github.com/rushter/selectolax">selectolax</a>; la prima è una alternativa alla classica libreria <a href="https://pypi.org/project/requests/">requests</a>, la seconda un'alternativa a <a href="https://pypi.org/project/beautifulsoup4/">beautifulsoup</a> per il parsing delle risposte HTML, ma permette unicamente di catturare i selettori CSS. Queste due scelte sono state utilizzate per garantire un approccio più moderno al web scraping.

### 1.2 - Introduzione a Scrapy
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


### 1.3 