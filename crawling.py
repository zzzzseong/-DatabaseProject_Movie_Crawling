from ctypes import sizeof
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import requests
import math, sys
import re
import math
movieCnt =0
def open_db(): #conn과 cur을 새로 만들어 가져옴
    conn = pymysql.connect(host='localhost', user='root',
                           password='11111111', db='navermovie', unix_socket='/tmp/mysql.sock')
    cur = conn.cursor(pymysql.cursors.DictCursor)#이름으로 칼럼값 접근
    return conn, cur

def close_db(conn,cur):
    cur.close()
    conn.close()
    
conn_1, cur_1=open_db()
conn_2, cur_2=open_db()
conn_3, cur_3=open_db()
conn_4, cur_4=open_db()
conn_5, cur_5=open_db()
conn_6, cur_6=open_db()
conn_7, cur_7=open_db()
conn_8, cur_8=open_db()
conn_9, cur_9=open_db()
buffer_genre=[]
buffer_country=[]
buffer_director=[]
buffer_actor=[]
buffer_persona=[]
buffer_line=[]
buffer_photo=[]
buffer_review=[]


def get_rankingmovie():
    raw = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver').text
    html = BeautifulSoup(raw, 'html.parser')
    allmovie = html.select_one('div.type_1>div#old_content>div.tab_type_6>ul>li:nth-child(3)>a').attrs['href']
    for page in range(1,41): #영화 2000개
        raw_a = requests.get('https://movie.naver.com/movie/sdb/rank/'+allmovie+'&page='+str(page)).text
        html_a = BeautifulSoup(raw_a, 'html.parser')
        mlist = html_a.select('.list_ranking>tbody > tr')
        for article in mlist:
            try:
                href = article.select_one('.title>.tit5>a').attrs['href']
                href='https://movie.naver.com'+href
                get_moviedata(href)
            except:
                title = pymysql.NULL 
    
    for page in range(1,41): #영화 재귀
        raw_b = requests.get('https://movie.naver.com/movie/sdb/rank/'+allmovie+'&page='+str(page)).text
        html_b = BeautifulSoup(raw_b, 'html.parser')
        mlist = html_b.select('.list_ranking>tbody > tr')
        for article in mlist:
            try:
                href = article.select_one('.title>.tit5>a').attrs['href']
                href='https://movie.naver.com'+href
                get_moviedata_rec1(href) #2000*5
                get_moviedata_rec2(href) #2000*5*5
                # get_moviedata_rec3(href) #2000*5*5*5
            except:
                title = pymysql.NULL 
                
                 
def get_moviedata_rec1(href):#재귀1
    raw_rec =requests.get(href).text
    html_rec = BeautifulSoup(raw_rec, 'html.parser')
    mlist = html_rec.select('div.obj_section>div.link_movie.type2>ul.thumb_link_mv>li')
    for article in mlist:
        try:
            rechref = article.select_one('a.title_mv').attrs['href']
            rechref='https://movie.naver.com'+rechref
            get_moviedata(rechref)
        except:
            title = pymysql.NULL 

def get_moviedata_rec2(href):#재귀2
    raw_rec =requests.get(href).text
    html_rec = BeautifulSoup(raw_rec, 'html.parser')
    mlist = html_rec.select('div.obj_section>div.link_movie.type2>ul.thumb_link_mv>li')
    for article in mlist:
        try:
            rechref = article.select_one('a.title_mv').attrs['href']
            rechref='https://movie.naver.com'+rechref
            get_moviedata_rec1(rechref)
        except:
            title = pymysql.NULL
            
def get_moviedata_rec3(href):#재귀3
    raw_rec =requests.get(href).text
    html_rec = BeautifulSoup(raw_rec, 'html.parser')
    mlist = html_rec.select('div.obj_section>div.link_movie.type2>ul.thumb_link_mv>li')
    for article in mlist:
        rechref = article.select_one('a.title_mv').attrs['href']
        rechref='https://movie.naver.com'+rechref
        get_moviedata_rec2(rechref)

