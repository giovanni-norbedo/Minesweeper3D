# Minesweeper3D

<img src="m3d.png" alt="Screenshot di Minesweeper3D" width="600">

**Autori:** Giovanni Norbedo e Marco Carmignano

**Corso:** Computabilità, Complessità e Logica

## Descrizione

Minesweeper3D è un'implementazione tridimensionale del classico gioco Minesweeper, sviluppato utilizzando la libreria Ursina in Python. Il gioco presenta una griglia di cubi 3D, alcuni dei quali contengono mine. L'obiettivo è rivelare tutti i cubi che non contengono mine, utilizzando i numeri sui cubi rivelati come indizi sul numero di mine adiacenti.

## Caratteristiche

* **Gameplay 3D:** Esplora il campo minato in tre dimensioni, aggiungendo una nuova prospettiva alla sfida classica.
* **Modalità Flag:** Segna i cubi sospetti con una bandiera per evitare di farli esplodere.
* **Livelli di Difficoltà:** Scegli tra diversi livelli di difficoltà per adattare la sfida alle tue abilità.
* **Dimensioni Griglia Variabili:** Personalizza le dimensioni della griglia per un'esperienza di gioco più complessa.
* **Risolutore automatico**: Non sai più cosa fare? Sfrutta il risolutore automatico, potrai farti risolvere l'intero cubo o farti fornire una risoluzione parziale.

## Implementazione Tecnica

Il progetto è strutturato in diversi file Python per una migliore organizzazione:

* `main.py`: Punto di ingresso principale del gioco.
* `game.py`: Contiene la logica del gioco, inclusi la generazione del campo minato, la gestione degli eventi di gioco e l'algoritmo flood-fill.
* `ui.py`: Gestisce l'interfaccia utente, inclusi i menu, i pulsanti e la visualizzazione del gioco.
* `config.py`: Contiene le variabili di configurazione del gioco.
* `sat.py`: Contiene tutto il codice relativo all'implementazione del SAT Solver Z3. **È il fulcro del progetto**


## Scopo del progetto (Z3)

Lo scopo del progetto è integrare il theorem prover Z3 per creare un risolutore automatico per il gioco. Z3 verrà utilizzato per modellare la logica del gioco e dedurre le mosse sicure, trovare le mine nel campo e risolvere autonomamente l'intero cubo, fornendo un'interessante applicazione pratica dei concetti di computabilità, complessità e logica. L'idea è di utilizzare Z3 per:

1. **Formalizzare le Regole:**  Rappresentare le regole del Minesweeper in una forma logica comprensibile a Z3.
2. **Codificare lo Stato del Gioco:** Tradurre lo stato attuale del gioco (cubi rivelati, numeri, bandiere) in asserzioni Z3.
3. **Generare Query:** Formulare query a Z3 per determinare le mosse sicure o le posizioni delle mine.
4. **Interpretare i Risultati:**  Utilizzare i risultati di Z3 per guidare le azioni di gioco dell'utente o risolvere automaticamente il gioco.


## Installazione

- Assicurati di avere Python3 installato
- Installa uv da https://docs.astral.sh/uv/getting-started/installation/
- Clona questo repository:
- `git clone https://...`
- Naviga nella cartella del progetto:
- `cd Minesweeper3D`
- Installa le dipendenze:
- `uv sync`
- Esegui il gioco:
- `uv run python3 main.py`
