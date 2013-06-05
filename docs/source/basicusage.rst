===========
Basic Usage
===========

Using the script is fairly straight forward. Assuming you have a running MongoDB database with a collection of companies complete with a LinkedIn company page url:

#. Open up a terminal session
#. Change to the directory where linkedin_data_gather.py sits
#. Run this command:

./linkedin_data_gather.py [database_name] [collection_name] [linkedin_url_field]

-------------
Example Usage
-------------

./linkedin_data_gather.py client_database all_clients linkedin_company_url