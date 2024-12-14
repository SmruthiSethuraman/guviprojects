import requests
import pymysql
Api_key="AIzaSyBsOKDS6sE_ymn1l7imdBTzcOYgAV--ESY" ## API KEY STORED IN A VARIABLE TO EXTRACT DATA FROM GOOGLE API
i=1
## Establishing MySQL Connection
connection=pymysql.connect(
            host='localhost',
            user='root',
            password='F@27S@23A@12',
            database='DSPROJECT')
mycursor=connection.cursor() # initialising the cursor 

## Function to extract json data from Google API

def extract_json(book_category,api_key,i):
    url="https://www.googleapis.com/books/v1/volumes"
    params={"q": book_category,
    "key":api_key,
    "startIndex":i,
    "maxResults":40}
    response=requests.get(url,params)
    return response

# Funtion to convert the json data into a list

def extract_data_from_json(data,searchkey):
    sk=searchkey
    all_list=[]
    for i in data['items']:
        if i['volumeInfo'].get('industryIdentifiers'):
            ind_identifier=i['volumeInfo']['industryIdentifiers'][0]['type'] 
        else:
            ind_identifier='NA'
        if i['saleInfo'].get('listPrice'):
            amount_listprice=i['saleInfo']['listPrice']['amount']
            currencycode_listprice=i['saleInfo']['listPrice']['currencyCode']      
        else:
            amount_listprice=0
            currencycode_listprice='NA'
        if i['saleInfo'].get('retailPrice'):
            amount_retailPrice=i['saleInfo']['retailPrice']['amount']
            currencycode_retailPrice=i['saleInfo']['retailPrice']['currencyCode']          
        else:
            amount_retailPrice=0
            currencycode_retailPrice='NA'
        if i['volumeInfo'].get('imageLinks'):
            image_links=i['volumeInfo']['imageLinks']['thumbnail']           
        else:
            image_links='NA'
        if i['volumeInfo'].get('categories'):
            categories=str(i['volumeInfo']['categories']) 
        else:       
            categories='NA'
        all_list.append({'id':i['id'],'search_key':sk,'title':i['volumeInfo'].get('title','NA'),
                         'subtitle':i['volumeInfo'].get('subtitle','NA'),
                         'author':str(i['volumeInfo'].get('authors','NA')),
                         'Pubisher':i['volumeInfo'].get('publisher','NA'),
                         'descrp':i['volumeInfo'].get('description','NA'),
                         'ind_identifier':ind_identifier,
                         'text_readingmode':i['volumeInfo']['readingModes']['text'],
                         'image_readingmode':i['volumeInfo']['readingModes']['image'],
                         'page_count':i['volumeInfo'].get('pageCount',0),
                         'categories':categories,
                         'language':i['volumeInfo']['language'],
                         'image_links':image_links,
                         'country':i['saleInfo']['country'],
                         'saleability':i['saleInfo']['saleability'],
                         'is_ebook':i['saleInfo']['isEbook'],
                         "ratingsCount":i['volumeInfo'].get('ratingsCount',0),
                         'average_rating':i['volumeInfo'].get('averageRating',0),
                         'amount_listprice':amount_listprice,
                         'currencycode_listprice':currencycode_listprice,
                         'amount_retailprice':amount_retailPrice,
                         'currencycode_retailprice':currencycode_retailPrice,
                         'buy_link':i['saleInfo'].get('buyLink','NA'),
                         'year':i['volumeInfo'].get('publishedDate','NA')})
    return all_list
# streamlit app code
import pandas as pd
import streamlit as st
import base64
# To Set the Background Image

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("C:/Users/SESA742087/Desktop/bookimage2.jpg")

st.markdown("<h1 style 'color:brown;'>THE BOOK STORE</h1>",unsafe_allow_html=True) # setting the app title

p=st.sidebar.radio("## Navigation",['BookSearch','FAQ']) #setting the sidebar 

# To create table & insert data in to the table 

