"""
import os
from selenium  import webdriver
chromedriver = "/usr/lib/chromium-browser/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
browser.delete_all_cookies()
browser.maximize_window()	
browser.get('https://freebitco.in/')
browser.find_element_by_class_name('login_menu_button').click()
"""

import time
import os
from selenium  import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from recaptchav2solved.bot import RecaptchaV2Solved


def init():
	print '[*] FREEBITCOIN [*]'
	
	chromedriver = "/usr/lib/chromium-browser/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	browser = webdriver.Chrome(chromedriver)
	browser.delete_all_cookies()
	browser.maximize_window()	
	browser.get('https://freebitco.in/')
	browser.find_element_by_class_name('login_menu_button').click()
	print '[*] Clicando em login'

	# efetuando login
	form = browser.find_element_by_id('login_form_div')
	form.find_element_by_name('btc_address').send_keys('dennysaug@gmail.com')
	form.find_element_by_name('password').send_keys('...')
	browser.find_element_by_class_name('cc_btn_accept_all').click()
	form.find_element_by_tag_name('button').click()
	print '[*] Efetuando login'
	return browser


def run(browser, i):
	# ler o script js que multiplica os bitcoin
	scriptjs = open('script_freebitcoin.js', 'rb')
	# click roll
	time.sleep(6)    	
	while True:
		saldo_atual = float(browser.find_element_by_id('balance').text)
		try:
			captchaIframe = WebDriverWait(browser, 5).until(
				EC.visibility_of_element_located((By.TAG_NAME, "iframe"))
			)               

			if captchaIframe:
				
				recaptcha = RecaptchaV2Solved(key='777c64eaf7b22ead16668198b16266e1')
				googlekey = browser.find_element_by_class_name('g-recaptcha').get_attribute('data-sitekey')
				site = browser.current_url
				while True:
					resultCaptcha = recaptcha.solve(googlekey, site) 								    

					if len(resultCaptcha):
						browser.execute_script('document.getElementById("g-recaptcha-response").innerHTML="' + resultCaptcha + '";')
						
						try:
							btnPlay = WebDriverWait(browser, 30).until(
								EC.element_to_be_clickable((By.ID, "free_play_form_button"))
							)

							if btnPlay:
								btnPlay.click()
								print '[*] Girou a roleta'
								time.sleep(6)
								novo_saldo = float(browser.find_element_by_id('balance').text)
								
								print ('[*] Voce Ganhou: %.8f BTC' % (novo_saldo - saldo_atual))
								break

						except:
							print '[*] Tempo da roleta ainda disponivel'
							time.sleep(5)

					else:
						print '[*] Captcha nao resolvido'
						
			break
		except NoSuchElementException:
			print '[*] Sem captcha ainda'
			time.sleep(30)

	if True: #i % 3 == 1: 
		# click on multiply btc
		browser.find_element_by_class_name('double_your_btc_link').click()

		# roda script bot
		print '[*] Iniciando as apostas'
		browser.execute_script('console.log("allow pasting");')
		browser.execute_script(scriptjs.read())
		scroll = browser.find_element_by_class_name('counter')
		scroll.location_once_scrolled_into_view
		
		time.sleep(5*60)
		print '[*] Saldo apos das apostas: ' + browser.find_element_by_id('balance').text + ' BTC'
		# aguarda 1h
		# atualiza a pagina
		# browser.refresh()
		# print '[*] Saldo Atual: ' + browser.find_element_by_id('balance').text + ' BTC'
	print "[*]=================[*]\n"
	browser.quit()

def main():
	i = 1	
	while True:		
		browser = init()
		run(browser, i)
		
		if i % 3 == 1:
			time.sleep(3300)
		else:
			time.sleep(3600)
			
		i += 1

if __name__ == "__main__":
	main()
	
