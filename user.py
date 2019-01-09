import os
import sys
import json
import time

PATH_USERS = "users/"
PATH_SECRETS = "secrets/"
PATH_STATS = "stats/"

# Currently, this only holds the last use
class Stats():
	last_login = None
	user = None

	def __filename(self):
		return PATH_STATS + self.user.user_id + "-" + self.user.ext + ".stats"

	def __init__(self, user):
		self.user = user
		filename = self.__filename()
		if os.path.isfile(filename):
			with open(filename) as f:
				stats = json.load(f)	
			self.last_login = stats.get("last_use")
	
	def update(self):
		# update the last use field with the current time
		stats = { "last_use": time.time() }
		with open(self.__filename(), 'w') as f:
			json.dump(stats, f)
	

class User():
	user_id = None
	ext = None
	personal_data = False

	# public - person
	salutation = None
	first_name = None
	last_name = None
	# public - organization
	org_name = None
	org_add_name = None
	# personal_data
	street = None
	zip = None
	city = None
	country = None

	stats = None
	messaging = None

	@classmethod
	def exists(cls, user_id, ext = "1"):
		filename = PATH_USERS + user_id + "-" + ext + ".user"
		return os.path.isfile(filename)
	
	@classmethod
	def get(cls, user_id, ext, personal_data = False):
		from messaging import Messaging
		filename = PATH_USERS + user_id + "-" + ext + ".user"
		if not os.path.isfile(filename):
			return None
		with open(filename) as f:
			dict = json.load(f)
	
		user = cls()
		user.user_id = user_id
		user.ext = ext
		user.salutation = dict.get("salutation", "")
		user.first_name = dict.get("first_name", "")
		user.last_name = dict.get("last_name", "")
		user.org_name = dict.get("org_name", "")
		user.org_add_name = dict.get("org_add_name", "")
		
		user.personal_data = personal_data
		if (personal_data):
			user.street = dict.get("street", "")
			user.zip = dict.get("zip", "")
			user.city = dict.get("city", "")
			user.country = dict.get("country", "")
			user.stats = Stats(user)
		
		user.messaging = Messaging(user)

		return user

	@classmethod
	def login(cls, user_id, ext, password, force = False):
		filename = PATH_SECRETS + user_id + "-" + ext + ".secrets"
		if not os.path.isfile(filename):
			return None
		with open(filename) as f:
			dict = json.load(f)

		if password != dict.get("password") and not force:
			return None

		return cls.get(user_id, ext, True)
