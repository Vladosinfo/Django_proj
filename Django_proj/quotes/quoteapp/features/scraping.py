from quoteapp.models import Tag, Author, Quote
import requests
from bs4 import BeautifulSoup

class scrapyng():
    def __init__(self):
        self.BASE_URL = 'https://quotes.toscrape.com/'
        self.count_added_quotes = 0
        self.count_added_authors = 0
        self.count_added_tags = 0


    def get_quotes(self, soup):
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        next_page = soup.find('li', class_='next')
        
        return quotes, authors, tags, next_page


    def select_save_author(self, author):
        authorOb = None

        author_tag_a = author.find_next_sibling('a')
        author_link_page = self.BASE_URL+author_tag_a['href']
        author_response = requests.get(author_link_page)
        soup_author = BeautifulSoup(author_response.text, 'lxml')
        # author_name = soup_author.find('h3', class_='author-title').text
        author_born_date = soup_author.find('span', class_='author-born-date').text
        author_born_location = soup_author.find('span', class_='author-born-location').text
        author_description = soup_author.find('div', class_='author-description').text    
        
        try:
            author_filter = Author.objects.filter(fullname = author.text)
            if not author_filter:
                author_save_result = Author(fullname = author.text, born_date = author_born_date, born_location = author_born_location, description = author_description)
                author_save_result.save()
                authorOb = author_save_result.id
                self.count_added_authors += 1
            else:
                authorOb = author_filter[0].id
        except Exception as e:
            print(f"Some error in time trying to save new author: {e}")

        return authorOb


    def select_save_tag(self, tag_name):
        tag_ob = None
            
        try:
            tag = Tag.objects.filter(name = tag_name)
            if not tag:
                tag_save_result = Tag(name = tag_name)
                tag_save_result.save()
                tag_ob = tag_save_result
                self.count_added_tags += 1
            else:
                tag_ob = tag[0]
        except Exception as e:
            print(f"Some error in time trying to save new tag: {e}")

        return tag_ob


    def scrapyng_quotes(self):
        response = requests.get(self.BASE_URL)
        soup = BeautifulSoup(response.text, 'lxml')
        next_page = soup.find('li', class_='next')

        quotes, authors, tags, next_page = self.get_quotes(soup)

        num = 1
        next_page_note_last = 0
        while next_page or next_page_note_last <= 1:
            for i in range(0, len(quotes)):
                quote_text = quotes[i].text[1:-1]

                # author
                author_obj = self.select_save_author(authors[i])

                # quote
                quote_obj = Quote.objects.filter(quote = quote_text)    #.save(commit=False)
                if not quote_obj:
                    new_quote = Quote.objects.create(quote = quote_text, author_id = author_obj)    #.save()
                    self.count_added_quotes += 1

                    # tags
                    tagsforquote = tags[i].find_all('a', class_='tag')
                    qtags = []
                    tagsObj = []
                    for tagforquote in tagsforquote:
                        tagObj = self.select_save_tag(tagforquote.text)
                        new_quote.tags.add(tagObj)

                        qtags.append(tagforquote.text)
                        tagsObj.append(tagObj)
                        # new_quote.tags.add(*tagsObj)

                    new_quote.save()

                    qtags = ', '.join(qtags)
                    print(str(num) + '. New added Quote: ' + quote_text[0:108] + '...')
                    print('-- Author: ' + authors[i].text)
                    print('-- Tags: ' + qtags)
                else:
                    print(str(num) + '. Exists Quote: ' + quote_text[0:108] + '...')
                print('-'*50)

                num+=1
                # if num == 35:
                    # break
            if next_page != None:
                next_link = self.BASE_URL+next_page.a['href']
                response = requests.get(next_link)
                soup = BeautifulSoup(response.text, 'lxml')
                quotes, authors, tags, next_page = self.get_quotes(soup)
            if next_page == None and next_page_note_last <= 1:
                next_page_note_last += 1

            # if num == 40:
            #     break
        
        print(f"New added Quotes: {self.count_added_quotes}, Authors: {self.count_added_authors}, Tags: {self.count_added_tags}")

        # added_items={
        #     {'quotes':self.count_added_quotes},
        #     {'authors':self.count_added_authors},
        #     {'tags':self.count_added_tags}}

        return True
