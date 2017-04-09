from HTMLParser import HTMLParser
from urllib import urlopen
from urlparse import urljoin 


class LinkParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for key, value in attrs:
                if key == "href":
                    newUrl = urljoin(self.baseUrl, value)
                    self.links.append(newUrl)

    def getDataAndLinks(self, url):
        self.baseUrl = url
        response = urlopen(url)
        contentType = response.info().type
        if contentType == "text/html":
            #rawData = response.read()
            #strData = rawData.encode("utf-8")
            strData = response.read()
            self.feed(strData)
            return strData, self.links
        else:
            return "", []


def crawler(url, word, maxPages):
    pages = [url]
    counter = 0 
    found = False
    while counter < maxPages and pages and not found:
        counter += 1
        url = pages[0]
        pages = pages[1:]
        try:
            print "%d Visiting: %s" % (counter, url)
            parser = LinkParser()
            data, links = parser.getDataAndLinks(url)
            if data.find(word) > -1:
                found = True
            
            pages = pages + links
            print "Succeeded"
        except Exception as e:
            print "Failed"
            print e

    if found:
        print "The word %s has been found at %s" % (word, url)
    else:
        print "The word %s is not found" % word


if __name__ == "__main__":
    crawler("http://www.google.com", "abcdef", 200) 
