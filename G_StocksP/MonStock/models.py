from django.db import models

"""
Install Jazzmin Admin UI
Create Purchase Model
Create Sales Model
Create Inventory Model

Chapitre 4: 
Total Amount Calculation when Purchase Product from Vendor
Save data in inventory model when Purchase
Show last balance Qty of Specific Product
Show Purchase data


"""


class Categorys(models.Model):
    title = models.CharField(max_length=100)
    short_name = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = '0. Categorys'


class Vendors(models.Model):
    full_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photo_vendor/', blank=True)
    adress = models.TextField(max_length=50)
    mobile = models.CharField(max_length=15)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '1. Vendors'

        def __str__(self):
            return self.full_name


class Units(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '2. Units'

        def __str__(self):
            return self.title


class Products(models.Model):
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=50)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE, null=True)
    unit = models.ForeignKey(Units, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="imgproduct/", blank=True)

    class Meta:
        verbose_name_plural = '3. Products'

        def __str__(self):
            return self.title


# Purchases Model
class Purchases(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)

    qty = models.FloatField(default=0)
    price = models.FloatField(default=0)
    total_amount = models.FloatField(editable=False, default=0)
    pur_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '4. Purchases'

    def save(self, *args, **kwargs):
        self.total_amount = self.qty * self.price
        super(Purchases, self).save(*args, **kwargs)
        # Inventory Effect
        inventory = Inventorys.objects.filter(product=self.product).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_bal_qty + self.qty
        else:
            totalBal = self.qty

        Inventorys.objects.create(
            product=self.product,
            purchase=self,
            sale=None,
            pur_qty=self.qty,
            sale_qty=None,
            total_bal_qty=totalBal
        )


# Sales Medels
class Sales(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    qty = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False)
    sale_date = models.DateTimeField(auto_now_add=True)

    customer_name = models.CharField(max_length=100, blank=True)
    customer_adresse = models.TextField(max_length=100, blank=True)
    customer_mobile = models.CharField(max_length=15, blank=True)
    customer_email = models.EmailField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = '5. Sales'


def save(self, *args, **kwargs):
    self.total_amount = self.qty * self.price
    super(Sales, self).save(*args, **kwargs)
    # Inventory Effect
    inventory = Inventorys.objects.filter(product=self.product).order_by('-id').first()
    if inventory:
        totalBal = inventory.total_bal_qty - self.qty

    Inventorys.objects.create(
        product=self.product,
        purchase=None,
        sale=self,
        pur_qty=None,
        sale_qty=self.qty,
        total_bal_qty=totalBal
    )


# Inventory Models
class Inventorys(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchases, on_delete=models.CASCADE, default=0, null=True)
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, default=0, null=True)
    pur_qty = models.FloatField(default=0, null=True)
    sale_qty = models.FloatField(default=0, null=True)
    total_bal_qty = models.FloatField()

    class Meta:
        verbose_name_plural = '6. Inventorys'

    def product_unit(self):
        return self.product.unit.title

    def pur_date(self):
        if self.purchase:
            return self.purchase.pur_date

    def sale_date(self):
        if self.sale:
            return self.sale.sale_date

