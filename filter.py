import datetime

class Filter():
    current_filter = {
        "CityId" : "",
        "ClinicId": "",
        "ServiceId": "",
        "DoctorId": "",
        "DateFrom": "",
        "DateTo": "",
    }
    def __init__(self):
        now = datetime.datetime.now()
        self.current_filter["DateFrom"] = "{}-{}-{}".format(now.day, now.month,
            now.year)
        self.current_filter["DateTo"] = self.current_filter["DateFrom"]
    def AddFilter(self, **kwargs):
        if kwargs is not None:
            for key, value in kwargs.items():
                if key in self.current_filter.keys():
                    self.current_filter[key] = value
        return self
    def as_dict(self):
        return self.current_filter
