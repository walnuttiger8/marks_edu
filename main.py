import bot
import socket


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(client)

bot = bot.Bot()
bot.run()

