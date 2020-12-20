import requests
from receiving.models import Receiving,PoInvHD,PoInvDT


def pull_receive_winspeed():
    import datetime, pytz
    tz = pytz.timezone('Asia/Bangkok')
    # Compute the local datetime: local_dt
    local_dt = datetime.datetime.now(tz=tz)
    # Print the local datetime
    report_str = local_dt.strftime('%Y-%m-%d')
    download_receive(report_str)

def download_receive(date='2020-12-14'):
    from datetime import datetime
    URL_SALE = f'http://180.183.250.150:8081/api/receive/date/{date}'
    URL_SALE = f'http://192.168.101.10:8081/api/receive/date/{date}'
    res = requests.get(URL_SALE)
    for item in res.json()['pos']:
        # print(item)
        poinvid         = item['POInvID']
        docuno          = item['DocuNo']
        totabaseamnt    = item['TotaBaseAmnt']
        vatamnt         = item['VATAmnt']
        netamnt         = item['NetAmnt']
        vendor          = item['VendorName']
        # saledate        = date_dt3 = datetime.strptime(date, '%Y-%m-%d')
        receivedate      = datetime.strptime(date, '%Y-%m-%d')
        obj, created = PoInvHD.objects.get_or_create(
            poinvid=int(poinvid),
            defaults={'docuno': docuno,
                    'totabaseamnt':float(totabaseamnt),
                    'vatamnt': float(vatamnt),
                    'netamnt': float(netamnt),
                    'receivedate':receivedate,
                    'vendorname':vendor
                    },
        )
        # Added on Sep 28,2020 -- To Pull Order detail
        # http://180.183.250.150:8081/api/saleorder/99551
        # http://192.168.101.10:8081/api/saleorder/99551
        if created:
            download_receive_items(obj,receivedate)

def download_receive_items(poinv_obj,receivedate):
    from datetime import datetime
    URL_SALE_ITEM = f'http://180.183.250.150:8081/api/receiveorder/{poinv_obj.poinvid}'
    URL_SALE_ITEM = f'http://192.168.101.10:8081/api/receiveorder/{poinv_obj.poinvid}'
    print (URL_SALE_ITEM)
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
        obj, created = PoInvDT.objects.get_or_create(
            poinvid=poinv_obj,listno=int(listno),
            defaults={'goodid': goodid,
                    'goodcode' : goodcode,
                    'goodname' : goodname,
                    'goodqty' : float(goodqty),
                    'goodamnt':float(goodamnt),
                    'inveid' : int(inveid),
                    'invecode':invecode,
                    'invename' : invename,
                    'created':receivedate
                    },
        )
        print(f'Order date {receivedate}')
        print(f'Create order detail {goodcode}')
        # Added on Sep 28,2020 -- To Pull Order detail
        # http://180.183.250.150:8081/api/saleorder/99551
        # http://192.168.101.10:8081/api/saleorder/99551
        if created:
            pass


# from product.models import Product,ProductStock
# from store.models import Store

# def add_to_receive(product_code,store_code,saledate,qty=0,price=0,description=''):
#     print(f'Add Receive : {product_code} ,{store_code} ,{qty} ,{price} ,{description}')
#     # Verify Product
#     product,created = Product.objects.get_or_create(
#                             number=product_code,
#                             defaults={
#                                 'finished_goods': True,
#                                 'title':description,
#                                 'description':description}
#                             )
#     # Verify Store
#     store,created = Store.objects.get_or_create(
#                             name = store_code,
#                             defaults ={
#                                 'title':store_code,
#                                 'sale_able':True}
#                             )
    
#     # sale = Sale.objects.create(product=product,
#     #                 store=store,qty=qty,
#     #                 price=price,description=description,created=saledate,saledate=saledate)

#     # Get or Create ProductStock
#     productstock,created = ProductStock.objects.get_or_create(
#                             product = product,
#                             store = store
#                             )

#     receive = Receiving.objects.create(product=product,
#                     productstock = productstock,
#                     store=store,qty=qty,
#                     receivedate=saledate)
#     print('Save Receive successful')