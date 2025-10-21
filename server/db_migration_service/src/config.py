import os
from dataclass import dataclass

load_dotenv('../../.env')

@dataclass
class DatabaseConfig:
    host: srt = os.getenv('')