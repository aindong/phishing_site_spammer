import sys
from http import client
from queue import Queue
from threading import Thread
from urllib.parse import urlparse

from faker import Faker

concurrent = 200


def doWork():
    while True:
        url = q.get()
        status, url, params, data = getStatus(url)
        doSomethingWithResult(status, url, params, data)
        q.task_done()


def getStatus(ourl):
    try:
        fake = Faker()
        password = fake.password(length=10, special_chars=True, digits=True, 
                                 upper_case=True, lower_case=True)
        profile = fake.profile(fields=None, sex=None)

        params = f'account=0&uname={profile["username"]}&pass={password}&fname={fake.first_name()}&mname={fake.last_name()}&lname={fake.last_name()}&m_mname={fake.name_female()}&bday={profile["birthdate"]}&address={profile["address"]}&city={fake.city()}&state={fake.state()}&zip={fake.zipcode()}&phone={fake.phone_number()}&email={profile["mail"]}&epass={password}&challenge1q=Choose+One&ans1=&c_ans1=&challenge2q=Choose+One&ans2=&c_ans2=&namecc=&ncc=&expdate=&securitycode=&submit=Submit'
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}

        url = urlparse(ourl)
        conn = client.HTTPConnection(url.netloc)
        conn.request("POST", "", params, headers)
        res = conn.getresponse()
        conn.close()

        return res.status, ourl, params, res.read()
    except client.HTTPException:
        return "error", ourl, "failed"


def doSomethingWithResult(status, url, params, data):
    print(status, url, params, data)


q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

try:
    for i in range(1000000000):
        url = 'https://maxmiliancosta.com.br/Banco%20De%20Oro/sso/validation.php'
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
