from djongo import models  # databases!
from django.contrib.auth.models import User
from django.urls import reverse
import jsonfield


class Categories(models.Model):
    category = jsonfield.JSONField({"Entertainment":0})
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # current_monthly_spent = models.CharField(max_length=100, default="0")
    # current_monthly_income = models.CharField(max_length=100, default="0")
    # # for form
    # monthly_goal = models.CharField(max_length=100, default="0", blank=True)
    # # current spent/income for view REPRESENTATION OF CURRENT_MONTHLY_SPENT/INCOME
    # monthly_amount = models.CharField(max_length=100, default="0")
    # is_expense = models.BooleanField(default=True)

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        super(Categories, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # reverse will return the full path as a string so we can redirect to our budgeting-home template page
        return reverse('budgeting-home')


class Transaction(models.Model):
    t_type = models.CharField("Income/Expense", max_length=15, null=True)
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, null=True)
    source = models.CharField("Title", max_length=30)
    amount = models.CharField(max_length=100, default="0")
    notes = models.TextField("Additional Information", blank=True, null=True)
    date_posted = models.DateField("Transaction Date (mm/dd/yyyy)",
                                   auto_now_add=False, auto_now=False, blank=False, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.source

    def get_absolute_url(self):
        # reverse will return the full path as a string so we can redirect to our transaction-detail template page for our newly created transaction
        return reverse('budgeting-home')

    def add_type(self, typeName):
        self.t_type = typeName
