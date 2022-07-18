from utils.bot import Viridian
from dotenv import load_dotenv

load_dotenv(".env")

if __name__ == "__main__":
    bot = Viridian()
    bot.run()
