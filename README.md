## Usage

This repository provides a script to scrape calendar data for the Bikram Sambat (B.S.) calendar, as well as a pre-scraped data file (`daysinmonth.txt`) and (`bstoad.txt`) . If you only need the calendar data, you can directly refer to the data file without running the script.

To access the data:
1. Open `daysinmonth.txt`/`bstoad.txt` for a snapshot of the calendar data as of [2024/10/26].
2. Alternatively, run the script (`nepcal.py`) if you need the most recent data.

> **Note**: This data file is a static snapshot and may not reflect updates from the original website. Running the script may result in different data if the source website has been updated.

## Data Snapshot

`daysinmonth.txt` has data of number of days in a month in a year and `bstoad.txt` is the reference date for Baisakh 1st of each year in A.D.

```plaintext
# Snapshot from daysinmonth.txt file

daysInMonths.put(1975, new byte[]{31,31,32,32,31,30,30,29,30,29,30,30});
daysInMonths.put(1976, new byte[]{31,32,31,32,31,31,30,30,30,29,30,31});
daysInMonths.put(1977, new byte[]{31,32,32,32,32,31,30,30,30,30,30,31});
daysInMonths.put(1978, new byte[]{31,31,32,32,31,31,31,30,30,30,30,30});
daysInMonths.put(1979, new byte[]{31,31,32,32,32,30,30,30,30,29,30,30});
daysInMonths.put(1980, new byte[]{31,32,32,32,32,31,30,30,29,29,30,31});

# Snapshot from bstoad.txt file

bsToAdYearReference.put(1975, LocalDate.of(1918, 4, 13));
bsToAdYearReference.put(1976, LocalDate.of(1919, 4, 13));
bsToAdYearReference.put(1977, LocalDate.of(1920, 4, 13));
bsToAdYearReference.put(1978, LocalDate.of(1921, 4, 13));
bsToAdYearReference.put(1979, LocalDate.of(1922, 4, 13));
bsToAdYearReference.put(1980, LocalDate.of(1923, 4, 13));
```

## Note on Data Structure

The data shown here is implemented in Java as a `HashMap`:

- **`daysInMonths`**: A `HashMap<Integer, byte[]>` that stores the number of days in each month for specific years in the Bikram Sambat (B.S.) calendar. Each entry's key is a year (e.g., `1975`), and the value is an array of bytes where each byte represents the days in a particular month.

- **`bsToAdYearReference`**: A `HashMap<Integer, LocalDate>` that maps each B.S. year to a corresponding date in the Gregorian (AD) calendar, providing a reference point for year conversions between the two calendars.

These `HashMap`s allow efficient lookup and organization of calendar data by year.


## Disclaimer
This script is intended solely for educational and personal use. It scrapes publicly accessible data (days in each month for years in the Bikram Sambat (B.S.) calendar) from [nepcal.com]. No sensitive, personal, or copyrighted data is collected or distributed through this project. The script is designed to make minimal requests to avoid impacting the website's performance. Users of this script are encouraged to respect the website's terms of service and use it responsibly. 

This script is not affiliated with or endorsed by [nepcal.com]. If the website owner requests removal of this data or usage adjustment, users are encouraged to comply.
