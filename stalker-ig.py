from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyinputplus as pyip
import requests
from pathlib import Path
import os

email = pyip.inputEmail('\nEmail: ')
password = pyip.inputPassword('Password: ')

user_to_search = input('\nWhat user to search for? ')

folder = Path(user_to_search + 'IGphotos')
os.makedirs(folder)

driver = webdriver.Chrome()

driver.get('https://instagram.com/')

driver.set_window_position(0, 0)
driver.maximize_window()

sleep(3)

login = driver.find_element_by_xpath("//input[@name='username']") 

passwd = driver.find_element_by_xpath("//input[@name='password']") 

login.send_keys(email)
passwd.send_keys(password)

login.submit()

sleep(3)

driver.get(f'https://instagram.com/{user_to_search}')

# body = driver.find_element_by_tag_name('body')
# for _ in range(100):
# 	body.send_keys(Keys.END)	
# 	sleep(2)

imgs = driver.find_elements_by_tag_name('img')[:-2]

src_imgs = [img.get_attribute("src") for img in imgs]

print()
for i, src_img in enumerate(src_imgs, 1):
	r = requests.get(src_img)
	with open(folder / str(i), 'wb') as img:
		for chunk in r.iter_content(chunk_size=1024*1024):
			if chunk:	
				img.write(chunk)
	
		print(f'Downloaded {folder / str(i)}...')

driver.quit()

