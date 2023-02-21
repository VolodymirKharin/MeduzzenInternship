from environs import Env

env = Env()
env.read_env("./.env")
HOST = env("HOST")
PORT = int(env("PORT"))
