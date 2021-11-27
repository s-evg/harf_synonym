from django.db import models


POS = [
    ['noun', 'существительное'],
    ['verb', 'глагол'],
    ['adjective', 'прилагательное'],
    ['participle', 'причастие']
]


class Word(models.Model):
    """Слово"""

    text = models.CharField(max_length=100, verbose_name='слово или фраза', primary_key=True)
    pos = models.CharField(max_length=20, verbose_name='часть речи', choices=POS, null=True, blank=True)
    tr = models.ManyToManyField('self', max_length=100, verbose_name='перевод / значение', null=True, blank=True)
    syn = models.ManyToManyField('self', max_length=100, verbose_name='синоним', null=True, blank=True)
    fr = models.PositiveIntegerField(max_length=1, verbose_name='из яндекса не понятно что это', null=True, blank=True)

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'

    def __str__(self):
        return self.text
