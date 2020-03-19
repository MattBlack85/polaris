import csv
import datetime
import re
from datetime import datetime as dt

import tabula

REPORT_1_DATE = '2020-01-21'
WHO_URL = 'https://www.who.int/docs/default-source/coronaviruse/situation-reports/'
EXTRACT_NUMBER_FROM_COUNTRY_REGEX = re.compile(r'^([\w\s\)]+) (\d+)$', re.UNICODE)


class Polaris:

    def _get_pdf_url(self, day: datetime.datetime) -> str:
        report_number = (day - dt.strptime(REPORT_1_DATE, '%Y-%m-%d')).days + 1
        return f'{WHO_URL}{day.date().isoformat().replace("-", "")}-sitrep-{report_number}-covid-19.pdf'

    def _is_interesting_row(self, row: list) -> bool:
        try:
            if not row[5] or not row[6]:
                return False
            else:
                return True

        except IndexError:
            return False

    def _sanitize_row(self, row: list) -> list:
        new_row = []
        country = None
        try:
            int(row[0][-1:])
            if match := EXTRACT_NUMBER_FROM_COUNTRY_REGEX.search(row[0]):  # NOQA
                try:
                    country = match.group(1)
                except AttributeError:
                    pass
                total_cases = match.group(2)
        except ValueError:
            # No number no party
            pass

        if country:
            return [country, total_cases, row[2], row[3], row[4]]
        else:
            return [row[0], row[1], row[2], row[3], row[4]]

    def _clean_csv(self, name: str) -> None:
        new_lines = []
        with open(f'{name}.csv', 'r+', newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar='|')
            writer = csv.writer(csvfile, quotechar='|')
            for row in reader:
                if self._is_interesting_row(row):
                    new_row = self._sanitize_row(row)
                    print('ROW', row)
                    new_row.append(name)
                    new_lines.append(new_row)

            # Reset the file
            csvfile.seek(0)
            writer.writerows(new_lines)
            csvfile.truncate()

    def get_data(self, date: str, page: list = [3, 4, 5, 6]) -> None:
        day = dt.strptime(date, '%Y-%m-%d')
        url = self._get_pdf_url(day)
        print('PDF URL:', url)
        tabula.convert_into(url, f'{day.date()}.csv', output_format='csv', pages=page)
        self._clean_csv(str(day.date()))
