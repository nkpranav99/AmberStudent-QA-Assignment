from getgauge.python import before_suite, after_suite, step
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
import time
from read_data import *


class Driver:
    instance = None

@before_suite
def init():
    global driver
    options = Options()
    chromedriver_path = 'drivers/chromedriver'

    driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
    Driver.instance = driver

@after_suite
def close():
    driver.quit()

def find_element_by_element_name(locator_name):
  locator = read_data_from_csv().get(locator_name)
  # print(locator)

  ## Other locator types can be added here
  if locator['type'] == 'xpath':
     return driver.find_element(By.XPATH, locator['value'])
  elif locator['type'] == 'id':
     return driver.find_element(By.ID, locator['value'])
  elif locator['type'] == 'css_selector':
     return driver.find_element(By.CSS_SELECTOR, locator['value'])
  
  else:
     print("Locator value for {0} not found.".format(locator_name))

@step("Scroll to <element> in page")
def scroll_to_element(element):
  #  driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

   target_element = find_element_by_element_name(element)
  #  WebDriverWait(driver,10).until(EC.presence_of_element_located(target_element))

   driver.execute_script('arguments[0].scrollIntoView(true);', target_element)


base_url = 'https://amberstudent.com/'

@step("Go to AmberStudent homepage")
def go_to_gauge_homepage_at():
    driver.get(base_url)
    driver.maximize_window()

@step("Navigate to Search and Search for <location>")
def navigate_to_search(location):
  find_element_by_element_name("searchbox").click()
  find_element_by_element_name("input_box").send_keys(str(location))
  time.sleep(5)
  find_element_by_element_name("input_box").send_keys(Keys.RETURN)

@step("Wait for <num> seconds")
def wait_for_seconds(num):
   time.sleep(int(num))

@step("Click on <element> in the webpage")
def click_on_button(element):
    time.sleep(2)
    find_element_by_element_name(element).click()

@step("Wait until <element> is visible")
def wait_until_element_is_visible(element):
  locator = read_data_from_csv().get(element)
  print("locator: ", locator)
  try:
     WebDriverWait.until(EC.element(getattr(By, locator['type'], locator['value'])))
  except:
     print("Element is not visible on page!")
     

@step("Click on checkbox for <room_type>")
def click_on_checkbox(room_type):
  try:
    checkbox = find_element_by_element_name(room_type)
    scroll_to_element(room_type)
    find_element_by_element_name(room_type).click()
  except:
    print("{0} checkbox not found!".format(room_type))

@step("Verify if the <room_type> checkbox is checked")
def checkbox_status(room_type):
   checkbox = find_element_by_element_name(room_type)
   driver.execute_script('arguments[0].scrollIntoView(true);', checkbox)
   assert checkbox.is_selected(), "The {0} checkbox is not checked!".format(room_type)
      
@step("Open <result> in a new tab")
def open_results_in_new_tab(result):
   AC(driver).key_down(Keys.CONTROL).click(result).key_up(Keys.CONTROL).perform

@step("Verify <details> of the property is <value>")
def verify_details_of_property(details, value):
   time.sleep(10)

   if details == "title":
      title = find_element_by_element_name(details)
      assert title.text == value, "The title of the property doesn't match!"
   elif details == "location":
      location = find_element_by_element_name(details)
      assert location.text == value, "The location of the property doesn't match!"
   else:
      print("This property doesn't have {0} mentioned!".format(details))

@step("Iterate over the Countries and validate the Popular Cities are not repeated for any")
def validate_popular_cities():
   all_cities = []
   
   ## Store webelements for all countries tab except "All"
   countries = driver.find_elements_by_xpath('//*[@id="downshift-0-menu"]/div/div[1]/button')

   for i in range(2,len(countries)):
    ## Click on each country in the search container
    driver.find_element_by_xpath('//*[@id="downshift-0-menu"]/div/div[1]/button[' + str(i) + ']').click()

    ## Store container for all popular cities present in all countries
    cities = driver.find_elements_by_xpath(("(//div[@class='amber-1z0x9lj'])[" +str(i+1) + ']') + '/div')

    ## Iterate over all countries, get text from all city webelements and append it to all_cities list and verify if repetition is not there for any city
    for city in cities:
       if city.get_attribute("innerText") not in all_cities:
          all_cities.append(city.get_attribute("innerText"))
       else:
          print("{} is repeated in the Popular Cities List!".format(city.get_attribute("innerText")))

@step("Switch to new active window")
def switch_window_handle():
   time.sleep(10)
   window_handles = driver.window_handles

   new_window = window_handles[-1]
   driver.switch_to.window(new_window)

@step("Sign in using Google")
def google_sign_in():
   time.sleep(5)
   window_handles = driver.window_handles

   new_window = window_handles[-1]
   driver.switch_to.window(new_window)
   WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mantine-cae72ecah-body']//div[3]/div")))
  #  driver.switch_to_frame(iframe)
   time.sleep(5)
   driver.switch_to_active_element
   find_element_by_element_name("Google_Sign_in_button").click()
   time.sleep(2)

  #  driver.switch_to_active_element

   email, password = read_user_credentials_from_csv()

   email_id = find_element_by_element_name("Google_sign_in_email")
   email_id.send_keys(str(email))

   time.sleep(15)