import sys      # system stuff [like argv]
import pickle   # for serialization/deserialization of objects to files
import httplib  # for web requests
import urllib   # for encoding
import re       # regular expressions
import math     # math lib
import random   # ramdon

from datetime import date #date stuff

#references
#python docs: http://docs.python.org/
#built-in functions: http://docs.python.org/library/functions.html
#string formatting: http://docs.python.org/library/stdtypes.html#string-formatting
#brief tour of stdlib: http://docs.python.org/tutorial/stdlib.html

class MyClass:
    #what follows is a documentation string
    #can be accessed via MyClass.__doc__
    """A test class

    Doesn't do too much.
    """
    def __init__(self): #class constructor
        self.foo = 'foo'
        self.bar = 'bar'
    def method(self, n):
        print n

#basic stuff
def main():
    print "Writing to stdio" #writing to stdio

    #number of arguments
    print 'Number of script arguments: %s' % len(sys.argv)
    print 'argv[0]: %s' %(sys.argv[0])

    #pass when statement is required
    if True: pass

    #make a list
    aList = [3, 'foo', 5.4]
    aList.append('10')
    print aList
    print 'aList[1]: %s' %(aList[1])
    print list('abcde') #the builtin function list can make a list from anything iterable
    print list((2, 3.3, 'abc')) #make a list from a tuple

    #make a dictionary
    aDict = { 'foo': 3, 'bar': 9, 'test': 'foobar' }
    print aDict
    print 'aDict["foo"]: %s' %(aDict['foo'])

    #use a class
    print MyClass.__doc__
    c = MyClass()
    print 'c.Foo: %s, c.Bar, %s' %(c.foo, c.bar)
    c.method(25)

    #use a regular expression
    print re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
    print re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat')

    #math stuff
    print math.cos(math.pi / 4.0)
    print math.log(1024, 2)

    #datetime stuff
    now = date.today()
    print now, now.day, now.month, now.year
    birthday = date(1979, 10, 30)
    age = now - birthday
    print "%s days old" % age.days

    serializationDeserialization()
    makeHttpGetRequest('www.google.com', '/') #will be 200/OK
    makeHttpGetRequest('finance.yahoo.com', '/d/quotes.csv?s=SBUX&f=snd1l1yr') #will issue 301
    makeHttpGetRequest('www.foo.com', '/should/return/404') #will issue 404
    params = { 'spam': 0, 'eggs': 1, 'bacon': 2 }
    makeHttpPostRequest('echoposter.appspot.com', '/', params)

    functionalTechniques()

#demonstrate object serialization / deserialization to a file
def serializationDeserialization():
    #define a list across multiple lines
    myList = [
        [2, 4], [3],
        [4]
    ]
    #open a temp file for binary writing
    #the + truncates the file
    with open('temp.dat', 'w+b') as f:
        pickle.dump(myList, f, pickle.HIGHEST_PROTOCOL) #dump the object to the file

    #read it back in
    with open('temp.dat', 'rb') as f:
        foo = pickle.load(f) # deserialize from the file
    print foo

#demonstrate making an http GET request
def makeHttpGetRequest(host, uri):
    conn = httplib.HTTPConnection(host)
    conn.request('GET', uri)
    processHttpResponse(conn)
    conn.close()

#demonstrate making an http POST request
def makeHttpPostRequest(host, uri, params):
    encodedParams = urllib.urlencode(params) #URL encode the parameters
    conn = httplib.HTTPConnection(host)
    headers = { 'Content-type': 'application/x-www-form-urlencoded',
                'Accept': 'text/plain' }
    conn.request('POST', uri, encodedParams, headers)
    processHttpResponse(conn)
    conn.close()

#process an http response
def processHttpResponse(conn):
    # get the response
    response = conn.getresponse()
    if response.status == 301:
        print "Status was redirect to %s" %(response.getheader("Location"))
    elif response.status != 200:
        print "Status wasn't 200/OK: Status: %d, Message: %s" %(response.status, response.reason)
    else:
        print "First 50 characters of response: %s" %(str(response.read())[0:50])

#for the filter function, determines if the parameter is even
def isEven(x):
    return x % 2 == 0
#for the map function, computes the square of the parameter
def computeSquare(x):
    return x**2
#using more than one sequence
def add(x,y):
    return x+y
#for the reduce function
def exponential(x,y):
    return x*y

#demonstrate functional programming techniques
def functionalTechniques():
    print "IsEven range(20): %s" % filter(isEven, range(20))
    print "Squares to 10: %s" % map(computeSquare, range(10))
    print "Add [1,2,3] to [4,5,6]: %s" % map(add, range(1,4), range(4,7))
    print "Exponential(range(5)): %s" % reduce(exponential, range(1,6))
                                    
if __name__ == "__main__":
    main()
