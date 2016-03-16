from __future__ import division
from django import template


#templatedivision will be used on templates used in this way:{{ 4|templatedivision:3 }} & {% load sip_filters %} in your html top, it will return float with upto two decimal places
register = template.Library()
@register.filter(name='templatedivision')
def templatedivision(value1,value2): 
     try:
        if value2:
            res=round(value1/value2, 2)
     except:
            pass
     return res

#convertpertonum will be used on templates used in this way:{{ 80|convertpertonum:10 }} & {% load sip_filters %} in your html top, it will return float with upto two decimal places
register = template.Library()
@register.filter(name='convertpertonum')
def convertpertonum(per,total): 
     try:
        
            res=round((per*total)/100, 2)
     except:
            pass
     return res

    
