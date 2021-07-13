from django.db import models
from django.utils import timezone


class CustomerLog(models.Model):
    """Модель клиента"""

    customer = models.CharField(
        max_length=20,
        verbose_name="Клиент",
        blank=False
    )

    date = models.DateTimeField(verbose_name='Дата', default=timezone.now)

    def __str__(self):
        return self.customer

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('date',)


class PurchasedItems(models.Model):
    """Модель купленого предмета"""

    item = models.CharField(
        max_length=30,
        verbose_name='Предмет',
        blank=False
    )

    total = models.DecimalField(max_digits=8)

    quantity = models.IntegerField(default=0)

    customer_item = models.ForeignKey(
        CustomerLog,
        verbose_name='Клиент',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.item}, кол-во: {self.quantity}, чек:{self.total}'

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