if p=='BookSearch':
    #st.image("C:/Users/SESA742087/Desktop/bookimage")
    st.balloons()
    sc=st.text_input("Enter the category of books to be searched")
    if st.button("Search"):
        while i<=500:
            json_data=extract_json(sc,Api_key,i)
            data=json_data.json()
            l=extract_data_from_json(data,sc)
            connection=pymysql.connect(
            host='localhost',
            user='root',
            password='F@27S@23A@12',
            database='DSPROJECT')
            

            

            mycursor.execute("""
            CREATE TABLE IF NOT EXISTS BOOKS(
            ID VARCHAR(255) PRIMARY KEY,
            SEARCH_KEY VARCHAR(255),
            BOOK_TITLE VARCHAR(255),
            BOOK_SUBTITLE TEXT,
            BOOK_AUTHORS TEXT,
            BOOK_PUBLISHER TEXT,                 
            BOOK_DESCRIPTION TEXT,
            BOOK_INDUSTRYIDENTIFIERS TEXT,
            TEXT_READINGMODE BOOL,
            IMAGE_READINGMODE BOOL,
            PAGECOUNT INT,
            CATEGORIES TEXT,
            LANGUAGE VARCHAR(50),
            IMAGELINKS TEXT,
            COUNTRY VARCHAR(100),
            SALEABILITY VARCHAR(50),
            ISEBOOK BOOL,
            RATINGS_COUNT INT,
            AVERAGE_RATING INT,                               
            AMOUNT_LISTPRICE DECIMAL(10,2),
            CURRENCYCODE_LISTPRICE VARCHAR(10),
            AMOUNT_RETAILPRICE DECIMAL(10,2),
            CURRENCYCODE_RETAILPRICE VARCHAR(10),
            BUYLINK TEXT,
            PUBLICATION_YEAR VARCHAR(10));
            """  )
            
            values=pd.DataFrame(l)
            #st.write(values)
            #mycursor.executemany(squery,values)
            #mycursor.execute("SELECT * FROM BOOKS")

            
            for index,row in values.iterrows():
                squery = """INSERT INTO BOOKS (ID,SEARCH_KEY,BOOK_TITLE,BOOK_SUBTITLE,BOOK_AUTHORS,BOOK_PUBLISHER,BOOK_DESCRIPTION,BOOK_INDUSTRYIDENTIFIERS,TEXT_READINGMODE,
                        IMAGE_READINGMODE,PAGECOUNT,CATEGORIES,LANGUAGE,IMAGELINKS,COUNTRY,SALEABILITY,ISEBOOK,RATINGS_COUNT,AVERAGE_RATING,AMOUNT_LISTPRICE,CURRENCYCODE_LISTPRICE,AMOUNT_RETAILPRICE,
                        CURRENCYCODE_RETAILPRICE,BUYLINK,PUBLICATION_YEAR) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
                        ID=VALUES(ID),SEARCH_KEY=VALUES(SEARCH_KEY),BOOK_TITLE=VALUES(BOOK_TITLE),BOOK_SUBTITLE=VALUES(BOOK_SUBTITLE),BOOK_AUTHORS=VALUES(BOOK_AUTHORS),BOOK_PUBLISHER=VALUES(BOOK_PUBLISHER),
                        BOOK_DESCRIPTION=VALUES(BOOK_DESCRIPTION),BOOK_INDUSTRYIDENTIFIERS=VALUES(BOOK_INDUSTRYIDENTIFIERS),TEXT_READINGMODE=VALUES(TEXT_READINGMODE),IMAGE_READINGMODE=VALUES(IMAGE_READINGMODE),
                        PAGECOUNT=VALUES(PAGECOUNT),CATEGORIES=VALUES(CATEGORIES),LANGUAGE=VALUES(LANGUAGE),IMAGELINKS=VALUES(IMAGELINKS),COUNTRY=VALUES(COUNTRY),SALEABILITY=VALUES(SALEABILITY),
                        ISEBOOK=VALUES(ISEBOOK),RATINGS_COUNT=VALUES(RATINGS_COUNT),AMOUNT_LISTPRICE=VALUES(AMOUNT_LISTPRICE),CURRENCYCODE_LISTPRICE=VALUES(CURRENCYCODE_LISTPRICE),
                        AMOUNT_RETAILPRICE=VALUES(AMOUNT_RETAILPRICE),CURRENCYCODE_RETAILPRICE=VALUES(CURRENCYCODE_RETAILPRICE),BUYLINK=VALUES(BUYLINK),PUBLICATION_YEAR=VALUES(PUBLICATION_YEAR)"""
                mycursor.execute(squery,tuple(row))          
            i=i+40
# to display the stroed data in a table format
        mycursor.execute(""" SELECT * FROM BOOKS """)
        myresults=mycursor.fetchall()
        col=[desc[0] for desc in mycursor.description]
        connection.commit()
        mycursor.close()
        connection.close()
        df=pd.DataFrame(myresults,columns=col)
        st.write(df)
