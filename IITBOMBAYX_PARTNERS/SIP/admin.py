'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''
from django.contrib import admin
from django.db import models as dmodels

from SIP import models 


#get the models from myproject.models]
mods = [x for x in models.__dict__.values() if issubclass(type(x), dmodels.base.ModelBase)]

admins = []
#for each model in our models module, prepare an admin class
#that will edit our model (Admin<model_name>, model) 
for c in mods: 
	admins.append(("%sAdmin"%c.__name__, c))

#create the admin class and register it
for (ac, c) in admins:
    try: #pass gracefully on duplicate registration errors
        admin.site.register(c, type(ac, (admin.ModelAdmin,), dict()))
    except:
        pass

