import random
import csv
import hashlib

def read_pin_data_from_csv(file_path):
    pin_data = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row_number, row in enumerate(reader, start=1):
            if len(row) >= 1:
                pin = row[0].strip()

                # Remove non-numeric characters from the PIN
                pin = ''.join(filter(str.isdigit, pin))

                if pin.isdigit() and len(pin) == 4:
                    pin_data[pin] = 1
                else:
                    print(f"Invalid data in row {row_number}: {row}")
            else:
                print(f"Invalid data in row {row_number}: {row}")
    return pin_data

# Read PIN frequency data from CSV file
file_path = 'C:/Users/adamo/Downloads/four-digit-pin-codes-sorted-by-frequency-withcount.csv'
pin_data = read_pin_data_from_csv(file_path)

class ServiceCracker:
    def crack_pin(self, target_pin_hash):
        for pin in pin_data.keys():
            hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
            if hashed_pin == target_pin_hash:
                return pin
        return None

# Example usage:
service_cracker = ServiceCracker()

# Replace 'TARGET_PIN_HASH' with the actual SHA-256 hash of the PIN you want to crack
target_pin_hash = input("Enter the SHA-256 hash of the 4-digit PIN you want to crack: ")

cracked_pin = service_cracker.crack_pin(target_pin_hash)
if cracked_pin is not None:
    print(f"Successfully cracked the PIN: {cracked_pin}.")
else:
    print(f"Failed to crack the PIN.")
