import factory
from django.contrib.auth.models import User
from budgets.models import Budget, Transaction


class UserFactory(factory.django.DjangoModelFactory):
    """Create a user for tests."""

    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class BudgetFactory(factory.django.DjangoModelFactory):
    """Create a budget for tests."""

    class Meta:
        model = Budget

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    total_budget = '200.0'


class TransactionFactory(factory.django.DjangoModelFactory):
    """Create a transaction for tests."""
    
    class Meta:
        model = Transaction

    assigned_to = factory.SubFactory(UserFactory)
    budget = factory.SubFactory(BudgetFactory)
    amount = '10.'