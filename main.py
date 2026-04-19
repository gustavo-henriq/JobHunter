from cathoScraper import get_catho
from database import insert_many_silver

jobs = get_catho()
insert_many_silver(jobs)