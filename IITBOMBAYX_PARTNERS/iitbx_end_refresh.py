from iitbx_settings import *

Lookup.objects.filter(category='Refresh Status',code=1).update(description='Off')
