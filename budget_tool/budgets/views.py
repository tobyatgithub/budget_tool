from django.urls import reverse_lazy
from .models import Budget, Transaction
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BudgetForm, TransactionForm


class BudgetListView(LoginRequiredMixin, ListView):
    """
    List all available budgets owned by current user.
    """
    template_name = '/src/budgets/templates/budget_list.html'
    # this will be the reference for the get_queryset() result
    context_object_name = 'budgets'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        # this line will be translated to SQL when called and filter is completed at database level.
        # this is way more efficient compared to query everything in sql, get to python and process
        # at python level.
        return Budget.objects.filter(user__username=self.request.user.username)


class BudgetDetailView(LoginRequiredMixin, ListView):
    """
    List all available budgets owned by current user.
    """
    template_name = '/src/budgets/templates/budget_detail.html'
    context_object_name = 'budgets'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        # pass
        return Budget.objects.filter(user__username=self.request.user.username)
        # return Budget.objects.all()

    def get_context_data(self, **kwargs):
        # 1. inherite information from super class (e.g. token, context object name, etc.)
        context = super().get_context_data(**kwargs)  
        # 2. we add one more info onto our context
        # budget__user__username -> in database, budget has an attr called user with an attr called username
        context['transactions'] = Transaction.objects.filter(budget__user__username=self.request.user.username)
        return context
        # return Budget.objects.all()


class TransactionView(LoginRequiredMixin, DetailView):
    """
    List all available transactions within the selected budget.
    """
    template_name = '/src/budgets/templates/transaction_detail.html'
    model = Transaction  # == to assign value to self.model
    context_object_name = 'transaction'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Budget.objects.filter(budget__user__username=self.request.user.username)
    

class BudgetCreateView(LoginRequiredMixin, CreateView):
    template_name = '/src/budgets/templates/budget_create.html'
    model = Budget
    form_class = BudgetForm
    success_url = reverse_lazy('budget_list_view')
    login_url = reverse_lazy('auth_login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = '/src/budgets/templates/transaction_create.html'
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('budget_detail_view')
    login_url = reverse_lazy('auth_login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)