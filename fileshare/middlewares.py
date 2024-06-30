import asyncio 
from .database import database  


# database middleware class 
class DatabaseMiddleware:
	"""
		database middleware to manage the connection and disconnection of the database within the lifecycle of an ASGI application.
		Scope parameter is a dictionary that contains details about the current request. 
		Receive is an async callable provided by the ASGI framework that you call to receive an event from the client (or in this case, from the ASGI server).
		Send is an async callable provided by the ASGI framework that you call to send a response or event back to the client (or in this case, to the ASGI server).			
	"""

	def __init__(self, app):
		self.app = app 

	async def __call__(self, scope, receive, send):
		
		if scope['type'] == 'lifespan':
			
			while True:
				
				message = await receive()

				if message['type'] == 'lifespan.startup':
					await database.connect()
					await send({'type': 'lifespan.startup.complete'})

				elif message['type'] == 'lifespan.shutdown':
					await database.disconnect()
					await send({'type': 'lifespan.shutdown.complete'})

				else:
					break
		else:
			# For any scope type other than lifespan, the middleware simply passes control to the next application or middleware in the stack.
			await self.app(scope, receive, send)


"""
	this middleware is applied directly in the asgi.py file, so there's no need to include it in settings.py
"""