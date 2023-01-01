

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_anime_page():
    anime_url = 'https://www.imdb.com/search/title/?at=0&genres=animation&keywords=anime&num_votes=1000,&sort=user_rating&title_type=tv_series'
    response = requests.get(anime_url)
    print(response)
    if response.status_code != 200:
        raise Exception ('Failed to load page {} '.format(anime_url))
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

imdb_url = ['https://www.imdb.com/search/title/?at=0&genres=animation&keywords=anime&num_votes=1000,&sort=user_rating&title_type=tv_series','https://www.imdb.com/search/title/?title_type=tv_series&num_votes=1000,&genres=animation&keywords=anime&sort=user_rating,desc&start=51&ref_=adv_nxt']
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

def get_anime_data1(Urls):
    anime_data1 = []
    
    for i in Urls:
        response = requests.get(i,headers = headers)
        doc = BeautifulSoup(response.content, 'html.parser')
        anime_data1.append(doc)
    return anime_data1


anime_data3 = get_anime_data1(imdb_url)

def get_anime_titles():
    anime_title = []
    #The anime_data3 conatins all the webpage data in html format
    for i in anime_data3:
        #find_all is BeautifulSoup method used for finding specified tags in html 
        anime_data = i.find_all('div', attrs={'class': 'lister-item mode-advanced'})  
        # Get anime title using h3 tags 
        for each_line in anime_data:
            title = each_line.h3.a.text
            anime_title.append(title)
    return anime_title

def get_anime_rating():
    anime_rating = [] 
    #The anime_data3 conatins all the webpage data in html format
    for i in anime_data3:
        title_rating_tag = i.find_all('div',{'class':'inline-block ratings-imdb-rating'})
        for j in title_rating_tag:
            rating_tag = j.text.replace('\n', '')
            anime_rating.append(rating_tag)
    return anime_rating

def get_anime_url():
    anime_url_tags = []
    base_url = 'https://www.imdb.com/' 
    #The anime_data3 conatins all the webpage data in html format
    for i in anime_data3:
        # Get url using h3 tags 
        url_tags = i.find_all('h3', {'class':'lister-item-header'})

        for j in url_tags:
            # concatenate base_url and url obtained by h3 tags
            anime_url_tags.append('https://www.imdb.com/'+ j.find('a')['href'])
    return anime_url_tags

def get_anime_description():
    anime_description = []
    #The anime_data3 conatins all the webpage data in html format
    for i in anime_data3:
        # Get description using p tags 
        anime_descp_tags = i.find_all('p', {'class': 'text-muted'})
        for j in anime_descp_tags:
            # Replace '\n' by empty space ''
            anime = j.text.replace('\n','')
            anime_description.append(anime)
        # Index the anime_descript list for only description    
        anime_descript = anime_description[1::2]
    return anime_descript

urls = get_anime_url()
anime_data2 = get_anime_data1(urls)

def get_year_duration(): 
    year_durations = []
    #The anime_data2 conatins all the 100 individual webpage data in html format
    for i in anime_data2:
        year_duration_tag = i.find_all('span', {'class':'sc-8c396aa2-2 itZqyK'})[0]
        for year in year_duration_tag:
            year_durations.append(year.text)
    return  year_durations

def get_creator_name():
    creators = []
    #The anime_data2 conatins all the 100 individual webpage data in html format
    for i in anime_data2:
        creator_name_tag = i.find_all('a', {'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})[0]
        for i in creator_name_tag:
            creators.append(i.text)
    return creators

def get_awards_nominations():
    awards_nominations = []
    #The anime_data2 conatins all the 100 individual webpage data in html format
    for i in anime_data2:
        award_tags = i.find_all('label',{'class':'ipc-metadata-list-item__list-content-item'})[0]
        
        for i in award_tags:
            award = i.text
            if award[0] in '0987654321':
                awards_nominations.append(award) 
            else:
                awards_nominations.append('NaN')
    return awards_nominations


def scrape_individual_anime():
    
    anime_dict = {
        'title' : get_anime_titles(),
        'rating' : get_anime_rating(),
        'description' : get_anime_description(),
        'year_duration' :get_year_duration(),
        'creator_name'  :get_creator_name(), 
        'awards_and_nominations' : get_awards_nominations(),
        'url' : get_anime_url()
    }
    return pd.DataFrame(anime_dict)
    
def scrape_anime():
    individual_df = scrape_individual_anime()
    individual_df.to_csv('Top100_Anime.csv', index=False)

import sys

if __name__ == "__main__":
    scrape_anime() 
    

