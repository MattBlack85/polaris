import csv
import datetime
from datetime import datetime as dt

import tabula

REPORT_1_DATE = '2020-01-21'
WHO_URL = 'https://www.who.int/docs/default-source/coronaviruse/situation-reports/'


class Polaris:

    def _get_yesterday_pdf_url(self, today_datetime: datetime.datetime) -> str:
        yesterday_report_number = (today_datetime - dt.strptime(REPORT_1_DATE, '%Y-%m-%d')).days
        return f'{WHO_URL}{(today_datetime - datetime.timedelta(days=1)).date().isoformat().replace("-", "")}-sitrep-{yesterday_report_number}-covid-19.pdf'

    def _is_interesting_row(self, row: list) -> bool:
        try:
            if row[1] in ('', None):
                return False

            try:
                int(row[1])
                return True
            except ValueError:
                return False

        except IndexError:
            return False

    def _sanitize_row(self, row: list) -> list:
        if not row[2]:
            row.pop(2)

        return row

    def _clean_csv(self, name: str) -> None:
        new_lines = []
        with open(f'{name}.csv', 'r+', newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar='|')
            writer = csv.writer(csvfile, quotechar='|')
            for row in reader:
                if self._is_interesting_row(row):
                    self._sanitize_row(row)
                    new_lines.append(row)

            # Reset the file
            csvfile.seek(0)
            writer.writerows(new_lines)
            csvfile.truncate()

    def get_latest_csv_data(self) -> None:
        today_datetime = dt.today()
        today = dt.date(today_datetime).isoformat()
        url = self._get_yesterday_pdf_url(today_datetime)
        tabula.convert_into(url, f'{today}.csv', output_format='csv', pages='all')
        self._clean_csv(today)
