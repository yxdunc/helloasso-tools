import csv
import sys
import requests

DEFAULT_FROM_DATE = "1/10/2020"
DEFAULT_TO_DATE = "1/1/2021"

URL_ANTI_FORGERY = "https://api.helloasso.com/v5/auth/antiforgerytoken"
URL_AUTH = "https://api.helloasso.com/v5/auth/login"
URL_ORG_DETAILS = "https://api.helloasso.com/v5/users/me/organizations"
URL_USER_EXPORT = "https://www.helloasso.com/admin/handler/reports.ashx?type=Details&id_adh={adherent_id}&from={from_date}&to={to_date}&includeSubpages=1&period=MONTH&domain=HelloAsso&trans=Adhesions&format=Csv"


class PrivateAPIClient:
	def __init__(self):
		self.http_session = requests.Session()
		self.x_csrf_token = None
		self.auth_token = None

	def auth(self, user_email, psw):
		resp = self.http_session.get(URL_ANTI_FORGERY)
		self.x_csrf_token = resp.text[1:-1]

		sys.stderr.write(f"[anti forgery token]: {resp.status_code}\n")
		if not resp.ok:
			sys.stderr.write(f" error: {resp.text}\n")
			exit(-1)

		headers = {
			"Content-Type": "application/json",
			"x-csrf-token": self.x_csrf_token,
		}

		body = {
			"email": user_email,
			"password": psw,
		}

		resp = self.http_session.post(URL_AUTH, headers=headers, json=body)

		sys.stderr.write(f"[authentication]: {resp.status_code}\n")
		if not resp.ok:
			sys.stderr.write(f" error: {resp.text}\n")
			exit(-1)

		self.auth_token = f"Bearer {resp.cookies['tm5-HelloAsso']}"

	def get_org_details(self):
		headers = {
			"authorization": self.auth_token
		}
		resp = self.http_session.get(URL_ORG_DETAILS, headers=headers)

		return resp.json()

	def get_members(self, adherent_id, from_date=DEFAULT_FROM_DATE, to_date=DEFAULT_TO_DATE):
		"""
		Get a table with all adherent who registered between {from_date} and {to_date}

		:param adherent_id: You can find it in the url behind the export button
		:param from_date: "DD/MM/YYYY"
		:param to_date: "DD/MM/YYYY"
		:return: A formatted CSV table
		"""
		formatted_url = URL_USER_EXPORT.format(adherent_id=adherent_id, from_date=from_date, to_date=to_date)
		resp = self.http_session.get(formatted_url)

		table = csv.reader(resp.text.splitlines(), delimiter=";")

		return table
