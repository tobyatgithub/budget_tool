from django.test import TestCase, Client
from budget_tool.factories import (
    BudgetFactory, 
    TransactionFactory, 
    UserFactory,
    Budget,
    Transaction)


class TestBudgetViews(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.set_password('secret')
        self.user.save()
        self.c = Client()

    def test_denied_if_no_login(self):
        res = self.c.get('/budget', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'class="login-form container"', res.content)
        
    def test_denied_if_wrong_pw(self):
        self.c.login(
            username=self.user.username,
            password='imadeitup',
        )        
        res = self.c.get('/budget')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(b'', res.content)

    def test_logged_in_views(self):
        self.c.login(
            username=self.user.username,
            password='secret',
        )

        budget = BudgetFactory(user=self.user)
        res = self.c.get('/budget', follow=True)
        
        # import pdb; pdb.set_trace()

        outprint = '<h3>Welcome to the site, {}</h3>\n'.format(self.user.username)
        self.assertIn(outprint.encode(), res.content)
        self.assertIn(budget.name.encode(), res.content)

    def test_logged_in_trans(self):
        self.c.login(
            username=self.user.username,
            password='secret',
        )

        budget = BudgetFactory(user=self.user)
        trans = TransactionFactory(budget=budget)
        res = self.c.get('/budgets', follow=True)

        self.assertEqual(trans.budget.name, budget.name)
        self.assertIn(trans.description.encode(), res.content)


class TestBudgetCreateViews(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.set_password('secret')
        self.user.save()
        self.c = Client()

    def test_create_budget(self):
        self.c.login(
            username=self.user.username,
            password='secret',
        )

        form_data = {
            'name': 'healthy fried chicken',
            'total_budget': '12.0',
            'remaining_budget': '12.0',
        }

        res = self.c.post('/budget/add', form_data, follow=True)

        self.assertIn(b'healthy fried chicken', res.content)


class TestTransCreateViews(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.set_password('secret')
        self.user.save()

        self.budget = BudgetFactory(user=self.user)

        self.c = Client()

    def test_create_transaction(self):
        self.c.login(
            username=self.user.username,
            password='secret',
        )

        form_data = {
            'assigned_to': self.user.id,
            'budget': self.budget.id,
            # 'trans_type': 'W',
            'amount': '200.0',
        }
        # import pdb; pdb.set_trace()
        res = self.c.post('/transaction/add', form_data, follow=True)

        self.assertIn(b'200.0', res.content)