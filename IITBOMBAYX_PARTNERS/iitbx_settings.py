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
from django.db import transaction
from datetime import date, timedelta
from collections import *
import collections
#Please add the full project folder pwd
#project_dir="bmwinfo/IITBOMBAYX_PARTNERS"
project_dir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE']='IITBOMBAYX_PARTNERS.settings'
django.setup()
num_days=4

from pymongo import MongoClient
from django.db import models,transaction
from django.core.mail.message import EmailMultiAlternatives
from SIP.models import *
from iitbx.models import *
from managerapp.models import *

mysql_host="localhost"
#please enter mysq username password
user=""
passwd=""
mysql_schema="edxapp"
mongodb='mongodb://localhost:27017/'
courses=["i4x/IITBombayX/CS101.1xA15/2015_T1","i4x/IITBombayX/ME209xA15/2015_T1","i4x/IITBombayX/EE210.1xA15/2015_T1","i4x/IITBombayX/CS101.1xS16/2016_T1","i4x/IITBombayX/EE210xS16/2016_T1","i4x/IITBombayX/ME209xS16/2016_T1","i4x/IITBombayX/HS791xS16/2016_T1"]
