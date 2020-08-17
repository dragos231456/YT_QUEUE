from SERVICE.service import Service
from REPO.song_repository import Repo
from VALIDATION.url_validator import Validator
from HOST.multithreaded_server import MultiThreaded_Server

repo = Repo()
validator = Validator()
service = Service(repo,validator)

server = MultiThreaded_Server(service)
server._start()