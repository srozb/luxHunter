from tabulate import tabulate
from collections import namedtuple
from bs4 import BeautifulSoup
import urllib.parse


res_nt = namedtuple("Reservation", "City CityId Clinic ClinicId Date Doctor \
    DoctorId IsFree RoomId Service ServiceId ReferralRequired TermId")
report_nt = namedtuple("Report", "Date City Clinic Doctor Service")

class Reservation():
    def __init__(self):
        self.avail_res = []
        self.report = []
    def _AddReservation(self, res_tuple, report_tuple):
        self.avail_res.append(res_tuple)
        self.report.append(report_tuple)
    def _URLDecode(self, buf):
        return urllib.parse.unquote(buf)
    def _ParseLink(self, buf):
        data = []
        buf = self._URLDecode(buf)
        buf = "".join(buf.split("?")[1:])
        buf = buf.split("&")
        for i in buf:
            i = "".join(i.split("=")[1:])
            data.append(i)
        return data
    def ParseHtml(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        for link in soup.find_all('a'):
            link = link.get("href")
            #print("Link:{}".format(link))
            if type(link) == str and link.startswith("/PatientPortal/Reservations/Reservation/ReservationConfirmation"):
                data = self._ParseLink(link)
                res_tuple = res_nt(*data)
                report_tuple = report_nt(res_tuple.Date, res_tuple.City,
                    res_tuple.Clinic, res_tuple.Doctor, res_tuple.Service)
                self._AddReservation(res_tuple, report_tuple)
    def PrintAsTable(self):
        print(tabulate(self.report, headers="keys"))
