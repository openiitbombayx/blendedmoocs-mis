
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

