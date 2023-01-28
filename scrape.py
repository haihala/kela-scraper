import argparse
from bs4 import BeautifulSoup
from email_validator import validate_email, EmailNotValidError
import phonenumbers

def main():
    args = parse_args()
    raw_list = parse_html(args.file)
    locations = find_locations(raw_list)
    therapists = filter_therapists(raw_list, args.locations)
    present_output(therapists, args, locations)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog = 'Kela scraper',
        description = 'Scrapes phone numbers and emails off of kela therapeut list',
        epilog = 'Hope this helps'
    )

    parser.add_argument(
        'file',
        help='File to parse from, download the list with all therapists from Kela\'s site.'
    )

    parser.add_argument(
        '--locations',
        required=True,
        nargs='+',
        help='Cities for which you are searching for. Case insensitive.'
    )

    parser.add_argument(
        '--fields',
        nargs='+',
        required=True,
        choices=['email', 'phone'],
        help='Fields to get'
    )

    return parser.parse_args()

def parse_html(file: str):
    with open(file) as handle:
        soup = BeautifulSoup(handle.read(), 'html.parser')
        output = []
        for item in soup.find_all('tr'):
            therapist = []
            for datapoint in item.find_all('span', {'class': 'hakutulosSolu'}):
                therapist.append(datapoint.string)

            if therapist:   # Filter out empty lists
                output.append(therapist)
        return output

def find_locations(raw_list):
    return set(item[0] for item in raw_list)

def filter_therapists(raw_list, locations):
    targets = [location.lower() for location in locations]

    return [
        item
        for item in raw_list
        if item[0].lower() in targets
    ]

def present_output(therapists, args, locations):
    if len(therapists) == 0:
        print(f'No therapists found for {args.locations}')
        print(f'Potential locations: {locations}')
        return

    if 'email' in args.fields:
        present_email(therapists)

    if 'phone' in args.fields:
        present_phone(therapists)


def present_email(therapists):
    actual_emails = []
    for therapist in therapists:
        try:
            validation = validate_email(therapist[2], check_deliverability=True)
            actual_emails.append(validation.email)
        except EmailNotValidError:
            # Sometimes, the field is not an email
            pass
        except AttributeError:
            # Sometimes, the field is just None
            pass

    print(f'Emails of potential therapists ({len(actual_emails)} addresses):')
    present(actual_emails)


def present_phone(therapists):
    actual_numbers = []
    for therapist in therapists:
        if therapist[1] is None:
            continue

        # Some have multiple numbers
        for number in [number.strip() for number in therapist[1].split(',')]:
            try:
                parsed = phonenumbers.parse(number, 'FI')

                if phonenumbers.is_valid_number(parsed):
                    actual_numbers.append(number)

            except phonenumbers.NumberParseException:
                print(number)
                pass


    print(f'Phone numbers of potential therapists ({len(actual_numbers)} numbers):')
    present(actual_numbers)

def present(items):
    print(', '.join(items))
    print()


if __name__ == '__main__':
    main()
