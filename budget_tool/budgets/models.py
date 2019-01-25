from django.db import models
# from django.utils import timezone
# from django.dispatch import receiver
from django.contrib.auth.models import User


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=128, default='noname')
    total_budget = models.FloatField(max_length=80, default='0.0')
    remaining_budget = models.FloatField(max_length=80, default='0.0')

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)    
    # test = models.CharField(max_length=80, default='humm')

    def __repr__(self):
        return "%s %s %s" % (self.name, self.total_budget, self.remaining_budget)

    def __str__(self):
        return "%s %s %s" % (self.name, self.total_budget, self.remaining_budget)


class Transaction(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='transactions')

    TYPES = [
        ("Withdrawal", "W"),
        ("Depositi", "D"),
    ]
    trans_type = models.CharField(max_length=50, default='Withdrawal', choices=TYPES)
    amount = models.FloatField(max_length=80, default='0.0')
    description = models.CharField(max_length=1280, default='No Description')
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)  
    
    def __repr__(self):
        return self.description
        
    def __str__(self):
        return self.description

    class Meta:
        ordering = ('trans_type',)


