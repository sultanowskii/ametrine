import requests


class League:
	def __init__(self, name: str, base_url: str, admin_name: str, admin_password: str):
		self.name = name
		self.base_url = base_url
		self.__admin_name = admin_name
		self.__admin_password = admin_password
		self.nonce = None
		self.session = requests.Session()
		self.teams = {}

	def get_admin_name(self) -> str:
		return self.__admin_name

	def get_admin_password(self) -> str:
		return self.__admin_password

	def get(self, url: str, **params) -> requests.Response:
		r = self.session.get(self.base_url + url, **params)
		return r

	def post(self, url: str, **params) -> requests.Response:
		r = self.session.post(self.base_url + url, **params)
		return r

	def delete(self, url: str, **params) -> requests.Response:
		r = self.session.delete(self.base_url + url, **params)
		return r

	def put(self, url: str, **params) -> requests.Response:
		r = self.session.put(self.base_url + url, **params)
		return r

	def patch(self, url: str, **params) -> requests.Response:
		r = self.session.patch(self.base_url + url, **params)
		return r


class Team:
	def __init__(self, name: str, email: str, password: str, sid: int = -1, hidden: bool = False, banned: bool = False):
		self.name = name
		self.__password = password
		self.hidden = hidden
		self.banned = banned
		self.sid = sid
		self.users = {}

	def get_password(self) -> str:
		return self.__password


class User:
	def __init__(self, name: str, email: str, password: str, sid: int = -1, verified: bool = False, hidden: bool = False, banned: bool = False):
		self.name = name
		self.__password = password
		self.verified = verified
		self.hidden = hidden
		self.banned = banned
		self.sid = sid

	def get_password(self) -> str:
		return self.__password