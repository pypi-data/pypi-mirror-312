import os
import sys
from pathlib import Path

from dotenv import load_dotenv


class Config:
    def __init__(self):
        self.home_config = os.path.join(os.path.expanduser("~"), ".smart-pr-generator")
        self.project_env = os.path.join(os.getcwd(), ".env")

    def load_env(path=".env"):
        if not (env_path := Path(path).expanduser()).exists():
            return
        os.environ.update(
            dict(
                line.split("=", 1)
                for line in env_path.read_text().splitlines()
                if line.strip() and not line.startswith("#")
            )
        )

    def load_env_files(self) -> None:
        if os.path.exists(self.home_config):
            load_dotenv(self.home_config)
        if os.path.exists(self.project_env):
            load_dotenv(self.project_env, override=True)

        # Get API key with fallback
        api_key = os.environ.get("SMART_PR_GENERATOR_API_KEY") or os.environ.get(
            "LAAS_API_KEY"
        )
        if not api_key:
            print(
                "❌ API key not found. Please set SMART_PR_GENERATOR_API_KEY or LAAS_API_KEY environment variable."
            )
            sys.exit(1)

        os.environ["LAAS_API_KEY"] = api_key

        langchain_key = os.environ.get("LANGCHAIN_API_KEY")
        if langchain_key is not None:
            os.environ["LANGCHAIN_API_KEY"] = langchain_key
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = "Smart PR Generator"
            os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        
