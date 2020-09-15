from rest_framework import serializers
from budgeting.models import *
from datetime import datetime


class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("expense_categories", "expense_categories_budget",
                  "expense_categories_monthly", "income_categories", "income_categories_budget", "income_categories_monthly")

    def create(self, validated_data):
        categories = Categories.objects.create(
            author=self.context["request"].user,
            expense_categories={
                "Entertainment": 0.0,
                "Utilities": 0.0,
                "Food": 0.0,
            },
            expense_categories_budget={
                "Entertainment": 0.0,
                "Utilities": 0.0,
                "Food": 0.0,
            },

            expense_categories_monthly={
                "Entertainment": {},
                "Utilities": {},
                "Food": {},
            },

            income_categories={
                "Work": 0.0,
                "Stocks": 0.0,
            },
            income_categories_budget={
                "Work": 0.0,
                "Stocks": 0.0,
            },

            income_categories_monthly={
                "Work": {},
                "Stocks": {},
            },



        )

        categories.save()
        return categories

    def update(self, instance, validated_data):
        instance.expense_categories = validated_data.get("expense_categories")
        instance.expense_categories_budget = validated_data.get(
            "expense_categories_budget")
        instance.expense_categories_monthly = validated_data.get(
            "expense_categories_monthly")

        instance.income_categories = validated_data.get("income_categories")
        instance.income_categories_budget = validated_data.get(
            "income_categories_budget")
        instance.income_categories_monthly = validated_data.get(
            "income_categories_monthly")

        instance.save()
        return instance


class AllTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('t_type', 'category', 'source',
                  'amount', 'notes', 'date_posted')

    # might need to change create and update func, and create a delete func

    # create to be explicit
    def create(self, validated_data):
        transaction = Transaction.objects.create(
            t_type=validated_data['t_type'],
            category=validated_data["category"],
            source=validated_data['source'],
            amount=validated_data['amount'],
            notes=validated_data['notes'],
            date_posted=validated_data['date_posted'],
            author=self.context['request'].user,
            year=validated_data['date_posted'].year,
            month=validated_data['date_posted'].month,
        )
        transaction.save()
        return transaction

    def update(self, instance, validated_data):
        transactionDate = datetime.strptime(
            str(validated_data.get("date_posted")), '%Y-%m-%d')
        instance.category = validated_data.get("category")
        instance.source = validated_data.get("source")
        instance.amount = validated_data.get("amount")
        instance.date_posted = validated_data.get("date_posted")
        instance.notes = validated_data.get("notes")
        instance.year = transactionDate.year
        instance.month = transactionDate.month

        instance.save()
        return instance
