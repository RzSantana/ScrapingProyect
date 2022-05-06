# Library's imports
import time  # Import for stop time
import sys 

import requests  # Import libraries for scraping
from bs4 import BeautifulSoup 

sys.path.append("database")
import connect # Import file that connect to database


# Url's
url = 'https://www.casadellibro.com'  # Url of website
urlCategory = 'https://www.casadellibro.com/libros/autoayuda-y-espiritualidad/autoayuda/102001000'  # Url of category in website
urlPage = urlCategory  # Url of website with the pages

# Function for get the data of website
def getData():
    result = requests.get(urlPage)
    soup = BeautifulSoup(result.text, 'lxml')
    return soup

# Function to get the last page of a category.
def getLastPage():
    pagesOfCategory = getData().find('nav', role="navigation")
    pages = pagesOfCategory.findAll('button', class_='v-pagination__item')
    pageMax = int(pages[pages.__len__()-1].text)
    return pageMax

# Function for get the block of all books a category
def getAllBooks():
    blockBooks = getData().find('div', class_='results')
    return blockBooks

# Function for get the number of books in a pages
def getNumBooks():
    books = getAllBooks().findAll('div', class_='row align-end')
    return books

print('Program ON')

# Query to execute in the database for create the table, if not exists
connect.executeSQL('CREATE TABLE IF NOT EXISTS test3 ('
                   'id INT NOT NULL AUTO_INCREMENT, '
                   'urlBook VARCHAR(255) NOT NULL, '
                   'title VARCHAR(255) NOT NULL, '
                   'description TEXT NOT NULL, '
                   'stars INT NOT NULL, '
                   'cover VARCHAR(255) NOT NULL, '
                   'tecnicalSheet TEXT NOT NULL, '
                   'urlAuthor VARCHAR(255) NOT NULL, '
                   'author VARCHAR(255) NOT NULL, '
                   'descriptionAuthor TEXT NOT NULL, '
                   'starsAuthor INT NOT NULL, '
                   'imgAuthor VARCHAR(255) NOT NULL, '
                   'PRIMARY KEY (`id`) '
                   ') ENGINE = InnoDB; ')

# Loop for all pages of a category ( p == page )
# for p in range(1, 20):  # Line of test code
for p in range(1, getLastPage()):

    # Printing the pages
    print('Page: ' + str(p))

    # Add page to url
    urlPage = urlCategory + '/p' + str(p)

    # Getting data of new url
    data = getData()

    # Getting name of the category if it is in page one
    if p == 1:
        category = data.find('div', id='h1-seo').get_text(strip=True)

    # Loop for get data of every the books ( b == book )
    for b in range(0, getNumBooks().__len__()):

        # Data of book
        try:
            book = getAllBooks().find('div', index=str(b))
            data = book.find('div', class_='row row--dense')
            data.findAll('div', class_='col')
        except:
            time.sleep(5)  # Waiting time for the web page to load
            book = getAllBooks().find('div', index=str(b))
            data = book.find('div', class_='row row--dense')
            data.findAll('div', class_='col')

        # Getting url of book, if it has
        try:
            urlBook = book.find('a', class_='title').get('href')
            urlBook = url + urlBook
        except:
            urlBook = 'None'

        # Getting title of book, if it has
        try:
            titleBook = book.find('a', class_='title').get_text(strip=True)
        except:
            titleBook = 'None'

        # Getting author of book, if it has
        try:
            authorBook = book.find('a', class_='author').get_text(strip=True)
        except:
            authorBook = 'None'

        # Getting data of author, if it has
        try:
            urlAuthor = book.find('a', class_='author').get('href')
            urlAuthor = url + urlAuthor
            urlPage = urlAuthor

            dataAuthor = getData()
            boxDataAuthor = dataAuthor.find('div', idcomponente='75822')

            # Obtener imagen del author
            try:
                imgAuthor = boxDataAuthor.find('img', class_='cdl-img active').get('src')
            except:
                imgAuthor = 'None'

            # Obtener descripción del author
            try:
                descriptionAuthor = boxDataAuthor.find('p').get_text()
            except:
                descriptionAuthor = 'None'

            # Obtener stars del author
            try:
                starsAuthor = boxDataAuthor.find('span', class_='title').get_text(strip=True)
            except:
                starsAuthor = '0'

            # Set the category page url again
            urlPage = urlCategory + '/p' + str(p)
        except:
            dataAuthor = 'None'
            imgAuthor = 'None'
            descriptionAuthor = 'None'
            starsAuthor = '0'

        # Getting description of book, if it has
        try:
            descriptionBook = book.find('div', class_='short').get_text(strip=True, separator=' ')
        except:
            descriptionBook = 'None'

        # Getting stars of book, if it has
        try:
            starsBook = book.find('span', class_='text-caption').get_text()
        except:
            starsBook = '0'

        # Getting image cover of book, if it has
        try:
            imgBook = book.find('img', class_='cdl-img').get('data-src')

            # Change the small image to big image
            imgBook = imgBook.replace("/t1/", "/t7/")
        except:
            imgBook = 'None'

        # Getting technical sheet of book, if it has
        try:
            urlPage = urlBook
            dataInBook = getData()

            dataProduct = dataInBook.find('div', class_='dataproduct')
            boxTechnicalSheetBook = dataProduct.findAll('div', class_='row text-body-2 no-gutters')
            technicalSheetBook = ''

            # Loop for getting all data from technical sheet
            for tS in range(0, boxTechnicalSheetBook.__len__()):
                technicalSheetBook = technicalSheetBook + boxTechnicalSheetBook[tS].get_text(strip=True, separator='') + '; '

            # Set the category page url again
            urlPage = urlCategory + '/p' + str(p)
        except:
            technicalSheetBook = 'None'

        # Query for insert the books in de tabla
        query = 'INSERT INTO test3 (id, urlBook, title, description, stars, cover, tecnicalSheet, urlAuthor, author, descriptionAuthor, starsAuthor, imgAuthor) VALUES (NULL,"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(urlBook.replace('"', ''),titleBook.replace('"', ''),descriptionBook.replace('"', ''),starsBook.replace('"', ''),imgBook.replace('"', ''),technicalSheetBook.replace('"', ''),urlAuthor.replace('"', ''),authorBook.replace('"', ''),descriptionAuthor.replace('"', ''),starsAuthor.replace('"', ''),imgAuthor.replace('"', ''),)

        # Execute the query
        connect.executeSQL(query)

    # Commit the query in the database
    connect.connexion.commit()


# Print that the query has been made
print('Finish, correct insertion')

# Close the database connection.
connect.connexionClose()
