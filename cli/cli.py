import csv
import sys

import click
import gspread

from api_client.private_api import PrivateAPIClient

GOOGLE_DRIVE_SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
DEFAULT_GOOGLE_CREDENTIALS_FILE = "./gsheet_credentials.json"


@click.group()
def cli():
    pass


@cli.command()
@click.option('--adherent_id', help='You can find this ID in the url of the export button in your dashboard', prompt="Adherent id")
@click.option('--from_date', help='The starting date of the interval of the export', prompt="Start date")
@click.option('--to_date', help='The ending date of the interval of the export',
              prompt='End date')
@click.option('--password', help='Your helloasso password',
              prompt='Password')
@click.option('--email', help='Your helloasso user email',
              prompt='Email')
@click.option('--output', help='The file name for the export',
              default='members_table.csv')
def export_members(output, email, password, to_date, from_date, adherent_id):
    """Export list of members of the non-profit"""
    client = PrivateAPIClient()

    client.auth(user_email=email, psw=password)
    members_table = client.get_members(from_date=from_date, to_date=to_date, adherent_id=adherent_id)

    with open(output, 'w', newline='') as file:
        writer = csv.writer(file, delimiter="\t")
        for row in members_table:
            writer.writerow(row)


@cli.command()
@click.option('--credentials', help='The credential file location', default=DEFAULT_GOOGLE_CREDENTIALS_FILE)
@click.option('--gsheet_url', help='The url of the google drive spreadsheet to update', prompt="Google sheet url")
@click.option('--gsheet_tab', help='The name of the tab to update', prompt="Google sheet tab name")
@click.option('--update_file', help='HelloAsso sheet to use for the update', prompt="Local update sheet")
def update_gsheet(update_file, gsheet_tab, gsheet_url, credentials):
    """Update online gsheet with local update file (most likely downloaded with: export_members)"""
    gc = gspread.service_account(filename=credentials, scopes=GOOGLE_DRIVE_SCOPES)

    gsheet = gc.open_by_url(gsheet_url)
    gsheet_tab = gsheet.worksheet(gsheet_tab)

    known_ids = gsheet_tab.col_values(1)

    with open(update_file, 'r', newline='') as file:
        file_reader = list(csv.reader(file, delimiter="\t"))[1:]
        rows_to_insert = []

        for row in file_reader:
            if row[0] not in known_ids:
                rows_to_insert.append(row)
                sys.stderr.write(f"[inserting member {int(row[0])}]\n")

        rows_to_insert.sort(key=lambda x: x[0], reverse=True)
        gsheet_tab.insert_rows(rows_to_insert, 2)