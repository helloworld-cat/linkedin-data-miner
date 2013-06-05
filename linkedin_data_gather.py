###
#
# Input: database, collection, linkedin url field
#
# Requirements: MongoDB, pymongo, BeautifulSoup4
#
# Given all inputs, connect to the Mongo database, select the collection, loop through all records in the database 
#   getting the linkedin page url. Once it has that, gather the desired linkedin infromation, and update the record
#   in Mongo
#
# Usage: python linkedin_data_gather.py [db collection record linkedin_url_field]
#
###

import sys
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib2
from bs4 import BeautifulSoup
import time

if __name__ == '__main__':

  # The Mongo database to connect to
  db_to_use = sys.argv[1]
  # The collection to use
  collection_to_use = sys.argv[2]
  # The LinkedIn URL field in your Mongo database
  linkedin_url_field = sys.argv[3]

  # Connect to the database
  client = MongoClient()
  db = client[db_to_use]
  collection = db[collection_to_use]

  # Get a list of all the records in the database - we need to update everything
  # Fetch the record and get the linkedin url
  for item in collection.find():
    
    # Fetch the record and get the linkedin url
    record_id = ObjectId(item["_id"])
    url_to_get = item[linkedin_url_field]

    print "Current ObjectID: " + str(record_id)
    print "Current URL: " + url_to_get

    if url_to_get != "N/A":
      # Get the HTML contents of the page and put it into BeautifulSoup
      opener = urllib2.build_opener()
      opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
      li_company_page = opener.open(url_to_get).read()
      soup = BeautifulSoup(li_company_page.decode('utf-8', 'ignore'))

      # Get the company description & specialties from the soup
      basic_li_data = soup.find(attrs = { "class" : "text-logo"})

      if basic_li_data:
        # Get the description
        description = basic_li_data.contents[1].text if basic_li_data else "N/A"

        # Get the specialities
        specialties = basic_li_data.contents[5].text.strip().replace("\n", "") if basic_li_data and len(basic_li_data) >= 5 else "N/A"
  
      # Potential data to get: website, type, founded, industry, company size
      raw_li_data = soup.find_all(["dt", "dd"])
      if raw_li_data:
        clean_li_data = []
        for x in range(len(raw_li_data)):
          clean_li_data.append(raw_li_data[x].text.strip())

        all_li_data = dict(clean_li_data[i:i+2] for i in range(0, len(clean_li_data), 2))

        company_size = all_li_data['Company Size'] if 'Company Size' in all_li_data else "N/A"
        website_url = all_li_data['Website'] if 'Website' in all_li_data else "N/A"
        industry = all_li_data['Industry'] if 'Industry' in all_li_data else "N/A"
        company_type = all_li_data['Type'] if 'Type' in all_li_data else "N/A"
        year_founded = all_li_data['Founded'] if 'Founded' in all_li_data else "N/A"

      # Let's update the record in the database

      try:
        collection.update( { '_id': ObjectId(record_id)}, {"$set": {'linkedin_description': description,
                                                                    'linkedin_specialties': specialties,
                                                                    'company_size': company_size,
                                                                    'website_url': website_url,
                                                                    'industry': industry,
                                                                    'company_type': company_type,
                                                                    'year_founded': year_founded}})
        print "Database updated. Oh yeah!!!"
      except:
        print "Sorry, I couldn't update the database because ", sys.exc_info()[0]
        raise

      # Let's not get banned by LI. Pause for 15 seconds
      time.sleep(15)