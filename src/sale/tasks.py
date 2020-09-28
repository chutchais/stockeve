import requests
from sale.models import SoInvHD

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
