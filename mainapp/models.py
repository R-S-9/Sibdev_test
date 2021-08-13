from django.db import models


class CustomerLog(models.Model):
    """Модель клиента"""

    customer = models.CharField(
        max_length=20,
        verbose_name="Клиент",
        blank=False
    )

    date = models.DateTimeField(verbose_name='Дата')

    def __str__(self):
        return f'{self.id}-{self.customer}, дата: {self.date}'

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

    total = models.DecimalField(max_digits=14, decimal_places=2)

    quantity = models.IntegerField(default=0)

    customer_item = models.ForeignKey(
        CustomerLog,
        verbose_name='Клиент',
        related_name='pur_item',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.customer_item.customer} - {self.item}, ' \
               f'кол-во: {self.quantity}, чек: {self.total}'

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
