import argparse
from keyval_storage.key_value_storage import KeyValueStorage

def main():
    parser = argparse.ArgumentParser(description="Key-Value JSON Storage CLI")
    parser.add_argument("--file", required=True, help="Path to the JSON storage file")
    parser.add_argument("--action", required=True, choices=["get", "set", "delete", "list"], help="Action to perform")
    parser.add_argument("--key", help="Key for the action")
    parser.add_argument("--value", help="Value for the 'set' action")

    args = parser.parse_args()
    storage = KeyValueStorage(args.file)

    if args.action == "get":
        if not args.key:
            print("Key is required for 'get' action")
            return
        print(storage.get(args.key))

    elif args.action == "set":
        if not (args.key and args.value):
            print("Key and value are required for 'set' action")
            return
        storage.set(args.key, args.value)
        print(f"Set {args.key} to {args.value}")

    elif args.action == "delete":
        if not args.key:
            print("Key is required for 'delete' action")
            return
        storage.delete(args.key)
        print(f"Deleted key {args.key}")

    elif args.action == "list":
        print(storage.list_keys())
