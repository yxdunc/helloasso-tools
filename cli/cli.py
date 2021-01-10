import csv

import click
from api_client.private_api import PrivateAPIClient


@click.command()
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
