from django.db import models


class Answers(models.Model):
    user_name = models.CharField(max_length=30)
    ip_address = models.CharField(max_length=127)
    R_count = models.IntegerField(default=0)
    I_count = models.IntegerField(default=0)
    A_count = models.IntegerField(default=0)
    S_count = models.IntegerField(default=0)
    E_count = models.IntegerField(default=0)
    C_count = models.IntegerField(default=0)
