import httplib

httpServ = httplib.HTTPConnection("127.0.0.1", 80)
httpServ.connect()

httpServ.request('GET', "/test.html")

response = httpServ.getresponse()
if response.status == httplib.OK:
    print "Output from HTML request"
    printText (response.read())

httpServ.request('GET', '/cgi_form.cgi?name=Brad&quote=Testing.')

response = httpServ.getresponse()
if response.status == httplib.OK:
    print "Output from CGI request"
    printText (response.read())

httpServ.close()