import os

# Logfile path
LOGFILE = f"log/pastebin_{os.getenv('HOSTNAME')}.log"

# RabbitMQ server scrapper queue
DOWNLOADER_QUEUE = "pastebin_downloader"
# RabbitMQ server parser queue
PARSER_QUEUE = "pastebin_parser"

# Storages:
# Temporary storage
TEMP_STORAGE = "tmp"
# Compressed downloaded files location
COMPRESSED_STORAGE = "storage"

# Scrapper's constants:
# Scraping url
SCRAPING_URL = "https://scrape.pastebin.com/api_scraping.php"
# Scraping number of results per request
SCRAPING_LIMIT = 250
# Time between two scrapper request
SCRAPING_SLEEP = 5
# Delay between two scrapper request
SCRAPING_DELAY = [0.5, 1]
# Number of fail action before stopping the process
MAX_FAILED_REQUEST = 20

# Downlaoder's constants:
# Time between two downloader request
DOWNLOADING_SLEEP = 0.5
# Delay between two downloader request
DOWNLOADING_DELAY = [0, 0.5, 1]

