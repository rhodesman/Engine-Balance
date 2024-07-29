# Engine Balance

Enngine Balance is a simple application for inputing the weights of engine components and outputting the best pairings of components with similar total weight

## Install Prerequisites

```bash
pip install scipy pandas pulp
```

## Usage

Add your component weights to the weights.csv file.  You can add or remove the number of components you have and the script will adjust accordingly.  (ex: if you have a 4 cylinder engine, only input 4 rows of weights, 8 cylinder, 8 rows, etc.)

```bash
python balance.py
```