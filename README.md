# helloasso
Client for helloasso private(WIP) and public(NDY) api. Along with some automatisation(NDY).
At the moment only based on the need of one non-profit, feel free to open an issue if you need a specific feature.

## install

```bash
pip install -r requirements.txt
```

## Usage

### Export .csv file with new members for a given time span
```bash 
python -m cli --adherent_id=[id] --from_date=1/12/2020 --to_date=1/1/2021 --email='john.doe@foobar.com'
```
