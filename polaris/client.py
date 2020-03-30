import csv
import datetime
from datetime import datetime as dt

import tabula

REPORT_1_DATE = '2020-01-21'
WHO_URL = 'https://www.who.int/docs/default-source/coronaviruse/situation-reports/'

REPLACE_MAP = {
    'Czechia': 'Czech Republic',
    'The United Kingdom': 'United Kingdom',
    'Curaçao': 'Curacao',
    'Saint Barthélemy': 'Saint Barthelemy',
    'Côte d’Ivoire': 'Cote d’Ivoire',
    'Réunion': 'Reunion',
    'conveyance (Diamond': 'International',
    'Kosovo[1]': 'Kosovo',
    'occupied Palestinian territory': 'Palestine',
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Democratic Republic': "Lao People's Democratic Republic",
    'Iran (Islamic Republic of)': 'Iran',
    '': 'Northern Mariana Islands',
}


class Polaris:

    def _get_pdf_url(self, day: datetime.datetime) -> str:
        report_number = (day - dt.strptime(REPORT_1_DATE, '%Y-%m-%d')).days + 1
        return f'{WHO_URL}{day.date().isoformat().replace("-", "")}-sitrep-{report_number}-covid-19.pdf'

    def _is_interesting_row(self, row: list) -> bool:
        # Check if we expect a number but there is a string
        try:
            if row[1]:
                try:
                    int(row[1])
                except ValueError:
                    return False
        except IndexError:
            return False

        try:
            if not row[5] or not row[6]:
                return False
            else:
                return True

        except IndexError:
            return False

    def _sanitize_row(self, row: list) -> list:
        country = row[0] if '\r' not in row[0] else row[0].replace('\r', ' ')
        if country in REPLACE_MAP:
            country = REPLACE_MAP[country]
        return [country, row[1], row[2], row[3], row[4]]

    def _clean_csv(self, name: str) -> None:
        new_lines = []
        with open(f'{name}.csv', 'r+', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='"')
            writer = csv.writer(csvfile)

            for row in reader:
                row = row[0].split(',')
                if self._is_interesting_row(row):
                    new_row = self._sanitize_row(row)
                    print('ROW', new_row)
                    new_row.append(name)
                    new_lines.append(new_row)

            # Reset the file
            csvfile.seek(0)
            writer.writerows(new_lines)
            csvfile.truncate()

    def get_data(self, date: str, page: list = [2, 3, 4, 5, 6, 7]) -> None:
        day = dt.strptime(date, '%Y-%m-%d')
        url = self._get_pdf_url(day)
        print('PDF URL:', url)
        tabula.convert_into(url, f'{day.date()}.csv', output_format='csv', pages=page)
        self._clean_csv(str(day.date()))
