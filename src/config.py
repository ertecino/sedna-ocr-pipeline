import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "input_docs"
OUTPUT_DIR = BASE_DIR / "output_csv"
ARCHIVE_DIR = BASE_DIR / "archive"

# API Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model
MODEL_NAME = "gemini-3.1-pro" # or gemini-2.5-pro, using 3.1 as per requirements
