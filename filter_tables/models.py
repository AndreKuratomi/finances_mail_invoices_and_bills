# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TableName(models.Model):
    index = models.IntegerField(blank=True, null=True)
    id = models.AutoField(primary_key=True)
    nome_do_cliente = models.TextField(db_column='Nome do Cliente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cnpj = models.TextField(db_column='CNPJ', blank=True, null=True)  # Field name made lowercase.
    numero = models.TextField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    valor_liquido = models.TextField(db_column='Valor Liquido', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'table_name'
