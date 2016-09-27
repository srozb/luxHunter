import requests, re, datetime

class Target():
    hostname = "portalpacjenta.luxmed.pl"
    def __init__(self):
        self.RequestVerificationToken = ""
        self.jar = requests.cookies.RequestsCookieJar()
        self.jar.set('LXCookieMonit', '1')
    def _getCSRFToken(self, buf):
        regex = r"\"__RequestVerificationToken\"\s+type=\"hidden\"\s+value=\"([0-9a-zA-Z-_]+)\""
        s = re.search(regex, buf)
        if not s:
            return ""
        return s.groups()[0]
    def _SetCSRFToken(self, buf):
        self.RequestVerificationToken = self._getCSRFToken(buf)
    def _UpdateJar(self, cookies):
        self.jar.update(cookies)
    def _DoPOST(self, url, data):
        r = requests.post(url, data, cookies=self.jar, allow_redirects=False)
        self._UpdateJar(r.cookies)
        return r
    def _DoGET(self, url):
        r = requests.get(url, cookies=self.jar)
        self._UpdateJar(r.cookies)
        return r
    def _BuildURL(self, endpoint, scheme="https"):
        urls = {
            "login": "/PatientPortal/Account/LogIn",
            "afterlogin": "/PatientPortal/",
            "find": "/PatientPortal/Reservations/Reservation/Find",
        }
        return "{}://{}{}".format(scheme, self.hostname, urls[endpoint])
    def Login(self, login, password):
        if not (login and password):
            raise Exception("Trzeba podac odpowiednie kredensy!")
        url = self._BuildURL("login")
        params = {
            "Login": login,
            "Password": password
        }
        resp = self._DoPOST(url, params)
        url = self._BuildURL("afterlogin")
        resp = self._DoGET(url)
        self._SetCSRFToken(resp.text)
    def Find(self, filter):
        url = self._BuildURL("find")
        filter = filter.as_dict()
        default_params = {
            "IsFromStartPage": "True",
            "SearchFirstFree": "True",
            "__RequestVerificationToken": self.RequestVerificationToken,
            "TimeOption": "Any",
        }
        params = {**default_params, **filter}
        resp = self._DoPOST(url, params)
        self._SetCSRFToken(resp.text)
        return resp.text