# To retrive data from databse (execute any of the 20 queries)
       
if p=="FAQ":
    q=st.selectbox('General Queries',["Check Availability of eBooks vs Physical Books","Find the publisher with most books published","Identify the publisher with Highest Average Rating","Top 5 Most Expensive Books",
    "Books Published After 2010 with at Least 500 Pages","List Books with Discounts Greater than 20%","Find the Average Page Count for eBooks vs Physical Books","Find the Top 3 Authors with the Most Books",
    "List Publishers with More than 10 Books","Find the Average Page Count for Each Category","Retrieve Books with More than 3 Authors","Books with Ratings Count Greater Than the Average","Books with the Same Author Published in the Same Year",
    "Books with a Specific Keyword in the Title","Year with the Highest Average Book Price","Count Authors Who Published 3 Consecutive Years","Find authors who have published books in the same year but under different publishers",
    "find the average amount_retailPrice of eBooks and physical books","Identify books that have an averageRating that is more than two standard deviations away from the average rating of all books",
    "Determine which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books"])
    if st.button("Go"):
        if q=="Find the publisher with most books published":
            mycursor.execute(""" SELECT BOOK_PUBLISHER,count(*) AS BOOK_COUNT FROM BOOKS 
                             WHERE book_publisher IS NOT NULL AND book_publisher != 'NA'
                             GROUP BY BOOK_PUBLISHER ORDER BY BOOK_COUNT DESC
                             LIMIT 1""")
           
        elif q=="Identify the publisher with Highest Average Rating":
            mycursor.execute(""" SELECT BOOK_PUBLISHER FROM BOOKS 
                             ORDER BY AVERAGE_RATING DESC
                             LIMIT 1""")
            
        elif q=="Top 5 Most Expensive Books":
            mycursor.execute(""" SELECT BOOK_TITLE FROM BOOKS 
                             ORDER BY AMOUNT_RETAILPRICE DESC
                             LIMIT 5""")

        elif q=="Books Published After 2010 with at Least 500 Pages":
            mycursor.execute("""SELECT ID,BOOK_TITLE FROM BOOKS WHERE
                             PUBLICATION_YEAR>2010 AND PAGECOUNT>=500""" )
        
        elif q=="Find the Top 3 Authors with the Most Books":
            mycursor.execute("""SELECT BOOK_AUTHORS  FROM BOOKS 
                             ORDER BY AMOUNT_RETAILPRICE DESC LIMIT 3""" )

        elif q=="List Publishers with More than 10 Books":
              mycursor.execute("""SELECT BOOK_PUBLISHER  FROM BOOKS 
                             GROUP BY BOOK_PUBLISHER HAVING COUNT(ID)>10""" )

        elif q=="Find the Average Page Count for Each Category":
             mycursor.execute("""SELECT CATEGORIES,AVG(PAGECOUNT) AS AVERAGE_PAGE_COUNT
                             FROM BOOKS GROUP BY CATEGORIES
                              """ )

        elif q=="Books with Ratings Count Greater Than the Average":    
                mycursor.execute("""SELECT ID,BOOK_TITLE
                             FROM BOOKS WHERE RATINGS_COUNT>AVERAGE_RATING
                              """ )   

        elif q=="Year with the Highest Average Book Price" :
                mycursor.execute("""SELECT PUBLICATION_YEAR FROM BOOKS
                               GROUP BY PUBLICATION_YEAR ORDER BY AVG(AMOUNT_RETAILPRICE)
                               LIMIT 1 """ )   

        elif q=="Find authors who have published books in the same year but under different publishers":
                 mycursor.execute("""SELECT BOOK_AUTHORS,PUBLICATION_YEAR,COUNT(ID) AS COUNT_OF_BOOKS FROM BOOKS
                               GROUP BY BOOK_AUTHORS ,PUBLICATION_YEAR 
                               """ ) 

        elif q=="Determine which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books":
               mycursor.execute("""SELECT BOOK_PUBLISHER,AVERAGE_RATING,COUNT(ID) AS NUMBER_OF_BOOKS FROM BOOKS GROUP BY BOOK_PUBLISHER,AVERAGE_RATING
                               HAVING COUNT(ID)>10 ORDER BY AVERAGE_RATING DESC 
                               """ )   
               
        elif q=="Check Availability of eBooks vs Physical Books":
             mycursor.execute(""" SELECt COUNT(CASE WHEN ISEBOOK=1 THEN ID END)AS EBOOK_AVAILABLITY,
                               COUNT(CASE WHEN TEXT_READINGMODE=1 THEN ID END) AS PHUSICALBOOK_AVAILABILITY
                              FROM BOOKS""")

        elif q=="List Books with Discounts Greater than 20%":
             mycursor.execute(""" SELECT ID, BOOK_TITLE,AMOUNT_LISTPRICE,AMOUNT_RETAILPRICE,((AMOUNT_LISTPRICE- AMOUNT_RETAILPRICE)/AMOUNT_LISTPRICE)*100 AS
                                DISCOUNT_PERCENTAGE FROM BOOKS
                                WHERE (((AMOUNT_LISTPRICE- AMOUNT_RETAILPRICE)/AMOUNT_LISTPRICE)*100)>20""")

        elif q=="Count Authors Who Published 3 Consecutive Years":
             mycursor.execute(""" WITH consecutive_years AS (
                                SELECT book_authors,publication_Year,
                                LEAD(publication_Year, 1) OVER (PARTITION BY book_authors ORDER BY publication_Year) AS next_year,
                                LEAD(publication_Year, 2) OVER (PARTITION BY book_authors ORDER BY publication_Year) AS next_next_year FROM BOOKS)
                                SELECT COUNT(DISTINCT book_authors) AS author_count FROM consecutive_years WHERE 
                                next_year = publication_Year + 1
                                AND next_next_year = publication_Year + 2 """)
    
        elif q=="Find the Average Page Count for eBooks vs Physical Books":
             mycursor.execute(""" SELECT AVG(CASE WHEN ISEBOOK=1 THEN pageCount END) AS avg_ebook_page_count,
                                 AVG(CASE WHEN TEXT_READINGMODE= 1 THEN pageCount END) AS avg_physical_page_count
                                 FROM books """ )
             
        elif q=="Retrieve Books with More than 3 Authors":
             mycursor.execute("""SELECT book_title, book_authors,publication_Year FROM books
                               WHERE (LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1) > 3""") 
   
        elif q=="Books with the Same Author Published in the Same Year":
             mycursor.execute("""SELECT book_authors,publication_Year,GROUP_CONCAT(book_title) AS TITLES FROM 
                              books GROUP BY book_authors, publication_Year HAVING COUNT(*) > 1""")
    
        elif q=="Find authors who have published books in the same year but under different publishers":
             mycursor.execute("""SELECT BOOK_AUTHORS, PUBLICATION_YEAR, COUNT(*) AS BOOK_COUNT FROM     (SELECT DISTINCT BOOK_AUTHORS, PUBLICATION_YEAR, BOOK_PUBLISHER
                                FROM books) AS distinct_books GROUP BY BOOK_AUTHORS, PUBLICATION_YEAR HAVING COUNT(BOOK_PUBLISHER) > 1""")
 
        elif q=="find the average amount_retailPrice of eBooks and physical books":
             mycursor.execute(""" SELECT AVG(CASE WHEN ISEBOOK=1 THEN AMOUNT_RETAILPRICE END)AS AVERAGE_EBOOK_PRICE ,
                              AVG(CASE WHEN TEXT_READINGMODE=1 THEN AMOUNT_RETAILPRICE END)ASAVERAGE_PHYSICALBOOK_PRICE
                              FROM BOOKS""")
        
        elif q=="Identify books that have an averageRating that is more than two standard deviations away from the average rating of all books":
             mycursor.execute("""WITH stats AS (SELECT AVG(average_Rating) AS avg_rating,STDDEV(average_Rating) AS stddev_rating FROM books)
                              SELECT book_title,average_Rating,ratings_Count FROM books, stats WHERE average_Rating > avg_rating + 2 * stddev_rating
                            OR average_Rating < avg_rating - 2 * stddev_rating""")

        elif q=="Books with a Specific Keyword in the Title":
            query="SELECT BOOK_TITLE,BOOK_AUTHORS FROM BOOKS WHERE BOOK_TITLE LIKE CONCAT(('%'+ SEARCH_KEY +'%'))"
            mycursor.execute(query)
    
     
        else:
            st.warning("Please select a query")    
# To display the extracted data

        results=mycursor.fetchall()
        col=[desc[0] for desc in mycursor.description]
        connection.commit()
        mycursor.close()
        connection.close()
        df=pd.DataFrame(results,columns=col)
        st.write(df)


