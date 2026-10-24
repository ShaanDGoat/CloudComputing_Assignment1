from flask import Flask, request
import threading
import logging
import json
import os


kv_store = {"name": "Shaan"}
store_lock = threading.Lock()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


app = Flask(__name__)


def load_data():
    if os.path.exists("kv_store.json"):
        with open("kv_store.json", "r") as f:
            global kv_store
            kv_store = json.load(f)
            logging.info("Data loaded from kv_store.json")


def save_data():
    with store_lock:
        with open("kv_store.json", "w", encoding="utf-8") as f:
            json.dump(kv_store, f)
    logging.info("Data saved to kv_store.json")


@app.route("/<key>", methods=["GET"])
def get_value(key):
    with store_lock:
        if key in kv_store:
            logging.info("Value retrieved for key: %s", key)
            return {"value": kv_store[key]}
    logging.info("Key not found: %s", key)
    return {"error": "Key not found"}, 404


@app.route("/<key>", methods=["POST"])
def set_value(key):
    value = request.json.get("value")
    logging.info("Setting value for key: %s", key)
    with store_lock:
        kv_store[key] = value
    logging.info("Value set for key: %s", key)
    return {"message": "Value set successfully"}


@app.route("/<key>", methods=["DELETE"])
def delete_value(key):
    with store_lock:
        if key in kv_store:
            del kv_store[key]
            logging.info("Value deleted for key: %s", key)
            return {"message": "Value deleted successfully"}
    logging.info("Key not found for deletion: %s", key)
    return {"error": "Key not found"}, 404


if __name__ == "__main__":
    load_data()
    try:
        app.run(host="127.0.0.1", port=8080, threaded=True)
    finally:
        save_data()