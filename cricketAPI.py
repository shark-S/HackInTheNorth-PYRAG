import requests,os,bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Cricket(object):

	def get_player_stats(self, playerName):
	    base_url="http://www.espncricinfo.com"
	    url="http://www.espncricinfo.com/ci/content/player/search.html?search="
	    names=[]
	    names=playerName.split()
	    playerName="+".join(names)
	    url=url+playerName
	    res=requests.get(url)
	    res.raise_for_status()
	    soup=bs4.BeautifulSoup(res.text,"lxml")
	    playerStatLink=soup.select(".ColumnistSmry") 
	    playerStatLink=playerStatLink[1]
	    temp_url=playerStatLink.get('href')
	    url=base_url+temp_url
	    res=requests.get(url)
	    soup=bs4.BeautifulSoup(res.text,"lxml")
	    player_info=soup.select(".ciPlayerinformationtxt")
	    player_stats={}   
	    for item in player_info[0:len(player_info)]:
	    	b=item.find('b')
	    	if b.string=="Major teams":
	    		span=item.findAll('span')
	    		temp=""
	    		for it in span:
	    			temp+=it.string+" "
	    	else:
	    		temp=item.find('span')
	    		temp=temp.string
	    	player_stats[b.string]=temp
	    return player_stats  

	def live_score(self):
	
	    response = requests.get('http://www.cricbuzz.com/live-scores')
	    soup = bs4.BeautifulSoup(response.text,"lxml")
	    team_mate = soup.findAll("div", {"class" : "cb-lv-main"})
	    scores = []
	    for i in team_mate:
    		scores.append(i.text) 
	    return scores

	def list_matches(self):
		response = requests.get('https://cricket.yahoo.com/matches/schedule')
		soup = bs4.BeautifulSoup(response.text,"lxml")
		head_list = soup.findAll("em", {"class": "ycric-table-heading"})
		invited_team_list = soup.findAll("div", {"class": "ycric-table-sub-heading"})
		no_list = soup.findAll("td", {"class": "sno"})
		tour_dates_list  = soup.findAll("span", {"class" : "matchDateTime"})
		match_list = soup.findAll("td", {"class": "smatch"})
		venue_list= soup.findAll("td", {"class": "svenue"})
		result_list = soup.findAll("td", {"class": "sresult"})
		heading = 0
		nos = []
		tour_date = []
		team_list = []
		venue = []
		result = []
		ans = []
		cnt = 0
		for i in match_list:
			if i.text != "Match":
				team_list.append(i.text)
		for i in no_list:
			if i.text !="#":
				nos.append(i.text)
		for i in venue_list:
			if i.text!="Venue":
				venue.append(i.text)
		for i in result_list:
			if i.text!="Result":
				result.append(i.text)
		cnt =len(nos)

		check = 0

		matches = []
		for i in range(cnt):
			if nos[i]=="1":
				if check != 0:
					check = check +1
				else:
					matches.append("\n\n")
					#print ("")
					#print ("")
				matches.append(head_list[heading].text)
				#print (head_list[heading].text)
				z= "Teams: "+invited_team_list[heading].text
				matches.append(z)
				#print (z)
				heading = heading+1
				l = nos[i]+" "+tour_dates_list[i].text+" "+team_list[i]+" "+venue[i]+" "+result[i]
				matches.append(l)
			else:
				l = nos[i]+" "+tour_dates_list[i].text+" "+team_list[i]+" "+venue[i]+" "+result[i]
				matches.append(l)
				#print (l)

		return matches

	def news(self):
		base_url='http://www.cricbuzz.com/cricket-news/latest-news'
		res=requests.get(base_url)

		soup = bs4.BeautifulSoup(res.text,"lxml")
		news = soup.select(".cb-col-33 a")
		news_dict={}
		for all_news in news:
		    if str(all_news.get("title"))!="More Photos" and str(all_news.get("title"))!="None":
        	    	news_dict[all_news.get("title")]=base_url+all_news.get("href")
		return news_dict

   
if __name__=='__main__':
	attr =  Cricket()
	player_stats=attr.get_player_stats("Virender Sehwag")
	print (player_stats)
	print (attr.live_score())
	print (attr.list_matches())
	print (attr.news())
