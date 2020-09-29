import requests
from sale.models import SoInvHD,SoInvDT

def pull_sale_winspeed():
    import datetime, pytz
    tz = pytz.timezone('Asia/Bangkok')
    # Compute the local datetime: local_dt
    local_dt = datetime.datetime.now(tz=tz)
    # Print the local datetime
    report_str = local_dt.strftime('%Y-%m-%d')
    print(f'Report time : {report_str}')
    donload_sale(report_str)

def donload_sale(date='2020-09-21'):
    from datetime import datetime
    URL_SALE = f'http://180.183.250.150:8081/api/sale/date/{date}'
    URL_SALE = f'http://192.168.101.10:8081/api/sale/date/{date}'
    res = requests.get(URL_SALE)
    for item in res.json()['invoices']:
        # print(item)
        soinvid         = item['SOInvID']
        docuno          = item['DocuNo']
        totabaseamnt    = item['TotaBaseAmnt']
        vatamnt         = item['VATAmnt']
        netamnt         = item['NetAmnt']
        saledate        = date_dt3 = datetime.strptime(date, '%Y-%m-%d')
        obj, created = SoInvHD.objects.get_or_create(
            soinvid=int(soinvid),
            defaults={'docuno': docuno,
                    'totabaseamnt':float(totabaseamnt),
                    'vatamnt': float(vatamnt),
                    'netamnt': float(netamnt),
                    'saledate':saledate
                    },
        )
        # Added on Sep 28,2020 -- To Pull Order detail
        # http://180.183.250.150:8081/api/saleorder/99551
        # http://192.168.101.10:8081/api/saleorder/99551
        if created:
            donload_sale_items(obj)

def donload_sale_items(soinv_obj):
    from datetime import datetime
    URL_SALE_ITEM = f'http://180.183.250.150:8081/api/saleorder/{soinv_obj.soinvid}'
    URL_SALE_ITEM = f'http://192.168.101.10:8081/api/saleorder/{soinv_obj.soinvid}'
    print (URL_SALE_ITEM)
    # URL_SALE_ITEM = f'http://192.168.101.10:8081/api/saleorder/{soinv}'
    # URL_SALE = f'http://192.168.101.10:8081/api/sale/date/{date}'
    res = requests.get(URL_SALE_ITEM)
    for item in res.json()['items']:
        # soinvid             = item['SOInvID']
        listno              = item['ListNo']
        goodid              = item['GoodID']
        goodcode            = item['GoodCode']
        goodname            = item['GoodName']
        goodqty             = item['GoodQty2']
        goodamnt            = item['GoodAmnt']
        inveid              = item['InveID']
        invecode            = item['InveCode']
        invename            = item['InveName']

        # saledate        = date_dt3 = datetime.strptime(date, '%Y-%m-%d')
        obj, created = SoInvDT.objects.get_or_create(
            soinvid=soinv_obj,listno=int(listno),
            defaults={'goodid': goodid,
                    'goodcode' : goodcode,
                    'goodname' : goodname,
                    'goodqty' : float(goodqty),
                    'goodamnt':float(goodamnt),
                    'inveid' : int(inveid),
                    'invecode':invecode,
                    'invename' : invename
                    },
        )
        print(f'Create order detail {goodcode}')
        # Added on Sep 28,2020 -- To Pull Order detail
        # http://180.183.250.150:8081/api/saleorder/99551
        # http://192.168.101.10:8081/api/saleorder/99551
        if created:
            pass