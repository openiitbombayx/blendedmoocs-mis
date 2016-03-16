'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


from django.contrib.sessions.models import Session
from tracking.models import Visitor
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from SIP.views import *
#import pytz 
from pytz import timezone
class Concurrentloginrestrict(object):
      def process_request(self,request):
        if request.user.is_authenticated():
          userip=request.META.get('REMOTE_ADDR','')
          try:
              lastlogin=request.user.last_login
          except:
                lastlogin=datetime(4712,12,31,0,0).replace(tzinfo=timezone('UTC'))
          print (datetime.now(timezone('UTC'))-lastlogin).total_seconds(),datetime.now(timezone('UTC')),"hello",lastlogin
          if 0<=(datetime.now(timezone('UTC'))-lastlogin).total_seconds()<5:#unicode(lastlogin)[:19]==unicode(timezone.now())[:19]:
              oldvisitorobj=Visitor.objects.filter(user=request.user).exclude(ip_address=userip)
              for i in oldvisitorobj:
                  Session.objects.filter(session_key=i.session_key).delete()
                  i.user=None
                  i.save()
                  
                  
          
        else:
             return loginn(request)
