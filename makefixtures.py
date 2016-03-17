import JSONField
from datetime import datetime
import os
from Decimal import decimal as D


snapshotids = [
    244881,244882,244887,244976,244977,244978,244979,244980,
    244981,244982,244984,244985,
    245122,245123,245124, 245128,245129,245130,245133,245134,245135
]
systemnames = [
    '2016-T-01A','2016-T-02A','2016-T-03T','2016-T-04A','2016-T-05T','2016-T-06T','2016-T-07T','2016-T-08T',
    '2016-T-09A','2016-T-10A','2016-T-11A','2016-T-12T',
    '2016-T-13A', '2016-T-14T', '2016-T-15A','2016-T-16T', '2016-T-17A', '2016-T-18T', '2016-T-19T',
    '2016-T-20T','2016-T-21T'
]

def getsnapshotidfromsystemname(sname):
    try:
        return snapshotids.index(systenames.index(sname))
    except IndexError as e:
        print(e)

#wait for K
def buildsystems():
    ct = 0
    jsonsystems = list()
    for f in dir(s):
        #open file
        _s={
        'pk': ct+1,
        'model': 'system',
        'fields': {
            "systemname": systemname,
            "snapshotid": getsnapshotidfromsystemname(systemname),
            "description": description,
            "isActive": True,
            "isTurf": isTurf,
            "exposure": exposure,
            "query": query,
            # "_created": datetime.utcnow()
                }
        }
        ct+=1
        jsonsystems.append(_s)
        #write to 'fixtures/systems.json'
def buildsnapshot():
    ##lOOP OVER FIELDS AND ADD 
    pass



def buildfunds():
    fund1 = {
    "pk": 1,
    "model": "fund",
    "fields": {
      "name": "Brownrock GBP",
      "code": "BR",
      "description": """
        Nullam non euismod risus. Pellentesque non velit vitae tortor scelerisque congue at vitae nibh. Curabitur imperdiet purus vel felis iaculis, eu lacinia ante aliquet. Praesent accumsan, nisi sit amet volutpat posuere, leo nulla posuere dolor, quis maximus elit lorem quis odio. Ut a fermentum sem. Praesent non mauris odio. Donec sit amet dignissim justo. Maecenas elit enim, faucibus sed augue et, vestibulum pulvinar tortor. In hac habitasse platea dictumst. Vivamus scelerisque sollicitudin iaculis. Duis ante urna, consequat et consequat id, laoreet at augue. Duis nec convallis eros. Nam eu lectus condimentum libero egestas cursus. Interdum et malesuada fames ac ante ipsum primis in faucibus.
      """,
      "managementfee":0.02,
      "performancefee": 0.02,
      "performancethreshold": 0.245,
      "bailoutfee": 0.1,
      "initialshareissue": 10,
      "sharespurchased": 0,
      "initialshareprice": 100.0,
      "currentshareprice": 100.0,
      "intialpricepershare": D('100.00'),
      "currency": "GBP",
      "openingbank": D('1000.00'),
      "currentbalance": D('1000.00'),
      "liveroi": 0.0,
      "livesince": datetime.strpftime("20160401", "%Y%m%d"),
      },
    fund2 = {
    "pk": 2,
    "model": "fund",
    "fields": {
      "name": "Schwarzmann AUD",
      "code": "BR",
      "description": """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus pulvinar dui eros, non eleifend urna varius vitae. Vivamus varius posuere elementum. Sed nec elementum nibh, sit amet aliquam purus. Pellentesque fringilla, mi ut auctor commodo, quam neque rutrum lectus, id euismod odio velit non nibh. Sed eget eros vel dui imperdiet tincidunt ut ut est. Donec malesuada gravida pretium. Suspendisse nisl ante, pellentesque ut consectetur sit amet, suscipit nec nunc. Praesent quis lobortis erat. Ut non efficitur erat. Maecenas ligula risus, auctor quis odio vitae, ornare mollis tortor. Integer suscipit metus nulla, ac accumsan felis placerat sit amet. Vivamus vestibulum justo ac lorem luctus pellentesque. Nunc egestas aliquam est a placerat. Quisque lobortis est lacus, quis laoreet neque ornare vel. Donec sodales convallis nibh, nec porta mi tincidunt vel.
      """,
      "managementfee":0.02,
      "performancefee": 0.02,
      "performancethreshold": 0.245,
      "bailoutfee": 0.1,
      "initialshareissue": 10,
      "sharespurchased": 0,
      "initialshareprice": 100.0,
      "currentshareprice": 100.0,
      "intialpricepershare": D('100.00'),
      "currency": "AUD",
      "openingbank": D('1000.00'),
      "currentbalance": D('1000.00'),
      "liveroi": 0.0,
      "livesince": datetime.strpftime("20160401", "%Y%m%d"),
      },
    fund3 = {
    "pk": 3,
    "model": "fund",
    "fields": {
      "name": "Hotshots AUD",
      "code": "BR",
      "description": """
        10 best performing systems bundled into a single, dynamic system
      """,
      "isActive": False,
      "managementfee":0.02,
      "performancefee": 0.02,
      "performancethreshold": 0.245,
      "bailoutfee": 0.1,
      "initialshareissue": 10,
      "sharespurchased": 0,
      "initialshareprice": 100.0,
      "currentshareprice": 100.0,
      "intialpricepershare": D('100.00'),
      "currency": "AUD",
      "openingbank": D('1000.00'),
      "currentbalance": D('1000.00'),
      "liveroi": 0.0,
      "livesince": datetime.strpftime("20160401", "%Y%m%d"),
      },
    fund4 = {
    "pk": 4,
    "model": "fund",
    "fields": {
      "name": "XXXXXXXX GBP",
      "code": "EXXXX",
      "description": """
      lotusmsmsmsmsmsmsmsmmsmsmsmsmsmsmsmmsmsmsmsmsmsmsmsmsmsmsms
      """,
      "isActive": False,
      "managementfee":0.02,
      "performancefee": 0.02,
      "performancethreshold": 0.245,
      "bailoutfee": 0.1,
      "initialshareissue": 10,
      "sharespurchased": 0,
      "initialshareprice": 100.0,
      "currentshareprice": 100.0,
      "intialpricepershare": D('100.00'),
      "currency": "AUD",
      "openingbank": D('1000.00'),
      "currentbalance": D('1000.00'),
      "liveroi": 0.0,
      "livesince": datetime.strpftime("20160401", "%Y%m%d"),
      },

def buildrunners():
    pass
    #all columns but
    #1 csv file
