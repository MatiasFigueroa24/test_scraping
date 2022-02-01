from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import unittest
import json


class Items(unittest.TestCase):
    def setUp(self):
        self.website_movies = 'https://www.starz.com/ar/es/movies'
        self.website_series = 'https://www.starz.com/ar/es/series'
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


# Obtiene todas las peliculas
    def test_all_movies_series(self):
        self.driver.get(self.website_movies)
        time.sleep(5)
        self.driver.find_element(By.CLASS_NAME,"view-all").click()
        self.list_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[@class='font-icon icon-stz-list']")))
        self.list_button.click()
        time.sleep(5)
        #obtengo los titulos de las peliculas
        title_movies = self.driver.find_elements(By.XPATH,"//p[@class='title']")
        #obtengo el año de las peliculas
        age = self.driver.find_elements(By.XPATH,"//p[@class='text-body']/span[3]")
        #obtengo el año de las peliculas
        duration = self.driver.find_elements(By.XPATH,"//p[@class='text-body']/span[1]")
        #obtengo los links de las peliculas
        list_link = self.driver.find_elements(By.CLASS_NAME,"list-link")
        links_href = [link_id.get_attribute('href') for link_id in list_link]

        data_movies = {}
        data_movies['movies'] = []
        #seteo los valores obtenidos en el diccionarios
        for i in title_movies:
                data_movies['movies'].append({
                    'title': i.text
                })

        count = 0
        for ages in age:
            data_movies['movies'][count].update({
                'age': ages.text
            })
            count += 1

        count = 0
        for durations in duration:
            data_movies['movies'][count].update({
                'durations': durations.text + ' min'
            })
            count += 1

        count = 0
        for link in links_href:
            #Abre el link y obtiene la sinopsis de cada pelicula
            self.driver.get(link)
            time.sleep(10)
            sinopsis = self.driver.find_element(By.XPATH,"//p[@lines='3']")

            data_movies['movies'][count].update({
                'link': link,
                'sinopsis': sinopsis.text
            })
            count += 1
        with open('test Scraping movies.json','w') as f:
            json.dump(data_movies,f)
        self.driver.quit()

    def test_all_series(self):
    # obtiene las series
        self.driver.get(self.website_series)
        time.sleep(5)
        self.driver.find_element(By.CLASS_NAME, "view-all").click()
        self.list_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='font-icon icon-stz-list']")))
        self.list_button.click()
        time.sleep(5)
        title_series = self.driver.find_elements(By.XPATH,"//p[@class='title']")
        episodes = self.driver.find_elements(By.XPATH, "//p[@class='text-body']/span[3]")
        list_link = self.driver.find_elements(By.CLASS_NAME, "list-link")
        links_href = [link_id.get_attribute('href') for link_id in list_link]

        data_series = {}
        data_series['series'] = []

        for i in title_series:
            data_series['series'].append({
                'title': i.text
            })

        count = 0
        for item in episodes:
            data_series['series'][count].update({
                'episodes': item.text
            })
            count += 1

        count = 0
        for link in links_href:
            self.driver.get(link)
            time.sleep(10)
            sinopsis = self.driver.find_element(By.XPATH,"//p[@lines='3']")

            data_series['series'][count].update({
                'sinopsis': sinopsis.text
            })
            count += 1
        with open('test Scraping series.json','w') as f:
            json.dump(data_series,f)
        self.driver.quit()



if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

