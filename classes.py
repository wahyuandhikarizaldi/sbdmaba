from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

# class CreateTask(FlaskForm):
#     title = StringField('Task Title')
#     shortdesc = StringField('Short Description')
#     priority = IntegerField('Priority')
#     create = SubmitField('Create')

# class DeleteTask(FlaskForm):
#     key = StringField('Task ID')
#     title = StringField('Task Title')
#     delete = SubmitField('Delete')

# class UpdateTask(FlaskForm):
#     key = StringField('Task Key')
#     shortdesc = StringField('Short Description')
#     update = SubmitField('Update')

  
## DOKTER
      
class DokterForm(FlaskForm):
    nama = StringField('Nama Dokter')
    spesialis = StringField('Spesialis')
    no_telepon = StringField('No Telepon')
    simpan = SubmitField('Simpan')

class DeleteDokterForm(FlaskForm):
    id_dokter = StringField('ID Dokter (MongoDB)')
    hapus = SubmitField('Hapus')

class UpdateDokterForm(FlaskForm):
    id_dokter = StringField('ID Dokter (MongoDB)')
    nama = StringField('Nama Dokter Baru')
    spesialis = StringField('Spesialis Baru')
    no_telepon = StringField('No Telepon Baru')
    update = SubmitField('Update')
    
    
### Pasien
class PasienForm(FlaskForm):
    nama = StringField('Nama Pasien')
    no_telepon = StringField('No Telepon')
    simpan = SubmitField('Simpan')

class DeletePasienForm(FlaskForm):
    id_pasien = StringField('ID Pasien (MongoDB)')
    hapus = SubmitField('Hapus')

class UpdatePasienForm(FlaskForm):
    id_pasien = StringField('ID Pasien (MongoDB)')
    nama = StringField('Nama Pasien Baru')
    no_telepon = StringField('No Telepon Baru')
    update = SubmitField('Update')
    
    
