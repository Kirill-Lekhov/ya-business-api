class APIError(Exception):
	"""
	Basic API error.
	"""
	pass


class AuthenticationError(APIError):
	"""
	User authentication error.
	"""
	pass


class CSRFTokenError(APIError):
	"""
	Invalid CSRF token error.
	"""
	pass
