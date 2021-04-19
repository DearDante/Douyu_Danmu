from selenium import webdriver
brow = webdriver.Safari()
brow.implicitly_wait(10)
brow.get('https://www.douyu.com/8777')
a = brow.find_element_by_id('js-barrage-list')
b = a.find_elements_by_tag_name('li')
c = b[0].find_elements_by_tag_name('span')
print(c[0].text)
brow.close()

