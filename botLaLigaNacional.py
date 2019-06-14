import telebot
from telebot import types

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import time

TOKEN = 'XXX' #Ponemos nuestro TOKEN generado con el @BotFather

mi_bot = telebot.TeleBot(TOKEN) #Creamos nuestra instancia "mi_bot" a partir de ese TOKEN

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('user-agent = Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')

@mi_bot.message_handler(commands=['start'])
def send_welcome(message):
    mi_bot.reply_to(message, "Bienvenido al bot de estadisticas de La Liga Nacional de Basquet")

@mi_bot.message_handler(commands=['help'])
def send_welcome(message):
    mi_bot.reply_to(message, "Envia /partidos para ver los proximos partidos o el ID de fibalivestats para ver las estadisticas")

@mi_bot.message_handler(commands=['partidos'])
def send_welcome(message):
	if (message.from_user.id == 843929119):
		url = 'http://www.laliganacional.com.ar/laliga/'
		driver = webdriver.Chrome(executable_path='/home/andres/proyectos/telegramLaLigaNacional/chromedriver', options=options)

		driver.get(url)

		# time.sleep(5)
		mi_bot.reply_to(message, "Estos son los partidos disponibles:")

		try:
			driver.switch_to.frame(0)
			x = driver.find_elements_by_css_selector('.spls_lsmatch')
			markup = types.ReplyKeyboardMarkup()
			
			for each in x:

				link = each.find_elements_by_tag_name("a")[0]
				partido = link.get_attribute('href').replace('http://www.fibalivestats.com/webcast/ADC/', '').replace('/', '')
				y = each.find_elements_by_css_selector('.teamname')
				for row in y:
					partido += " " + row.text
				
				markup.add(partido)
				# partidos += " " + each.find_element_by_css_selector("spls_matchrow3")
		
			# mi_bot.reply_to(message, partidos)
			mi_bot.reply_to(message, "Elija un partido", reply_markup=markup)

			driver.close()
		except:
			mi_bot.reply_to(message, "\nNo encontramos partidos")
			driver.close()
			return
		# for each in x:
		# 	print (x)
		# 	link = row.find_elements_by_tag_name("a")[1]
		# 	mi_bot.reply_to(message, link.get_attribute('href'))


