#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
import datetime, re, os, time, threading, sqlite3
from sqlite3 import Error



class FacebookScraper():
    def __init__(self):
        self.new_ads = []
        self.old_ads = []
        self.previous_posts = []
        #self.postCSS='div._1dwg._1w_m._q7o' #this css is for a smaller portion of post that is sufficient to extract required information.
        #self.postCSS='div._5jmm._5pat._3lb4.u_1hpu27ttag' #this modification is done to easily distinguish hidden posts from shown posts
        self.postCSS='div._5jmm._5pat._3lb4.w_1f8qou8f2n'
        #self.sponsoredCSS = 'b.j_1hpu27-s20.i_1hpu27-s1t'#change
        self.sponsoredCSS = 'a.q_1f8qou0u_y.w_1f8qou438b'
        self.adtitleCSS ='span.fwb.fcg'#change
        self.data_file = 'data/ad_data.db'
        self.refresh_delay=5

    def generate_file(self,username):
        try:
            con = sqlite3.connect(self.data_file)
            cursorObj = con.cursor()
            self.user = str(username)
            cursorObj.execute("CREATE TABLE IF NOT EXISTS "+self.user+"(ad_title text, ad_description text, ad_url text, ad_time text, ad_date text)")
            con.commit()
        except Error:
            print(Error)
        finally:
            con.close()

    def sql_fetch(self):
        con = sqlite3.connect(self.data_file)
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM '+str(self.user))
        rows = cursorObj.fetchall()
        for row in rows:
            print(row)
        con.close()

    def start_browser(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://www.facebook.com')

    def clean_html(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def ampersand_filter(self,string):
        new_string = string.replace('&amp;','&')
        return new_string

    def add_line_to_new_format(self,line_items):
        with open(self.data_file,'a') as f:
            line = '~'.join(line_items)
            f.write(line+'\n')

    def check_sponsored_tag(self, post):
        #sponsored_tag = post.find_elements_by_css_selector('a.r_1hpu27_e3t.n_1hpu27zbgc')#change
        sponsored_tag1 = post.find_elements_by_css_selector('a.z_1hpu27-s23.v_1hpu27-s26')#change
        sponsored_tag = post.find_elements_by_css_selector('a.q_1f8qou0u_y.w_1f8qou438b')
        if len(sponsored_tag)>0 or len(sponsored_tag1)>0:
            return True

        sub_heading=''
        sub_heading_s = post.find_elements_by_css_selector(self.sponsoredCSS)
        for alphabet_s in sub_heading_s:
            alphabet = alphabet_s.get_attribute('innerHTML')
            sub_heading = sub_heading + alphabet
        if sub_heading == "Sponsored":
            return True
        else:
            return False

    def fb_ad_scraper(self):
        for post in self.new_ads:
            try:
                line_items=[]

                #this prints the advertisement title
                try:
                    ad_title_box = post.find_element_by_css_selector('span.fwb.fcg')
                except:
                    ad_title_box = post.find_element_by_css_selector('span.fsl.fwb')
                ad_title_s = ad_title_box.find_element_by_tag_name('a')
                ad_title = str(ad_title_s.get_attribute('innerHTML')).strip()
                ad_title = self.ampersand_filter(ad_title)
                line_items.append(ad_title)
                print(ad_title)


                #this prints the advertisement description
                descs=[]
                ad_descs_s = post.find_elements_by_tag_name('p')
                for item in ad_descs_s:
                    ad_desc = str(item.get_attribute('innerHTML')).strip()
                    ad_desc = self.clean_html(ad_desc)
                    ad_desc = self.ampersand_filter(ad_desc)
                    descs.append(ad_desc)
                    print(ad_desc)
                print('\n')
                desc_string = '. '.join(descs)
                line_items.append(desc_string)

                #this gets the url
                url = ad_title_s.get_attribute('href')
                line_items.append(url)

                #this provides the date and time
                date_time = datetime.datetime.now()
                ad_date = date_time.strftime("%x")
                ad_time = date_time.strftime("%X")
                line_items.append(ad_time)
                line_items.append(ad_date)

                #this adds everything to a line, which is added to self.data_file
                conn = sqlite3.connect(self.data_file)
                cursorObj = conn.cursor()
                cursorObj.execute('INSERT INTO '+self.user+'(ad_title, ad_description, ad_url, ad_time, ad_date) VALUES(?, ?, ?, ?, ?)', tuple(line_items))
                conn.commit()
                conn.close()

                #this refreshes the old_ads list
                self.old_ads.append(post)
            except:
                print('ERROR: One post not processed')
                continue
        self.new_ads=[]


    def refresh(self):
        all_posts = self.browser.find_elements_by_css_selector(self.postCSS) + self.browser.find_elements_by_css_selector(self.postCSS+'.sponsored_ad')
        hidden_posts = self.browser.find_elements_by_css_selector(self.postCSS+'.hidden_elem') + self.browser.find_elements_by_css_selector(self.postCSS+'.sponsored_ad.hidden_elem')

        for hidden_post in hidden_posts:
            if hidden_post in all_posts:
                all_posts.remove(hidden_post)

        for post in all_posts:
            if post in self.previous_posts:
                all_posts.remove(post)
                continue
            else:
                self.previous_posts.append(post)
                if self.check_sponsored_tag(post)==True:
                    if post in self.old_ads:
                        continue
                    else:
                        self.new_ads.append(post)

        print([len(self.new_ads),len(self.old_ads)])
        self.fb_ad_scraper()

    def start(self):
        self.repeat=True

        def start_function():
            if self.browser.current_url == 'https://www.facebook.com/':
                while self.repeat==True:
                    self.refresh()
                    time.sleep(self.refresh_delay)
                self.repeat=True

        t = threading.Thread(target=start_function, daemon=True)
        t.start()


    def stop(self):
        while True:
            try:
                self.repeat=False
                self.refresh()
                break
            except:
                continue

if __name__ == '__main__':
    s = FacebookScraper()
    s.generate_file('test')
    s.sql_fetch()
