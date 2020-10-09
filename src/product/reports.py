from django.core.mail import send_mail
from django_q.tasks import async_task

from product.models import Product

def lower_stock_report():
    import datetime, pytz
    tz = pytz.timezone('Asia/Bangkok')
    local_dt = datetime.datetime.now(tz=tz)
    report_str = local_dt.strftime('%Y-%m-%d %H:%M:%S')
    print(f'Generate Stock status report on {report_str}')
    objects = Product.objects.filter(lower_stock=True,min_stock__gt = 0).order_by('number')
    async_task('product.reports.send_email_report',
                objects,
                f'Daily Lacking Stock Report on {report_str}',
                'product/stock_report.html')

def higher_stock_report():
    import datetime, pytz
    tz = pytz.timezone('Asia/Bangkok')
    local_dt = datetime.datetime.now(tz=tz)
    report_str = local_dt.strftime('%Y-%m-%d %H:%M:%S')
    print(f'Generate Stock status report on {report_str}')
    objects = Product.objects.filter(higher_stock=True,max_stock__gt = 0).order_by('number')
    async_task('product.reports.send_email_report',
                objects,
                f'Daily Over Stock Report on {report_str}',
                'product/stock_report.html')


# Common Email function
def send_email_report(object_list,title ,template_file):
    print (f'{title} -- Send mail')
    from django.template.loader import render_to_string
    html_message  = render_to_string(template_file, 
            {
                'object_list': object_list,
                'title' : title 
            }
        )

    from django.conf import settings as conf_settings
    recipient_list 	= conf_settings.EMAIL_RECIPIENT_LACKING_LIST
    from_email 		= conf_settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject= f'{title}',
        message = None,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
        auth_user=None,auth_password=None,connection=None,
        html_message=html_message
    )