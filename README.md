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
python -m cli export-members --adherent_id=[id] --from_date=1/12/2020 --to_date=1/1/2021 --email="john.doe@foobar.com"
```

### Update Gsheet

Follow these instructions to generate a credential file for google drive and gsheet: https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access-for-a-project

⚠ If you create "Service account" make sure to share the spreadsheet document with this service account by inviting its generated email address.

Copy the credential file at the root of the repository and name it: `gsheet_credentials.json`

```bash 
python -m cli update-gsheet   --gsheet_url="https://docs.google.com/spreadsheets/..." --gsheet_tab="Sheet1" --update_file=members_table.csv
```
