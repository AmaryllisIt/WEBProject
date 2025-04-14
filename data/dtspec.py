import datetime


class DateSpec:
    """Class object for reconstrucing date"""
    def get_correct_date(self):
        self.date_now = datetime.date.today()
        return '.'.join(reversed(str(self.date_now).split('-')))
    

