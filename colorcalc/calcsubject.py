from django.db import models


class CalcSubject(models.Model):
    
    MONTHS = [
        ('Jan', 'January'),
        ('Feb', 'February'),
        ('Mar', 'March'),
        ('Apr', 'April'),
        ('May', 'May'),
        ('Jun', 'June'),
        ('Jul', 'July'),
        ('Aug', 'August'),
        ('Sep', 'September'),
        ('Oct', 'October'),
        ('Nov', 'November'),
        ('Dec', 'December'),

    ]

    name = models.CharField(max_length=50)    
    birthMonth = models.CharField(max_length=3, choices=MONTHS)
    birthNum = models.IntegerField()


            
    def __str__(self):
        return  "".join( [self.name, "_", self.birthMonth, str(self.birthNum)] )
