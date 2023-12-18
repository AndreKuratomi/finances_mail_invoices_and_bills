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
    cliente = models.TextField(db_column='CLIENTE', blank=True, null=True)  # Field name made lowercase.
    planta = models.TextField(db_column='PLANTA', blank=True, null=True)  # Field name made lowercase.
    origem = models.TextField(db_column='ORIGEM', blank=True, null=True)  # Field name made lowercase.
    percurso = models.IntegerField(db_column='PERCURSO', blank=True, null=True)  # Field name made lowercase.
    nota = models.IntegerField(db_column='NOTA', blank=True, null=True)  # Field name made lowercase.
    item = models.IntegerField(db_column='ITEM', blank=True, null=True)  # Field name made lowercase.
    metal = models.TextField(db_column='METAL', blank=True, null=True)  # Field name made lowercase.
    peso = models.IntegerField(db_column='PESO', blank=True, null=True)  # Field name made lowercase.
    emissao_da_nf = models.TextField(db_column='EMISSAO DA NF', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    previsao_de_chegada = models.TextField(db_column='PREVISAO DE CHEGADA', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    status = models.TextField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
    placa = models.TextField(db_column='PLACA', blank=True, null=True)  # Field name made lowercase.
    transportadora = models.TextField(db_column='TRANSPORTADORA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'table_name'
