from django.urls import path
from .views import BudgetDetailView, BudgetListView, TransactionView

urlpatterns = [
    path('budget', BudgetListView.as_view(), name='budget_list_view'),
    path('budgets', BudgetDetailView.as_view(), name='budget_detail_view'),
    path('transaction/<int:id>', TransactionView.as_view(), name='transaction_detail'),
    # path('card/<int:id>', CardView.as_view(), name='card_detail'),
]
