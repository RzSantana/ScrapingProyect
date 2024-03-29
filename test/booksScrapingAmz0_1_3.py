
# Version 0.1.3


# Library's imports
import time # Import for stop time
import sys


from selenium import webdriver # Import libraries for scraping
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

sys.path.append("database")
import connect # Import file that connect to database
    


# Location of the file for the connection with the browser
path = Service('utils/geckodriver.exe')

# Url website
website = 'https://www.amazon.es/s?i=stripbooks&bbn=902718031&rh=n%3A599364031%2Cn%3A902716031%2Cn%3A902718031%2Cp_n_availability%3A831278031%2Cp_n_binding_browse-bin%3A831435031%7C831436031&dc&fs=true&qid=1651600699&rnid=831428031&ref=sr_pg_1'

driver = webdriver.Firefox(service=path)

execute = input('> [Desea ejecutar el programa: s/n] ')
if execute == 's':
    run = True
elif execute == 'n':
    run = False
else:
    run = False
    print('> [Error: Dato invalido]')

# Query to execute in the database for create the table, if not exists
connect.executeSQL('CREATE TABLE IF NOT EXISTS test ('
                   'id INT NOT NULL AUTO_INCREMENT, '
                   'urlBook VARCHAR(255) NOT NULL, '
                   'title VARCHAR(255) NOT NULL, '
                   'description TEXT NOT NULL, '
                   'price FLOAT NOT NULL, '
                   'stars INT NOT NULL, '
                   'cover VARCHAR(255) NOT NULL, '
                   'tecnicalSheet TEXT NOT NULL, '
                   'urlAuthor VARCHAR(255) NOT NULL, '
                   'author VARCHAR(255) NOT NULL, '
                   'descriptionAuthor TEXT NOT NULL, '
                   'imgAuthor VARCHAR(255) NOT NULL, '
                   'PRIMARY KEY (`id`) '
                   ') ENGINE = InnoDB; ')

while run is True:    
    # Open browser and website
    driver.get(website)
    categorie_window = driver.current_window_handle # Store the id of the primary window
    print('> [Run launch]') 

    time.sleep(3)

    
    # Accept cookies
    try:
        driver.find_element(By.ID, 'sp-cc-accept').click()
        print('> [Cookies aceptadas]')
    except:
        print('> [Cookies no encontradas]')
        pass
    

    time.sleep(3)

    # View actual page
    actualPage = driver.find_element(By.CLASS_NAME, 's-pagination-selected').text # Captura el nuemo de la pagina activa
    print(f'> [Pagina: {actualPage}]')


    # Get books
    containerBooks = driver.find_element(By.CLASS_NAME, 's-main-slot')
    arrayBooks = containerBooks.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]') # Array con todos los libros

    if len(arrayBooks) > 0:
        print('> [Libros capturados]')
        print(f'> [Total: {len(arrayBooks)}]')
    else:
        print('> [Error: Libros no encontrados]')

            
    # Get into de books
    for b in range(0, len(arrayBooks)):
        title = arrayBooks[b].find_element(By.TAG_NAME, 'h2')  
        urlBook = title.find_element(By.TAG_NAME, 'a').get_attribute('href') # Coge la url del libro
        

        # Open new Window in tab
        driver.switch_to.new_window('tab')
        driver.get(urlBook)        
        book_window = driver.current_window_handle # Store the id of the primary window


        # Book image capture
        try:
            imgBook = driver.find_element(By.CLASS_NAME, 'frontImage').get_attribute('src')
        except:
            imgBook = 'None'
            pass


        # Book title capture
        try:
            titleBook = driver.find_element(By.ID, 'productTitle').text
        except:
            titleBook = 'None'
            pass


        # Book description capture
        try:
            descriptionBook = driver.find_element(By.ID, 'editorialReviews_feature_div').text
        except:
            descriptionBook = 'None'
            pass


        # Book stars capture
        try:
            starsBook = driver.find_element(By.ID, 'acrCustomerReviewText').text
            starsBook = starsBook.replace('.', '')
            starsBook = starsBook.replace('valoraciones', '')
        except:
            starsBook = 0
            pass


        # Book price capture
        try:
            price = driver.find_element(By.ID, 'price').text
            price = price.replace('€', '')
            price = price.replace(',', '.')
            price = float(price)
        except:
            price = 0
            pass
        
        # Book product details capture
        try:
            containerProductDetails = driver.find_element(By.ID, 'detailBullets_feature_div')
            arrayDetails = containerProductDetails.find_elements(By.TAG_NAME, 'li') # Array con todos los datos
            
            productDetails = ''
            for n in range(0, len(arrayDetails)):
                txt = arrayDetails[n].text
                productDetails = productDetails + txt + '; ' # Estructura de los detalles del libro
        except:
            productDetails = 'None'
            pass


        # Book description capture
        try:  
            containerDescriptionAuthor = driver.find_element(By.ID, 'editorialReviews_feature_div')
            descriptionAuthor = containerDescriptionAuthor.find_element(By.XPATH, 'div[2]/div/span').text
        except:
            descriptionAuthor = 'None'
            pass


        # Book author data capture
        try:
            containerAuthor = driver.find_element(By.ID, 'authorFollow_feature_div')
            linkAuthor = driver.find_element(By.CLASS_NAME, 'authorNameLink').get_attribute('href')
            
            
            # Open new Window in tab
            driver.switch_to.new_window('tab')
            driver.get(linkAuthor)


            # Book author capture
            try:
                containerAuthorBook = driver.find_element(By.ID, 'authorName')
                authorBook = driver.find_element(By.TAG_NAME, 'h1').text
            except:
                authorBook = 'None'


            # Book image capture
            try:        
                containerImgAuthor = driver.find_element(By.ID, 'authorImage')
                imgAuthor = driver.find_element(By.CLASS_NAME, 'a-dynamic-image ').get_attribute('src')
            except:
                imgAuthor = 'None'
        except:
            pass

        # Close new Window in tab and chage de window
        driver.close()
        driver.switch_to.window(book_window)            

        print(f'> [Libro Completado {b}]')
        

        # Query for insert the books in de tabla
        query = 'INSERT INTO test (id, urlBook, title, description, price, stars, cover, tecnicalSheet, urlAuthor, author, descriptionAuthor, imgAuthor) VALUES (NULL,"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(urlBook.replace('"', ''), titleBook.replace('"', ''), descriptionBook.replace('"', ''), price, starsBook, imgBook.replace('"', ''), productDetails, linkAuthor.replace('"', ''), authorBook.replace('"', ''), descriptionAuthor.replace('"', ''), imgAuthor.replace('"', ''))
        connect.executeSQL(query) # Execute the query
        connect.commitSQL() # Commit the query in the database
        print(f'> [✅ Commit]')


        # Close new Window in tab and chage de window
        driver.close()
        driver.switch_to.window(categorie_window)
    
   
    endPage = driver.find_element(By.CLASS_NAME, 's-pagination-disabled').text
    if endPage == 'Siguiente':
        run = False
    else:
        urlNextPage = driver.find_element(By.CLASS_NAME, 's-pagination-next').get_attribute('href') # Get the Url
        website = urlNextPage
    
connect.connexionClose()
print('> [Programa Finalizado]')