@mi_bot.message_handler(func=lambda m: True)
def echo_all(message):
	if (message.from_user.id == 843929119):
		#mi_bot.reply_to(message, message.text)
		partidoNumero = message.text

		partidoNumero = partidoNumero.split(" ", 1)[0]

		url = 'https://www.fibalivestats.com/u/ADC/' + partidoNumero + '/st.html'
		driver = webdriver.Chrome(executable_path='/home/andres/proyectos/telegramLaLigaNacional/chromedriver', options=options)

		try:
			driver.get(url)
		except:
			mi_bot.reply_to(message, "Partido no encontrado")
			driver.close()
			return


		try:
			localname = driver.find_element_by_css_selector('.id_aj_1_code').text
			visitaname = driver.find_element_by_css_selector('.id_aj_2_code').text
			localTotal = str(driver.find_element_by_css_selector('#aj_1_score').text)
			visitaTotal = str(driver.find_element_by_css_selector('#aj_2_score').text)
		except:
			try:
				url = 'https://www.fibalivestats.com/u/ADC/' + partidoNumero
				driver.get(url)
				noEmpezado = driver.find_element_by_css_selector('.upcoming-match-status').text
				mi_bot.reply_to(message, noEmpezado)
				driver.close()
				types.ReplyKeyboardRemove()
				return
			except:	
				mi_bot.reply_to(message, "Partido no encontrado")
				driver.close()
				return

		types.ReplyKeyboardRemove()
		cuartos = "	" + localname + "	" + visitaname
		
		q1 = "1	" + str(driver.find_element_by_css_selector('#aj_1_p1_score').text) + "	" +  str(driver.find_element_by_css_selector('#aj_2_p1_score').text)
		q2 = "2	" + str(driver.find_element_by_css_selector('#aj_1_p2_score').text) + "	" +  str(driver.find_element_by_css_selector('#aj_2_p2_score').text)
		q3 = "3	" + str(driver.find_element_by_css_selector('#aj_1_p3_score').text) + "	" +  str(driver.find_element_by_css_selector('#aj_2_p3_score').text)
		q4 = "4	" + str(driver.find_element_by_css_selector('#aj_1_p4_score').text) + "	" +  str(driver.find_element_by_css_selector('#aj_2_p4_score').text)

		resumenlocal = "2P: " + str(driver.find_element_by_css_selector('#aj_1_tot_sTwoPointersMade').text) + "/" + str(driver.find_element_by_css_selector('#aj_1_tot_sTwoPointersAttempted').text) + " (" + str(driver.find_element_by_css_selector('#aj_1_tot_sTwoPointersPercentage').text) + ")"
		resumenlocal += "\n3P: " + str(driver.find_element_by_css_selector('#aj_1_tot_sThreePointersMade').text) + "/" + str(driver.find_element_by_css_selector('#aj_1_tot_sThreePointersAttempted').text) + " (" + str(driver.find_element_by_css_selector('#aj_1_tot_sThreePointersPercentage').text) + ")"
		resumenlocal += "\nTC: " + str(driver.find_element_by_css_selector('#aj_1_tot_sFieldGoalsMade').text) + "/" + str(driver.find_element_by_css_selector('#aj_1_tot_sFieldGoalsAttempted').text) + " (" + str(driver.find_element_by_css_selector('#aj_1_tot_sFieldGoalsPercentage').text) + ")"
		resumenlocal += "\nTL: " + str(driver.find_element_by_css_selector('#aj_1_tot_sFreeThrowsMade').text) + "/" + str(driver.find_element_by_css_selector('#aj_1_tot_sFreeThrowsAttempted').text) + " (" + str(driver.find_element_by_css_selector('#aj_1_tot_sFreeThrowsPercentage').text) + ")"
		resumenlocal += "\nRT: " + str(driver.find_element_by_css_selector('#aj_1_tot_sReboundsTotal').text) 
		resumenlocal += "\nAS: " + str(driver.find_element_by_css_selector('#aj_1_tot_sAssists').text) 
		resumenlocal += "\nRB: " + str(driver.find_element_by_css_selector('#aj_1_tot_sSteals').text) 
		resumenlocal += "\nTP: " + str(driver.find_element_by_css_selector('#aj_1_tot_sBlocks').text) 
		resumenlocal += "\nPE: " + str(driver.find_element_by_css_selector('#aj_1_tot_sTurnovers').text) 
		resumenlocal += "\nFP: " + str(driver.find_element_by_css_selector('#aj_1_tot_sFoulsPersonal').text) 
		resumenlocal += "\nPtPi: " + str(driver.find_element_by_css_selector('#aj_1_tot_sPointsInThePaint').text) 
		resumenlocal += "\n2aO: " + str(driver.find_element_by_css_selector('#aj_1_tot_sPointsSecondChance').text) 
		resumenlocal += "\nPtP: " + str(driver.find_element_by_css_selector('#aj_1_tot_sPointsFromTurnovers').text) 
		resumenlocal += "\nPtB: " + str(driver.find_element_by_css_selector('#aj_1_tot_sBenchPoints').text) 
		resumenlocal += "\nPtCA: " + str(driver.find_element_by_css_selector('#aj_1_tot_sPointsFastBreak').text) 

		resumenvisita = "2P: " + str(driver.find_element_by_css_selector('#aj_2_tot_sTwoPointersMade').text) + "/" + str(driver.find_element_by_css_selector('#aj_2_tot_sTwoPointersAttempted').text) + " (" + str(driver.find_element_by_css_selector('#aj_2_tot_sTwoPointersPercentage').text) + ")"
		resumenvisita += "\n3P: " + str(driver.find_element_by_css_selector('#aj_2_tot_sThreePointersMade').text) + "/" + str(driver.find_element_by_css_selector('#aj_2_tot_sThreePointersAttempted').text) + " (" + str(driver.find_element_by_css_selector('#aj_2_tot_sThreePointersPercentage').text) + ")"
		resumenvisita += "\nTC: " + str(driver.find_element_by_css_selector('#aj_2_tot_sFieldGoalsMade').text) + "/" + str(driver.find_element_by_css_selector('#aj_2_tot_sFieldGoalsAttempted').text) + " (" + str(driver.find_element_by_css_selector('#aj_2_tot_sFieldGoalsPercentage').text) + ")"
		resumenvisita += "\nTL: " + str(driver.find_element_by_css_selector('#aj_2_tot_sFreeThrowsMade').text) + "/" + str(driver.find_element_by_css_selector('#aj_2_tot_sFreeThrowsAttempted').text) + " (" + str(driver.find_element_by_css_selector('#aj_2_tot_sFreeThrowsPercentage').text) + ")"
		resumenvisita += "\nRT: " + str(driver.find_element_by_css_selector('#aj_2_tot_sReboundsTotal').text) 
		resumenvisita += "\nAS: " + str(driver.find_element_by_css_selector('#aj_2_tot_sAssists').text) 
		resumenvisita += "\nRB: " + str(driver.find_element_by_css_selector('#aj_2_tot_sSteals').text) 
		resumenvisita += "\nTP: " + str(driver.find_element_by_css_selector('#aj_2_tot_sBlocks').text) 
		resumenvisita += "\nPE: " + str(driver.find_element_by_css_selector('#aj_2_tot_sTurnovers').text) 
		resumenvisita += "\nFP: " + str(driver.find_element_by_css_selector('#aj_2_tot_sFoulsPersonal').text) 
		resumenvisita += "\nPtPi: " + str(driver.find_element_by_css_selector('#aj_2_tot_sPointsInThePaint').text) 
		resumenvisita += "\n2aO: " + str(driver.find_element_by_css_selector('#aj_2_tot_sPointsSecondChance').text) 
		resumenvisita += "\nPtP: " + str(driver.find_element_by_css_selector('#aj_2_tot_sPointsFromTurnovers').text) 
		resumenvisita += "\nPtB: " + str(driver.find_element_by_css_selector('#aj_2_tot_sBenchPoints').text) 
		resumenvisita += "\nPtCA: " + str(driver.find_element_by_css_selector('#aj_2_tot_sPointsFastBreak').text) 


		driver.close()

		cabecera = localname + ' (' + localTotal + ') vs ' + visitaname + ' (' + visitaTotal + ')'
		cuartos += "\n " + q1 + "\n " + q2 + "\n " + q3 + "\n " + q4

		response = cabecera + "\n\n" + cuartos + "\n\n*" + localname + "*\n" + resumenlocal + "\n\n*" + visitaname + "*\n" + resumenvisita

		mi_bot.reply_to(message, response, parse_mode= 'Markdown')
	else:
		mi_bot.reply_to(message, "No te reconozco")


mi_bot.polling()
