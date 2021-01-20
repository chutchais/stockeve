import requests
from transfer.models import ICStockHD,ICStockDetail
from product.models import Product,ProductStock
from store.models import Store

def pull_transfer_winspeed():
    import datetime, pytz
    tz = pytz.timezone('Asia/Bangkok')
    # Compute the local datetime: local_dt
    local_dt = datetime.datetime.now(tz=tz)
    # Print the local datetime
    # Added on Jan 8,2021 -- To increase 1 day for get sale data.
    local_dt = local_dt + datetime.timedelta(days=1)
    # ----------------------------------------------------------
    report_str = local_dt.strftime('%Y-%m-%d')
    print(f'Report time : {report_str}')
    download_transfer(report_str)

def download_transfer(date='2020-09-21'):
    from datetime import datetime
    URL_TRANSFER = f'http://180.183.250.150:8081/api/transfer/date/{date}'
    URL_TRANSFER = f'http://192.168.101.10:8081/api/transfer/date/{date}'
    res = requests.get(URL_TRANSFER)
    for item in res.json()['pos']:
        # print(item)
        docuid          = item['DocuID']
        docuno          = item['DocuNo']
        remark1         = item['Remark1']
        # docdate         = item['DocDate']
        # docdate         = datetime.strptime(date, '%Y-%m-%d')
        docudate        = datetime.strptime(date, '%Y-%m-%d')
        obj, created = ICStockHD.objects.get_or_create(
            docuid=int(docuid),
            defaults={'docuno': docuno,
                        'remark1' : remark1,
                        'docudate' : docudate
                    },
        )
        # Added on Sep 28,2020 -- To Pull Order detail
        # http://180.183.250.150:8081/api/saleorder/99551
        # http://192.168.101.10:8081/api/saleorder/99551
        if created:
            download_transfer_items(obj,docudate)

def download_transfer_items(trans_obj,transferdate):
    from datetime import datetime
    URL_TRANSFER_ITEM = f'http://180.183.250.150:8081/api/tranferdetail/{trans_obj.docuid}'
    URL_TRANSFER_ITEM = f'http://192.168.101.10:8081/api/tranferdetail/{trans_obj.docuid}'
    print (URL_TRANSFER_ITEM)
    res = requests.get(URL_TRANSFER_ITEM)
    for item in res.json()['items']:
        # soinvid             = item['SOInvID']
        listno              = item['ListNo']
        goodid              = item['GoodID']
        goodcode            = item['GoodCode']
        goodname            = item['GoodName']
        goodqty             = item['RemaQty']
        inveid              = item['InveID']
        invecode            = item['InveCode']
        invename            = item['InveName']

        # saledate        = date_dt3 = datetime.strptime(date, '%Y-%m-%d')
        obj, created = ICStockDetail.objects.get_or_create(
            icstockhd=trans_obj,listno=int(listno),
            defaults={'goodid': goodid,
                    'goodcode' : goodcode,
                    'goodname' : goodname,
                    'goodqty' : float(goodqty),
                    'inveid' : int(inveid),
                    'invecode':invecode,
                    'invename' : invename,
                    'created':transferdate
                    },
        )
        # print(f'Order ddate {transferdate}')
        # print(f'Create order detail {transferdate}')
        # Added on Sep 28,2020 -- To Pull Order detail
        # http://180.183.250.150:8081/api/saleorder/99551
        # http://192.168.101.10:8081/api/saleorder/99551
        if created:
            # pass
            # Start to adjust balance in Stock
            # 1)Get or Create Store object
            store,created = Store.objects.get_or_create(
                        name = invecode,
                        defaults ={
                            'title':invename,
                            'sale_able':True}
                        )
            # 2) Get or Create Product
            product,created = Product.objects.get_or_create(
                        number=goodcode,
                        defaults={
                            'finished_goods': True,
                            'title':goodname,
                            'description':goodname}
                        )
            # 3) Adjust Number in Store
            productstock,created = ProductStock.objects.get_or_create(
                        store = store,product=product,
                        defaults={
                            'qty' : float(goodqty)
                        }
                        )
            
            if not created:
                # Stock is exist -- need to adjust number
                print(f'Adjust stock of {productstock} by {float(goodqty)}')
                productstock.qty = productstock.qty + float(goodqty)
                productstock.save()
            else :
                print(f'Creagte stock of {productstock} by {float(goodqty)}')


# from product.models import Product
# from store.models import Store

# def add_to_sale(product_code,store_code,saledate,qty=0,price=0,description=''):
#     print(f'Add Sale : {product_code} ,{store_code} ,{qty} ,{price} ,{description}')
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
    
#     sale = Sale.objects.create(product=product,
#                     store=store,qty=qty,
#                     price=price,description=description,created=saledate,saledate=saledate)
#     print('Save Sale successful..')
