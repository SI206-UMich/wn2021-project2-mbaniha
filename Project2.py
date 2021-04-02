from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    titles = []
    authors = []
    search = open(filename)
    soup = BeautifulSoup(search, 'html.parser')
    search.close()
    
    table = soup.find_all('tr')
    for element in table:
        title = element.find('a', {'class':'bookTitle'})
        titles.append(title.text.strip())
        author = element.find('a', {'class':'authorName'})
        authors.append(author.text.strip())
    
    return list(zip(titles, authors))
    
    


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser') #VSCode warning: suggested adding features for consistency

    title_links = soup.find_all('a', {'class':'bookTitle'}, limit = 10)
    titles = ["https://www.goodreads.com" + title['href'] for title in title_links]
    return titles


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    data = r.content
    soup = BeautifulSoup(data, 'html.parser')

    title = soup.find('h1').text.strip()
    author = soup.find('a', {'class':'authorName'}).text.strip()
    pages = soup.find('span', itemprop='numberOfPages').text.strip()
    numPages = int(re.findall(r'[0-9]+', pages)[0])
    
    return (title, author, numPages)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    bestList = []
    bestFile = open(filepath,'r',encoding='UTF-8')
    soup = BeautifulSoup(bestFile, 'html.parser')
    bestFile.close()
    
    divs = soup.find_all('div', {'class':'category clearFix'})
    for div in divs:
        category = div.find('h4').text.strip()
        name = div.find('img')['alt'].strip()
        link = div.find('a')['href']
        summary = (category,name,link)
        bestList.append(summary)
    
    return bestList



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline='') as csvfile:
        field_names = ['Book Title', 'Author Name']
        writer = csv.writer(csvfile)
        writer.writerow(field_names)
        for book in data:
            writer.writerow(book)
    #No need to close file when using with statement



def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    
    ecFile = open(filepath, 'r', encoding='UTF-8')
    soup = BeautifulSoup(ecFile, 'html.parser')
    ecFile.close()

    description = soup.find('div', {'id':'description'}).text.strip()

    regex = '([A-Z][a-z][a-z]+(?=[ \t][A-Z])(?:[ \t][A-Z][a-z]+)+)'
    # regex considering all 3 requirements of a Named Entity
    named = re.findall(regex, description)
    return named
    

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)
        # check that the variable you saved after calling the function is a list
        self.assertTrue(isinstance(titles, list))
        # check that each item in the list is a tuple
        self.assertTrue(all(isinstance(t, tuple) for t in titles))
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        first = ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling')
        self.assertEqual(titles[0], first)
        # check that the last title is correct (open search_results.htm and find it)
        last = ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling')
        self.assertEqual(titles[-1], last)

        

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertTrue(isinstance(TestCases.search_urls, list))
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        self.assertTrue(all(isinstance(u, str) for u in TestCases.search_urls))
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        sub_url = "https://www.goodreads.com/book/show/"
        self.assertTrue(all((sub_url in u) for u in TestCases.search_urls))


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
        # check that each item in the list is a tuple
        self.assertTrue(all(isinstance(s, tuple) for s in summaries))
        # check that each tuple has 3 elements
        self.assertTrue(all((len(s) == 3) for s in summaries))
        # check that the first two elements in the tuple are string
        self.assertTrue(all(isinstance(s[0], str) for s in summaries))
        self.assertTrue(all(isinstance(s[1], str) for s in summaries))
        # check that the third element in the tuple, i.e. pages is an int
        self.assertTrue(all(isinstance(s[2], int) for s in summaries))
        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(best), 20)
        # assert each item in the list of best books is a tuple
        self.assertTrue(all(isinstance(b, tuple) for b in best))
        # check that each tuple has a length of 3
        self.assertTrue(all((len(b) == 3) for b in best))
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        csv_lines = []
        with open('test.csv', 'r') as csvfile:
            for line in csv.reader(csvfile):
                csv_lines.append(line)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ["Book Title","Author Name"])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    #With the page in extra_credit.htm, a total of 10 distinct Named Entities should be found

    unittest.main(verbosity=2)
    
    #print statements to help during implementation and testing
    #print(get_titles_from_search_results('search_results.htm'))
    #print(get_search_links())
    #print(get_book_summary('https://www.goodreads.com/book/show/52578297-the-midnight-library?from_choice=true'))
    #print(summarize_best_books("best_books_2020.htm"))




