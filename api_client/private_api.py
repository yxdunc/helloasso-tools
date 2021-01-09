class PrivateAPIClient:
	def auth(self, user_email, psw):
		# https://api.helloasso.com/v5/auth/antiforgerytoken
		
		# https://api.helloasso.com/v5/auth/login
		## Content-Type: application/json
		## x-csrf-token: [TOKEN]
		## cookies...
		
		self.auth_token = f"Bearer {resp.cookies['tm5-HelloAss']}"}
		self.cookies = resp.cookies

	def get_org_details(self):
		# https://api.helloasso.com/v5/users/me/organizations
		## authorization: self.auth_token
		## cookies...
		pass

	def get_users(self):
		# https://www.helloasso.com/admin/handler/reports.ashx?type=Details&id_adh=[ID?]&from=1/11/2020&to=8/1/2021&includeSubpages=1&period=MONTH&domain=HelloAsso&trans=Adhesions&format=Csv
		pass
