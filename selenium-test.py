from selenium import webdriver
import getpass
from time import sleep
import sqlite3
from datetime import date

#fixed hardcoded PATH
driver = webdriver.Firefox(executable_path=r'C:\geckodriver\geckodriver.exe')
driver.implicitly_wait(10)
data_atual = date.today()

def login():
    #temporary workarround for hardcoded email
    login = open(r'email.txt').read()
    passwd = getpass.getpass()
    #pick up the page ids
    id_login = 'sign_in_email'
    id_pass = 'sign_in_password'
    name_btn = 'commit'
    driver.get('https://hackerone.com/users/sign_in')
    #Do the actions on the browser
    input_login = driver.find_element_by_id(id_login)
    input_pass = driver.find_element_by_id(id_pass)
    btn_login = driver.find_element_by_name(name_btn)
    input_login.send_keys(login)
    input_pass.send_keys(passwd)
    btn_login.click()


def twofa():
    id_twofa = 'sign_in_totp_code'
    twofa = getpass.getpass(prompt='Two-factor Authentication code: ')
    input_twofa = driver.find_element_by_id(id_twofa)
    input_twofa.send_keys(twofa)
    
    id_btn = '/html/body/div[2]/div/div/div[2]/div/form/div/div/div/div[2]/div/button'
    input_btn = driver.find_element_by_xpath(id_btn)
    input_btn.click()

#def all_programs():

def private():
    global select_private
    driver.get('https://hackerone.com/hacker_dashboard/my_programs')
    id_private = 'PRIVATE' 
    btn_private = driver.find_element_by_id(id_private) 
    btn_private.click()
    #Scrolling the page and Listing
    for scroll in range(5):
        driver.execute_script("window.scrollTo(0, 100000)")
        sleep(5) 
    class_programs = 'spec-profile-name'
    select_private = driver.find_elements_by_class_name(class_programs)


def sqlite_connect():
    global conn
    path = r'C:\SQLite\db'
    conn = sqlite3.connect(path+r'\teste.db')


def sqlite_create_table():
    conn.execute('CREATE TABLE IF NOT EXISTS private_programs(id integer, name text, link text, datestamp text)')
    conn.commit()

def sqlite_insert_into_table():
    n = 1
    for printing in select_private:
        name = printing.text
        link = printing.get_attribute('href')
        print(n, name, link) 
        n += 1
        conn.execute("INSERT INTO private_programs (id, name, link, datestamp) VALUES ('"+str(n)+"', '"+name+"', '"+link+"', '"+str(data_atual)+"');")
    conn.commit()




def sqlite_drop_table():
    conn.execute('DROP TABLE programs')



login()
twofa()
#vai ate os programas privados e guarda os nomes
private()
sqlite_connect()
#atualiza a tabela de programas privados
sqlite_insert_into_table()

conn.close()