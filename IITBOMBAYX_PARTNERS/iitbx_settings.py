'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


import pymongo
import MySQLdb
import argparse,re,datetime
import sys, getopt,os
import django
import time
from datetime import date, timedelta
#Please add the full project folder pwd
project_dir="bmwinfo/IITBOMBAYX_PARTNERS"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE']='IITBOMBAYX_PARTNERS.settings'
django.setup()


from pymongo import MongoClient
from django.db import models,transaction
from django.core.mail.message import EmailMultiAlternatives
from SIP.models import *


mysql_host="localhost"
#please enter mysq username password
user="iitbxblended"
passwd="11tbx@123"
mysql_schema="edxapp"
mongodb='mongodb://localhost:27017/'
courses=["CS101.1xA15","ME209xA15","EE210.1xA15"]
