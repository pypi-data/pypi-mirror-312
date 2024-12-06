# currency_normalizer/currency_normalizer.py

import os
import yaml

class CurrencyNormalizer:
    def __init__(self):
        yaml_filename = 'currencies.yaml'
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            current_dir = os.getcwd()
        yaml_path = os.path.join(current_dir, yaml_filename)
        try:
            with open(yaml_path, 'r') as file:
                self.currency_data = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The file {yaml_filename} was not found.")
            self.currency_data = {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            self.currency_data = {}

    def normalize(self, value):
        value = value.strip().lower()
        for code, data in self.currency_data.items():
            if value in [
                data['symbol'].lower(),
                data['symbol_native'].lower(),
                data['name'].lower(),
                data['name_plural'].lower()
            ]:
                return code
        return None



def main():
    cn = CurrencyNormalizer()
    r=cn.normalize("$")
    print(r)

    # Get and print all available profiles

if __name__ == "__main__":
    main()