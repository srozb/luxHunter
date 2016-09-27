#!/usr/bin/env python3

from target import Target
from filter import Filter
from reservation import Reservation

login = ""
password = ""

LX = Target()
R = Reservation()
CustFilt = Filter().AddFilter(CityId=1).AddFilter(ClinicId=19).AddFilter(ServiceId=4502)

LX.Login(login, password)
results = LX.Find(CustFilt)
R.ParseHtml(results)
R.PrintAsTable()
