import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data from the URL."""
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except Exception as e:
        raise Exception(f"Error downloading data: {e}")

def processData(file_content):
    """Processes the CSV content and returns a dictionary mapping ID to (name, birthday)."""
    logger = logging.getLogger('assignment2')
    personData = {}
    lines = file_content.splitlines()

    for line_num, line in enumerate(lines[1:], start=2):  # Skip header
        fields = line.split(',')
        try:
            #hello
            person_id = int(fields[0])
            name = fields[1]
            birthday = datetime.datetime.strptime(fields[2], "%d/%m/%Y").date()
            personData[person_id] = (name, birthday)
        except (ValueError, IndexError):
            logger.error(f"Error processing line #{line_num} for ID #{fields[0]}")
    
    return personData

def displayPerson(id, personData):
    """Displays the person's name and birthday."""
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday}")
    else:
        print("No user found with that id")

def main(url):
    logging.basicConfig(filename='errors.log', level=logging.ERROR)
    print(f"Running main with URL = {url}...")

    # Download data
    try:
        csvData = downloadData(url)
    except Exception as e:
        print(e)
        return

    # Process data
    personData = processData(csvData)

    # Interact with user
    while True:
        try:
            user_input = int(input("Enter an ID to lookup (0 or negative to exit): "))
            if user_input <= 0:
                break
            displayPerson(user_input, personData)
        except ValueError:
            print("Please enter a valid integer.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
