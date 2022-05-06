
# Version 0.1


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
                   'author VARCHAR(255) NOT NULL, '
                   'PRIMARY KEY (`id`) '
                   ') ENGINE = InnoDB; ')

while run is True:    
    # Open browser and website
    driver.get(website)
    print('> [Run launch]')

    
    # Store the id of the primary window
    original_window = driver.current_window_handle 

    time.sleep(3)

    
    # Accept cookies
    try:
        driver.find_element(By.ID, 'sp-cc-accept').click()
        print('> [Cookies aceptadas]')
    except:
        print('> [Cookies no encontradas]')
        pass
    

    time.sleep(3)
    actualPage = driver.find_element(By.CLASS_NAME, 's-pagination-selected').text
    print(f'> [Pagina: {actualPage}]')


    # Get books
    containerBooks = driver.find_element(By.CLASS_NAME, 's-main-slot')
    arrayBooks = containerBooks.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]') # Contiene todos los libros

    if len(arrayBooks) > 0:
        print('> [Libros capturados]')
        print(f'> [Total: {len(arrayBooks)}]')
    else:
        print('> [Error: Libros no encontrados]')

            
    # Entrance to the books
    for b in range(0, len(arrayBooks)-1):
        title = arrayBooks[b].find_element(By.TAG_NAME, 'h2')  
        urlBook = title.find_element(By.TAG_NAME, 'a').get_attribute('href') # Get the Url
        

        # Open new Window in tab
        driver.switch_to.new_window('tab')
        driver.get(urlBook)

        try:
           imgBook = driver.find_element(By.CLASS_NAME, 'frontImage').get_attribute('src')
        except:
            imgBook = 'None'

        try:
           titleBook = driver.find_element(By.ID, 'productTitle').text
        except:
            titleBook = 'None'

        try:
            author = driver.find_element(By.CLASS_NAME, 'contributorNameID').text
        except:
            author = 'None'

        try:
            descriptionBook = driver.find_element(By.ID, 'bookDescription_feature_div').text
        except:
            descriptionBook = 'None'

        try:
            starsBook = driver.find_element(By.ID, 'acrCustomerReviewText').text
            starsBook = starsBook.replace('.', '')
            starsBook = starsBook.replace('valoraciones', '')
            print(starsBook)
        except:
            starsBook = 0

        try:
            precio = 0
            precio = driver.find_element(By.ID, 'price').text
            precio = precio.replace('€', '')
            precio = precio.replace(',', '.')
            precio = float(precio)
            print(precio)
            
            if precio == 0:
                precio = driver.find_element(By.ID, 'a-autoid-7-announce')
                precio = precio.find_element(By.CLASS_NAME, 'a-color-secondary').text
                precio = float(precio)
                print(precio)
        except:
            precio = 0
        
        try:
            authorBook = driver.find_element(By.CLASS_NAME, 'contributorNameID').text
        except:
            authorBook = 'None'
        
        print(f'> [Libro Completado {b}]')
        
        # Query for insert the books in de tabla
        query = 'INSERT INTO test (id, urlBook, title, description, price, stars, cover, author) VALUES (NULL,"{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(urlBook.replace('"', ''), titleBook.replace('"', ''), descriptionBook.replace('"', ''), precio, starsBook, imgBook.replace('"', ''), authorBook.replace('"', ''))
        connect.executeSQL(query) # Execute the query
        connect.commitSQL() # Commit the query in the database
        print(f'> [✅ Commit]')


        # Close new Window in tab and chage de window
        driver.close()
        driver.switch_to.window(original_window)
    
   
    endPage = driver.find_element(By.CLASS_NAME, 's-pagination-disabled').text
    if endPage == 'Siguiente':
        run = False
    else:
        urlNextPage = driver.find_element(By.CLASS_NAME, 's-pagination-next').get_attribute('href') # Get the Url
        website = urlNextPage
    
connect.connexionClose()
print('> [Programa Finalizado]')