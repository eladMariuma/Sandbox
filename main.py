import logging
import json
import datetime
import sys

CONFIG_PATH = "config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_config(path: str) -> dict:
    try:
        with open(path) as json_file:
            config = json.load(json_file)
        logging.info("Configuration loaded successful")
        return config
    except FileNotFoundError:
        logging.error("File not found")
    except json.JSONDecodeError:
        logging.error("Error parding file")
        return {}

def greet_user(name: str):
    current_time = datetime.now().strftime("%H:%M:%S")
    logging.info(f"Hello {name}, today is the {current_time}")
    logging.debug(f"Username is {name} and good luck debugging forward")

def main():
    logging.info('Lets start the app;')
    config = load_config(CONFIG_PATH)
    target_user_id = config.get("target_user_id", "default_user")
    user = next((u for u in config.get("users, []") if u.get("id") == target_user_id),None)
    user_phone = user.get("phone", "default_phone")
    greet_user(user_phone)


if __name__ == "__main__":
    main()