def get_moviedata(href):
    global conn_1,cur_1,conn_2,cur_2,conn_3,cur_3,conn_4,cur_4,conn_5,cur_5,conn_6,cur_6,conn_7,cur_7,conn_8,cur_8,conn_9,cur_9
    global buffer_genre,buffer_country,buffer_director,buffer_actor,buffer_persona,buffer_line,buffer_photo,buffer_review
    ####################################################################영화
    raw_movie =requests.get(href).text
    html_movie = BeautifulSoup(raw_movie, 'html.parser')
    
    moviecode= (int)(href.split('=')[1]) #영화코드

    title_movie=html_movie.select_one('div.mv_info>h3.h_movie>a').text #영화 제목
    
    movie_rate=html_movie.select_one('div.mv_info>dl.info_spec>dd:nth-child(8)>p>a') #영화 등급 ex)12, 19...
    if(movie_rate is None):
        movie_rate=pymysql.NULL
    else:
        movie_rate=movie_rate.text

    audience_rate=html_movie.select_one('a.ntz_score>div.star_score>span.st_off>span.st_on') #관람객 평점
    if(audience_rate is None):
        audience_rate=pymysql.NULL
    else:
        audience_rate=float(audience_rate['style'][6:-1])/10


    audience_count=html_movie.select_one('div.score>div.uio_ntz_btn.see>div.ly_count>em') #관람객 참여자
    if(audience_count is None):
        audience_count=pymysql.NULL
    else:
        audience_count=audience_count.text

    netizen_rate=html_movie.select_one('div.score.score_left>div.star_score>a#pointNetizenPersentBasic>span.st_off>span.st_on') #네티즌 평점
    if(netizen_rate is None):
        netizen_rate=pymysql.NULL
    else:
        netizen_rate=float(netizen_rate['style'][6:-1])/10

    netizen_count=html_movie.select_one('div.score.score_left>div.uio_ntz_btn>div.ly_count>em')#네티즌 참여자
    if(netizen_count is None):
        netizen_count=pymysql.NULL
    else:
        netizen_count=netizen_count.text 

    journalist_rate=html_movie.select_one('div.spc_score_area>a.spc>div.star_score>span.st_off>span.st_on') #기자,평론가 평점
    if(journalist_rate is None):
        journalist_rate=pymysql.NULL
    else:
        journalist_rate=float(journalist_rate['style'][6:-1])/10
    
    link_journalist = html_movie.select_one('div.sub_tab_area>ul.end_sub_tab>li:nth-child(5)>a').attrs['href']
    raw_journalist = requests.get('https://movie.naver.com/movie/bi/mi'+link_journalist[1:]).text
    html_journalist = BeautifulSoup(raw_journalist, 'html.parser')
    journalist_count=html_journalist.select_one('div.score_special>div.title_area>span.user_count>em')
    if(journalist_count is None):
        journalist_count=pymysql.NULL #기자,평론가 참여자
    else:
        journalist_count=journalist_count.text

    totalaudience=html_movie.select_one('div.mv_info>dl.info_spec>dd:nth-child(10)>div.step9_cont>p.count') #누적 관객
    if(totalaudience is None):
        totalaudience=pymysql.NULL
    else:
        totalaudience=totalaudience.text

    playing_time=html_movie.select_one('div.mv_info>dl.info_spec>dd:nth-child(2)>p>span:nth-child(3)') #상영시간
    if(playing_time is None):
        playing_time=pymysql.NULL
    else:
        playing_time=playing_time.text
        playing_time=re.sub(r"[\n\t\s]*", "", playing_time)

    opening_date=html_movie.select_one('div.mv_info>dl.info_spec>dd:nth-child(2)>p>span:nth-child(4)') #개봉일
    if(opening_date is None):
        opening_date=pymysql.NULL
    else:
        opening_date=opening_date.text
        opening_date=re.sub(r"[\n\t\s]*", "", opening_date)

    image_movie=html_movie.select_one('div.poster>a') #영화 이미지 주소
    if(image_movie is None):
        image_movie=pymysql.NULL
    else:
        image_movie=image_movie.find("img").get("src")
        insert_sql="""insert into movie(moviecode,title_movie,movie_rate,audience_rate,audience_count,
                    netizen_rate,netizen_count,journalist_rate,journalist_count,totalaudience
                    ,playing_time,opening_date,image_movie)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        movie=(moviecode,title_movie,movie_rate,audience_rate,audience_count,netizen_rate,netizen_count,
            journalist_rate,journalist_count,totalaudience,playing_time,opening_date,image_movie)
    
    print('영화코드:',moviecode,
        '\n제목:',title_movie,
        '\n등급:', movie_rate,
        '\n관람객 평점:',audience_rate,
        '\n관람객 참여자:',audience_count,
        '\n네티즌 평점:',netizen_rate,
        '\n네티즌 참여자:',netizen_count,
        '\n기자,평론가 평점:',journalist_rate,
        '\n기자,평론가 참여자:',journalist_count,
        '\n누적 관객:',totalaudience,
        '\n상영 시간:',playing_time,
        '\n개봉일:',opening_date,
        '\n이미지:',image_movie
    )
    
    cur_1.execute(insert_sql, movie) 
    conn_1.commit()
    print('movie table insert')
    # ####################################################################장르
    print()
    genre_movie=html_movie.select_one('div.mv_info>dl.info_spec>dd:nth-child(2)>p>span:nth-child(1)') #장르
    if(genre_movie is None):
        genre_movie=pymysql.NULL
    else:
        genre_movie=genre_movie.text
        genre_movie= re.sub(r"[\n\t\s]*", "", genre_movie).split(',')
        
    insert_sql="""insert into genre(moviecode,genre_movie)
                    values(%s, %s)"""    
        
    
    for i in range(0,len(genre_movie)):
        print('영화 코드:',moviecode,
            '\n장르:', genre_movie[i])
        genre=(moviecode,genre_movie[i])
        buffer_genre.append(genre)
        
    cur_2.executemany(insert_sql, buffer_genre)
    conn_2.commit()
    buffer_genre=[]
    print('genre table insert')
    # ####################################################################나라
    print()
    country_movie=html_movie.select_one('div.mv_info>dl.info_spec>dd:nth-child(2)>p>span:nth-child(2)') #나라
    if(country_movie is None):
        country_movie=pymysql.NULL
    else:
        country_movie=country_movie.text
        country_movie= re.sub(r"[\n\t\s]*", "", country_movie).split(',')
        
    insert_sql="""insert into country(moviecode,country_movie)
                    values(%s, %s)"""
                    
    for i in range(0,len(country_movie)):
        print('영화 코드:',moviecode,
            '\n나라:',country_movie[i])
        
        country=(moviecode,country_movie[i])
        buffer_country.append(country)
        print(country)
    cur_3.executemany(insert_sql, buffer_country)
    conn_3.commit()
    buffer_country=[]
    print('country table insert')
    ####################################################################감독
    print()
        
    name_director=html_movie.select_one('div.mv_info>dl.info_spec>dd:nth-child(4)')
    if(name_director is None):
        name_director=pymysql.NULL
    else:
        
        name_director=name_director.text
        name_director= re.sub(r"[\n\t\s]*", "", name_director).split(',')

    
    insert_sql="""insert into director(directorcode,moviecode,name_director,image_director)
                    values(%s, %s, %s, %s)"""
                      
    for i in range (1, len(name_director)+1) :
        link_director=html_movie.select_one('div.mv_info>dl.info_spec>dd:nth-child(4)>p>a:nth-child(%i)' % (i))
        
        if(link_director is None):
            link_director=pymysql.NULL
        else:
            link_director=link_director.attrs['href']
            link_director='https://movie.naver.com'+link_director        

        raw_director =requests.get(link_director).text
        html_director = BeautifulSoup(raw_director, 'html.parser')
        
        image_director = html_director.select_one('div.poster') #감독 사진
        if(image_director is None):
            image_director=pymysql.NULL
        else:
            image_director=image_director.find("img").get("src")
            
        directorcode=int(link_director.split('=')[1]) #감독 코드
        
        
        print('감독 코드:',directorcode,
            '\n영화 코드:',moviecode,
            '\n감독 이름:',name_director[i-1],
            '\n감독 사진:',image_director
        )
        director=(directorcode,moviecode,name_director[i-1],image_director)
        buffer_director.append(director)

    cur_4.executemany(insert_sql, buffer_director)
    conn_4.commit()
    buffer_director=[]
    print("director table insert")
    
    # ####################################################################배우
    print()
    link_actor=href.replace('basic','detail')
    raw_actor =requests.get(link_actor).text
    html_actor = BeautifulSoup(raw_actor, 'html.parser')
    alistCnt=html_actor.select('div.made_people>div.lst_people_area.height100>ul.lst_people>li')
    insert_sql="""insert into actor(actorcode,moviecode,name_actor,image_actor)
                    values(%s, %s, %s, %s)"""
    for i in range(1, len(alistCnt)+1):
        name_actor=html_actor.select_one('div.made_people>div.lst_people_area.height100>ul.lst_people>li:nth-child(%i)>div.p_info>a'% (i)) #배우 이름
        if(name_actor is None):
            name_actor=pymysql.NULL
        else:
            name_actor=name_actor.text
                    
        image_actor=html_actor.select_one('div.made_people>div.lst_people_area.height100>ul.lst_people>li:nth-child(%i)>p.p_thumb>a'% (i)) #배우 이미지
        if(image_actor is None):
            image_actor=pymysql.NULL
        else:
            image_actor=image_actor.find("img").get("src")
        
        actorcode=html_actor.select_one('div.made_people>div.lst_people_area.height100>ul.lst_people>li:nth-child(%i)>p.p_thumb>a'% (i)) #배우 코드
        if(actorcode is None):
            actorcode=pymysql.NULL
        else:
            actorcode=actorcode.attrs['href'].split('=')[1]
        
        moviecode= int(href.split('=')[1]) #영화코드

        print('배우 코드:',actorcode,
            '\n영화 코드:',moviecode,
            '\n배우 이름:',name_actor,
            '\n배우 사진:',image_actor
        )
        
        actor=(actorcode,moviecode,name_actor,image_actor)
        #print(actor)
        buffer_actor.append(actor)
    cur_5.executemany(insert_sql, buffer_actor)
    conn_5.commit()
    buffer_actor=[]
    print('actor table insert')
    
    # ####################################################################등장인물
    print()
    insert_sql="""insert into persona(moviecode,image_persona,star,name_persona,part_persona)
                    values(%s, %s, %s, %s, %s)"""
    for i in range(1, len(alistCnt)+1):
        star=html_actor.select_one('div.made_people>div.lst_people_area.height100>ul.lst_people>li:nth-child(%i)>div.p_info>div.part>p.in_prt>em.p_part'% (i)) #배우 이름
        if(star is None):
            star=pymysql.NULL
        else:
            star=star.text
        
        image_persona=html_actor.select_one('div.made_people>div.lst_people_area.height100>ul.lst_people>li:nth-child(%i)>p.p_thumb>a'% (i)) #배우 이미지
        if(image_persona is None):
            image_persona=pymysql.NULL
        else:
            image_persona=image_persona.find("img").get("src")
            
        part_persona=html_actor.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li:nth-child(%i) > div > div > p.pe_cmt > span'% (i)) #배역
        if(part_persona is None):
            part_persona=pymysql.NULL
        else:
            part_persona=part_persona.text[:-2]
            
        name_persona=html_actor.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li:nth-child(%i) > div > a'% (i)) #배우 이름
        if(name_persona is None):
            name_persona=pymysql.NULL
        else:
            name_persona=name_persona.text
            
        print('영화 코드:',moviecode,
            '\n배우 사진:',image_persona,
            '\n주연?:',star,
            '\n배우이름:',name_persona,
            '\n배역:',part_persona)
        
        
        persona=(moviecode,image_persona,star,name_persona,part_persona)
        buffer_persona.append(persona)
    
    cur_6.executemany(insert_sql, buffer_persona)
    conn_6.commit()
    buffer_persona=[]
    print('persona table insert')
            
    
    ####################################################################명대사
    print()
    link_line=href.replace('basic','script')
    link_line=link_line+'&order=best&nid=&page='
    raw_line =requests.get(link_line).text
    html_line = BeautifulSoup(raw_line, 'html.parser')
    lLineCnt=html_line.select_one('div.top_behavior.no_border>span.cnt>em').text
    insert_sql="""insert into line(moviecode,image_line,bestline,part_line,name_line,writer_line,likecnt,makingdate_line)
                    values(%s, %s, %s, %s, %s, %s, %s, %s)"""
                    
    for i in range(1,math.ceil(int(lLineCnt)/10)+1):
        lList=html_line.select('div.ifr_area>ul.lines>li')
        for j in range(1, len(lList)+1):
            bestline=html_line.select_one('div.ifr_area>ul.lines>li:nth-child(%i)>div.lines_area2>p.one_line'% (j)) #명대사
            if(bestline is None):
                bestline=pymysql.NULL
            else:
                bestline=bestline.text
            
            image_line=html_line.select_one('div.ifr_area>ul.lines>li:nth-child(%i)>p.thumb>a'% (j)) #사진
            if(image_line is None):
                image_line=pymysql.NULL
            else:
                image_line=image_line.find("img").get("src")
                
            part_line=html_line.select_one('div.ifr_area>ul.lines>li:nth-child(%i)>div.lines_area2>p.char_part>span'% (j)) #극중이름
            if(part_line is None):
                part_line=pymysql.NULL
            else:
                part_line=part_line.text
            
            name_line=html_line.select_one('div.ifr_area>ul.lines>li:nth-child(%i)>div.lines_area2>p>a'% (j)) #배우이름
            if(name_line is None):
                name_line=pymysql.NULL
            else:
                name_line=name_line.text
                
            writer_line=html_line.select_one('div.ifr_area>ul.lines>li:nth-child(%i)>div.lines_area2>p.etc_lines>span>a'% (j)) #작성자
            if(writer_line is None):
                writer_line=pymysql.NULL
            else:
                writer_line=writer_line.text
                
            likecnt=html_line.select_one('div.ifr_area>ul.lines>li:nth-child(%i)>div.lines_area2>p.etc_lines>span.w_recomm>em'% (j)) #추천수
            if(likecnt is None):
                likecnt=pymysql.NULL
            else:
                likecnt=likecnt.text
                
            makingdate_line=html_line.select_one('div.ifr_area>ul.lines>li:nth-child(%i)>div.lines_area2>em.date'% (j)) #작성 날짜
            if(makingdate_line is None):
                makingdate_line=pymysql.NULL
            else:
                makingdate_line=makingdate_line.text
                
            print('영화코드:',moviecode,
                '\n사진:',image_line,
                '\n대사:',bestline,
                '\n극중이름:',part_line,
                '\n배우이름:',name_line,
                '\n작성자:',writer_line,
                '\n추천수:',likecnt,
                '\n작성 날짜:',makingdate_line)
            
            line=(moviecode,image_line,bestline,part_line,name_line,writer_line,likecnt,makingdate_line)
            buffer_line.append(line)
    
    cur_7.executemany(insert_sql, buffer_line)
    conn_7.commit()
    buffer_line=[]
    print('line table insert')        
    
            
            
    ####################################################################포토
    print()
    link_photo=href.replace('basic','photo')
    raw_photo =requests.get(link_photo).text
    html_photo = BeautifulSoup(raw_photo, 'html.parser')
    photoCnt=html_photo.select_one('div.photo>div.title_area>span.count>em').text
    insert_sql="""insert into photo(moviecode,image_photo)
                    values(%s, %s)"""
    for i in range(1, math.ceil(int(photoCnt)/18)+1):
        photoList=html_photo.select('div.gallery_group>ul#gallery_group>li')
        for j in photoList:
            
            if(j is None):
                image_photo=pymysql.NULL
            else:
                image_photo=j.find("img").get("src") #감독 사진
                
            print('영화 코드:',moviecode,
                  '\n사진 URL:',image_photo)
            
            photo=(moviecode,image_photo)
            buffer_photo.append(photo)
    cur_8.executemany(insert_sql, buffer_photo)
    conn_8.commit()
    print("photo table insert")
    buffer_photo=[]            
        
    ####################################################################리뷰
    print()
    link_review=href.replace('basic','review')
    raw_review =requests.get(link_review).text
    html_review = BeautifulSoup(raw_review, 'html.parser')
    rCnt=html_review.select_one('div.review>div.top_behavior>span.cnt>em')
    
    if(rCnt is None):
        rCnt=pymysql.NULL
    else:
        rCnt=int(rCnt.text)
    
    insert_sql="""insert into review(moviecode,title_review,writer_review,makingdate_review,hits,content)
                    values(%s, %s, %s, %s, %s, %s)"""
    for i in range(1,math.ceil(rCnt/10)+1):
        rList=html_review.select('div.review>ul.rvw_list_area>li')
        for j in range(1, len(rList)+1):
            print()
            title_review=html_review.select_one('div.review>ul.rvw_list_area>li:nth-child(%i)>a>strong'% (j)) #리뷰 타이틀
            if(title_review is None):
                title_review=pymysql.NULL
            else:
                title_review=title_review.text
                
            writer_review=html_review.select_one('div.review>ul.rvw_list_area>li:nth-child(%i)>span.user>a'% (j)) #작성자
            if(writer_review is None):
                writer_review=pymysql.NULL
            else:
                writer_review=writer_review.text
            
            makingdate_review=html_review.select_one('div.review>ul.rvw_list_area>li:nth-child(%i)>span.user>em'% (j)) #작성 날짜
            if(makingdate_review is None):
                makingdate_review=pymysql.NULL
            else:
                makingdate_review=makingdate_review.text
                
            hits=html_review.select_one('div.review>ul.rvw_list_area>li:nth-child(%i)>span.user'% (j)) #추천수
            if(hits is None):
                hits=pymysql.NULL
            else:
                hits=hits.text.split('추천')
                
            content=html_review.select_one('div.review>ul.rvw_list_area>li:nth-child(%i)>p>a'% (j)) #내용
            if(content is None):
                content=pymysql.NULL
            else:
                content=content.text
            
            print('영화코드:',moviecode,
                  '\n리뷰 타이틀:',title_review,
                  '\n작성자:',writer_review,
                  '\n작성 날짜:',makingdate_review,
                  '\n추천수:',hits[1],
                  '\n내용:',content)
            
            review=(moviecode,title_review,writer_review,makingdate_review,hits[1],content)
            buffer_review.append(review)
    cur_9.executemany(insert_sql, buffer_review)
    conn_9.commit()
    buffer_review=[]  
    print("review table insert")        
                 
    
if __name__ == '__main__':
    get_rankingmovie()