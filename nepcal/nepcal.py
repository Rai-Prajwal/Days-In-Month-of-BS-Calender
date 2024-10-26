from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
import time

# Specify the path to geckodriver or other webdriver geckodriver is used here since it is for firefox browser
service = Service('D:/geckodriver.exe')  # Adjust this path as necessary

# Set up Firefox options for headless mode and to block images and CSS
options = Options()
options.headless = True  # Enable headless mode
options.set_preference("permissions.default.image", 2)       # Block images
options.set_preference("permissions.default.stylesheet", 2)  # Block CSS

# Create the Firefox WebDriver with the specified options
driver = webdriver.Firefox(service=service, options=options)

#Adjust path as necessary
DAYS_IN_MONTHS_FILE = "C:/Users/raipr/Desktop/daysinmonth.txt"
BS_TO_AD_FILE = "C:/Users/raipr/Desktop/bstoad.txt"
PROGRESS_FILE = "C:/Users/raipr/Desktop/progress.txt"
MAX_RETRIES = 3  # Set the maximum number of retries for each page load

def update_or_append_to_file(file_path, year, line):
    # Ensure the file exists; create if not
    if not os.path.exists(file_path):
        open(file_path, 'w').close()  # Creates an empty file

    # Check if the year already exists in the file
    lines = []
    year_found = False
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, existing_line in enumerate(lines):
        if f"put({year}," in existing_line:
            lines[i] = line + '\n'  # Replace the existing line
            year_found = True
            break

    if not year_found:
        lines.append(line + '\n')  # Append the new line if year not found

    with open(file_path, 'w') as file:
        file.writelines(lines)

def save_progress(year):
    """Save progress to track the last completed year."""
    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(year))

def load_progress():
    """Load the last completed year from the progress file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return None
    return None

def remove_unwanted_elements(soup):
    """Remove all elements except essential content, images, and CSS."""
    for element in soup(["script", "style", "footer", "header", "aside", "nav"]):
        element.decompose()  # Remove the tag and its contents
    return soup

def get_highest_days_in_months_and_bs_to_ad_reference(year):
    highest_days_in_months = []
    bs_to_ad_date = None

    for month in range(1, 13):
        url = f"http://www.nepcal.com/index.php?y={year}&m={month}"
        retries = 0

        while retries < MAX_RETRIES:
            try:
                driver.get(url)
                # Wait up to 30 seconds for the "global-wrapper" element to appear
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "global-wrapper")))

                # Parse the page content and remove unwanted elements
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                soup = remove_unwanted_elements(soup)

                # Get BS to AD reference for the 1st month only
                if month == 1:
                    bs_to_ad_div = soup.find('div', id=f"tip_{year}-1-1")
                    ad_date_span = bs_to_ad_div.find('span', class_='tt_ad') if bs_to_ad_div else None
                    if ad_date_span:
                        ad_date_text = ad_date_span.get_text(strip=True)
                        adday, adyear = int(ad_date_text.split()[0]), int(ad_date_text.split()[-1])
                        bs_to_ad_date = f"LocalDate.of({adyear}, 4, {adday})"

                # Find the right_big div for days in the month
                right_big = soup.find('div', id='right_big')
                if not right_big:
                    print(f"right_big div not found for year {year}, month {month}")
                    highest_days_in_months.append(None)
                else:
                    # Find the highest day in the month
                    day_rows = right_big.find_all('div', class_='day_row_b')
                    highest_value = 0
                    for row in day_rows:
                        day_containers = row.find_all('div', class_='day_container_b')
                        for container in day_containers:
                            day_val = container.find('div', class_='dayvaln_b')
                            if day_val:
                                day_value = int(day_val.get_text(strip=True))
                                if day_value > highest_value:
                                    highest_value = day_value
                    highest_days_in_months.append(highest_value)

                break  # Exit the retry loop if successful

            except Exception as e:
                print(f"Error loading page for year {year}, month {month}: {e}")
                retries += 1
                if retries < MAX_RETRIES:
                    print(f"Retrying... ({retries}/{MAX_RETRIES})")
                    time.sleep(2)  # Optional: wait briefly before retrying
                else:
                    print(f"Failed to load page for year {year}, month {month} after {MAX_RETRIES} attempts.")
                    highest_days_in_months.append(None)

    return highest_days_in_months, bs_to_ad_date

def main():
    # Load last completed year from progress file
    start_year = load_progress() or 1975  # Start from 1975 if no progress found

    for year in range(start_year, 2101):  # Adjust range as needed
        highest_days, bs_to_ad_date = get_highest_days_in_months_and_bs_to_ad_reference(year)

        if highest_days:
            formatted_days = ','.join(map(lambda d: str(d) if d is not None else '0', highest_days))
            days_line = f"daysInMonths.put({year}, new byte[]{{{formatted_days}}});"
            update_or_append_to_file(DAYS_IN_MONTHS_FILE, year, days_line)

        if bs_to_ad_date:
            ad_line = f"bsToAdYearReference.put({year}, {bs_to_ad_date});"
            update_or_append_to_file(BS_TO_AD_FILE, year, ad_line)

        # Save progress after each completed year
        save_progress(year)

    driver.quit()

if __name__ == "__main__":
    main()
