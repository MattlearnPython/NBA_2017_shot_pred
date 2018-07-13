from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import 

def extract_numbers(str_list):
	numbers_list = []
	for words in str_list:
		# Modified string to better split
		words_new = str()
    	for char in words:
        	if char != 'p':
            	words_new += char
        	else:
            	words_new += ' '
        # Extract numbers
		numbers = [int(s) for s in words_new.split() if s.isdigit()]
		numbers_list.append(numbers)

	return numbers_list

def get_shot_chart(url, player_name):
	#url = "https://www.basketball-reference.com/teams/GSW/2018_games.html"  # Schedule of GSW in 2017-2018 season on Basketball-reference.com
	driver = webdriver.Chrome('/Users/jinzhao/Desktop/Machine Learning/NBA/nba shot prediction/chromedriver')
	driver.get(url)

	# Wait up to 10 sec to load the website, otherwise it will close
	WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable(
	            (By.XPATH, """//table[@id='games']//tbody//tr//td[@data-stat='box_score_text']""")
	            )
		)
	print("Complete Loading!")

	# Navigating back clears 'games'. 
	# Sol: Relocate games in every loop
	games = driver.find_elements_by_xpath("//table[@id='games']//tbody//tr//td[@data-stat='box_score_text']")
	n_games = len(games)
	#player_name = "'Stephen Curry'"

	missed_shots = []
	made_shots = []
	for i in range(n_games):
		# Find 'Box score' and click
		game = driver.find_elements_by_xpath("//table[@id='games']//tbody//tr//td[@data-stat='box_score_text']")[i]
		game.click()
		# Find 'Shot Chart' and click
		shot_chart = driver.find_element_by_xpath("//*[contains(text(), 'Shot Charts')]")
		shot_chart.click()
		# Choose player
		### Have to deal with matchups where this player didn't show up
		player_shot = driver.find_elements_by_xpath("//*[contains(text(),%s)]" % player_name)
		print(len(player_shot))
		print(driver.current_url)
		if len(player_shot) != 0:
			player_shot[0].click()
			# Extract Shot positions
			all_shots = driver.find_elements_by_xpath("//div[@id='shots-GSW']/div")
			for shot in all_shots:
				tip = shot.get_attribute("tip")
				if "Stephen Curry" in tip:
					pos = shot.get_attribute("style")
					if "made" in tip:
						made_shots.append(pos)
					else:
						missed_shots.append(pos)

		# Need two backs to return
		driver.back()
		driver.back()
	driver.quit()

	# Process data
	missed_shots_pos = extract_numbers(missed_shots)
	made_shots_pos = extract_numbers(made_shots)

	n_made = len(made_shots_pos)
	n_missed = len(missed_shots_pos)

	X_missed = np.array(missed_shots_pos).resize((n_missed, 2))
	y_missed = np.zeros((n_missed, 1))

	X_made =  np.array(made_shots_pos).resize((n_made, 2))
	y_made = np.ones((n_made, 1))

	data_missed = np.column_stack((X_missed, y_missed))
	data_made = np.column_stack((X_made, y_made))

	data = np.vstack((data_missed, data_made))
	data_ = np.random.permutation(data)
	return data_

if __name__ == '__main__':

	# Scrape player shot chart, Return shots position and save as a csv file
	player_name = "'Stephen Curry'"
	url = "https://www.basketball-reference.com/teams/GSW/2018_games.html"  # Schedule of GSW in 2017-2018 season on Basketball-reference.com
	data = get_shot_chart(url, player_name)


    with open('Stephen_2017.csv', 'w') as file:
    	writer = csv.writer(file)
    for i in range(data.shape[0]):
        writer.writerow(data[i, :])
        







