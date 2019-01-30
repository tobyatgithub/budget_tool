from django.test import TestCase
from budget_tool.factories import UserFactory, BudgetFactory, TransactionFactory


class TestBudgetModels(TestCase):
    def setUp(self):
        self.budget = BudgetFactory(name='test name')

    def test_default_budget_attrs(self):
        self.assertEqual(self.budget.name, 'test name')
        self.assertEqual(self.budget.total_budget, '200.0')


class TestTransModels(TestCase):
    def setUp(self):
        self.transaction = TransactionFactory(
            assigned_to=UserFactory(),
            budget=BudgetFactory(name='test name')
        )
    
    def test_default_trans_attrs(self):
        self.assertEqual(self.transaction.trans_type, 'Withdrawal')