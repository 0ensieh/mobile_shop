# Generated by Django 4.1.5 on 2023-02-12 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='آدرس دقیق')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر منتسب به آدرس')),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس ها',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('paid_time', models.DateTimeField(blank=True, null=True, verbose_name='زمان پرداخت')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت شده؟')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='کد')),
                ('shipping_status', models.CharField(choices=[('Waiting Payment', 'در انتظار پرداخت'), ('Paid', 'پرداخت شده'), ('Posted', 'ارسال شده'), ('Delivered', 'تحویل داده شده'), ('Returned', 'مرجوعی'), ('Canceled', 'لغو شده'), ('Waiting For Checking', 'منتظر تایید شدن چک')], default='Waiting Payment', max_length=20, verbose_name='وضعیت سفارش')),
                ('payment_type', models.CharField(choices=[('Internet', 'پرداخت اینترنتی'), ('Home', 'پرداخت در محل'), ('Check', 'خرید چکی')], default='Internet', max_length=100, verbose_name='نوع پرداخت')),
                ('ref_id', models.IntegerField(blank=True, null=True, verbose_name='کد رهگیری پرداخت اینترنتی')),
                ('description', models.TextField(verbose_name='توضیحات مربوط به سفارش(رنگ کالا)')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='order.address', verbose_name='آدرس')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر سفارش دهنده')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش ها',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('price_after_discount', models.PositiveIntegerField(verbose_name='قیمت بعد از تخفیف')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='تعداد')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='سفارش مربوطه')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_items', to='shop.product', verbose_name='محصول مربوطه')),
            ],
            options={
                'verbose_name': 'آیتم',
                'verbose_name_plural': 'آیتم ها',
            },
        ),
        migrations.CreateModel(
            name='CheckImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_image', models.ImageField(upload_to='check/check_image/', verbose_name='عکس چک')),
                ('national_cart', models.ImageField(upload_to='check/national_cart/', verbose_name='عکس کارت ملی')),
                ('others', models.ImageField(blank=True, null=True, upload_to='check/others', verbose_name='سایر مدارک')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='سفارش مربوطه')),
            ],
            options={
                'verbose_name': 'چک  ',
                'verbose_name_plural': 'چک ها',
            },
        ),
    ]