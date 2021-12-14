# AMICA: Argument Mining In Covid-19 Articles

Il servizio sviluppato per amica si compone di due servizi: uno per la gestione e l'inserimento di paper nel database e uno per il rendering dei papers in base alla query fornita. 

<details>
<summary><b>Papers downloader service</b></summary>

## Papers downloader service 

Questo servizio è mirato all'estrazione, labelling con margot e inserimento di papers e pre-prints sul covid in un database mongoDb. 
La pipeline di lavoro è definita nel file ```main.py``` dove vengono richiamate le diverse fasi della stessa attraverso gli opportuni moduli definiti nella cartella services.

#### Fase 1: Connessione al database 

La prima operazione eseguita dal servizio è la connessione al database specificato in fase di run del programma, il database contiene la collection papers, formata dai paper formattati come definito nel file ```models/Paper.py```

#### Fase 2: Download dei papers 

La seconda fase consiste nello scaricare i papers rilevanti al covid dalle varie fonti tramite chiamate http ai server specifici. 
Tutti i moduli per scaricare i dati sono definiti nella cartella ```services/paperDownloaders```. 
I risultati vengono filtrati, mandando alla fase successiva solo i paper non presenti nel database. 

#### Fase 3: Processing con Grobid

I papers rimanenti vengono processati da grobid, tool per estrarre testo da un pdf. 
Il modulo che implementa il servizio è ```services/textExtractor/TextPdfExtractor.py```.

#### Fase 4: Labelling con margot 

Il testo estratto nella fase precedente viene processato da margot, come definito nel file ```services/margot/MargotClient.py```. 
L'output di margot viene salvato nel formato definito da ```models/MargotSentence.py``` per ogni frase analizzata. 

#### Fase 5: Inserimento nel db 

Alla fine del processo ogni nuovo paper analizzato viene inserito nel database. 

#### Come lanciare il programma 

```python3 main.py --margot "path della cartella con gli eseguibili di margot" --workingDir "cartella di output dei file di margot" --dbName "nome del database" --dbHost "host del database"```

</details>
<details>
<summary><b>Query handler</b></summary>

## Query handler

Questo tool è mirato alla costruzione della risposta alla query inserita nel servizio <b>amica</b>.
Il programma prende in input la query e gli estremi di un database da cui prendere gli articoli. 

### Processing della query

La query viene divisa in parole singole, creando una lista di keywords $k$. 

### Ranking degli articoli 

La funzione di ranking è definita nel file ```utils/margotSentences/sorting.py```
Gli articoli vengono ordinati in base ad uno score, assegnato ad ogni paper $p$, ottenuto dalla moltiplicazione di due fattori:
1. Correspondance score: <a href="https://www.codecogs.com/eqnedit.php?latex=\bg_white&space;\frac{1}{len(p)}\sum_{i=1}^{len(p)}{\sum_{j=1}^{len(k)}&space;\frac{corr(k_j,&space;p_i)}{len(k)}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\bg_white&space;\frac{1}{len(p)}\sum_{i=1}^{len(p)}{\sum_{j=1}^{len(k)}&space;\frac{corr(k_j,&space;p_i)}{len(k)}}" title="\frac{1}{len(p)}\sum_{i=1}^{len(p)}{\sum_{j=1}^{len(k)} \frac{corr(k_j, p_i)}{len(k)}}" /></a>.<br>Dove corr(keyword, sentence) = 1 se keyword presente in sentence, 0 se no.
1. Margot score: <a href="https://www.codecogs.com/eqnedit.php?latex=\bg_white&space;\frac{1}{len(p)}&space;\sum_{i=1}^{len(p)}&space;\max{&space;\{&space;CS(p_i),&space;ES(p_i)&space;\}&space;}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\bg_white&space;\frac{1}{len(p)}&space;\sum_{i=1}^{len(p)}&space;\max{&space;\{&space;CS(p_i),&space;ES(p_i)&space;\}&space;}" title="\frac{1}{len(p)} \sum_{i=1}^{len(p)} \max{ \{ CS(p_i), ES(p_i) \} }" /></a>.
<br>Dove CS(sentence) è il claim score della frase assegnato da margot e ES(sentence) è l'evidence score della frase stabilito dalla stessa.

### Rendering in html 

La lista ordinata di articoli viene trasformata in .html come definito nei files ```models/Body.py``` e ```web/templates/body.html``` tramite la libreria <b>jinja2</b>.
</details>
