from flask import Flask, render_template, redirect
from pymongo import MongoClient
from classes import *
from bson.objectid import ObjectId


# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))
client = MongoClient('localhost:27017')
db = client.TaskManager

if db.settings.count_documents({'name': 'task_id'}) <= 0:
    print("task_id Not found, creating....")
    db.settings.insert_one({'name':'task_id', 'value':0})

def updateTaskID(value):
    task_id = db.settings.find_one()['value']
    task_id += value
    db.settings.update_one(
        {'name':'task_id'},
        {'$set':
            {'value':task_id}
        })

def createTask(form):
    title = form.title.data
    priority = form.priority.data
    shortdesc = form.shortdesc.data
    task_id = db.settings.find_one()['value']
    
    task = {'id':task_id, 'title':title, 'shortdesc':shortdesc, 'priority':priority}

    db.tasks.insert_one(task)
    updateTaskID(1)
    return redirect('/')

def deleteTask(form):
    key = form.key.data
    title = form.title.data

    if(key):
        print(key, type(key))
        db.tasks.delete_many({'id':int(key)})
    else:
        db.tasks.delete_many({'title':title})

    return redirect('/')

def updateTask(form):
    key = form.key.data
    shortdesc = form.shortdesc.data
    
    db.tasks.update_one(
        {"id": int(key)},
        {"$set":
            {"shortdesc": shortdesc}
        }
    )

    return redirect('/')

# def resetTask(form):
#     db.tasks.drop()
#     db.settings.drop()
#     db.settings.insert_one({'name':'task_id', 'value':0})
#     return redirect('/')

@app.route("/delete_dokter/<id>", methods=["POST"])
def delete_dokter(id):
    db.dokter.delete_one({"_id": ObjectId(id)})
    return redirect("/")

@app.route("/delete_pasien/<id>", methods=["POST"])
def delete_pasien(id):
    db.pasien.delete_one({"_id": ObjectId(id)})
    return redirect("/")


@app.route('/', methods=['GET','POST'])
def main():
    # create form
    # cform = CreateTask(prefix='cform')
    # dform = DeleteTask(prefix='dform')
    # uform = UpdateTask(prefix='uform')
    # reset = ResetTask(prefix='reset')
    
    f_create_dokter = DokterForm(prefix='create_dokter')
    f_delete_dokter = DeleteDokterForm(prefix='delete_dokter')
    f_update_dokter = UpdateDokterForm(prefix='update_dokter')
    
    
    f_create_pasien = PasienForm(prefix='create_pasien')
    f_delete_pasien = DeletePasienForm(prefix='delete_pasien')
    f_update_pasien = UpdatePasienForm(prefix='update_pasien')


    # response
    # if cform.validate_on_submit() and cform.create.data:
    #     return createTask(cform)
    # if dform.validate_on_submit() and dform.delete.data:
    #     return deleteTask(dform)
    # if uform.validate_on_submit() and uform.update.data:
    #     return updateTask(uform)
    # if reset.validate_on_submit() and reset.reset.data:
    #     return resetTask(reset)
    
    if f_create_dokter.validate_on_submit() and f_create_dokter.simpan.data:
        dokter = {
            "nama": f_create_dokter.nama.data,
            "spesialis": f_create_dokter.spesialis.data,
            "no_telepon": f_create_dokter.no_telepon.data
        }
        db.dokter.insert_one(dokter)
        return redirect('/')

    if f_delete_dokter.validate_on_submit() and f_delete_dokter.hapus.data:
        try:
            db.dokter.delete_one({"_id": ObjectId(f_delete_dokter.id_dokter.data)})
        except:
            pass
        return redirect('/')

    if f_update_dokter.validate_on_submit() and f_update_dokter.update.data:
        try:
            db.dokter.update_one(
                {"_id": ObjectId(f_update_dokter.id_dokter.data)},
                {"$set": {
                    "nama": f_update_dokter.nama.data,
                    "spesialis": f_update_dokter.spesialis.data,
                    "no_telepon": f_update_dokter.no_telepon.data
                }}
            )
        except:
            pass
        return redirect('/')
    
    
    
    
    
    
    if f_create_pasien.validate_on_submit() and f_create_pasien.simpan.data:
        pasien = {
            "nama": f_create_pasien.nama.data,
            "no_telepon": f_create_pasien.no_telepon.data
        }
        db.pasien.insert_one(pasien)
        return redirect('/')

    if f_delete_pasien.validate_on_submit() and f_delete_pasien.hapus.data:
        try:
            db.pasien.delete_one({"_id": ObjectId(f_delete_pasien.id_pasien.data)})
        except:
            pass
        return redirect('/')

    if f_update_pasien.validate_on_submit() and f_update_pasien.update.data:
        try:
            db.pasien.update_one(
                {"_id": ObjectId(f_update_pasien.id_pasien.data)},
                {"$set": {
                    "nama": f_update_pasien.nama.data,
                    "no_telepon": f_update_pasien.no_telepon.data
                }}
            )
        except:
            pass
        return redirect('/')


    # read all data
    docs = db.tasks.find()
    data = []
    for i in docs:
        data.append(i)
        
    dokter_list = list(db.dokter.find())
    pasien_list = list(db.pasien.find())
    return render_template('home.html',
                           f_create_dokter=f_create_dokter, f_create_pasien=f_create_pasien,
                           f_delete_dokter=f_delete_dokter, f_delete_pasien=f_delete_pasien,
                           f_update_dokter=f_update_dokter, f_update_pasien=f_update_pasien,
                           data=data, dokter_list=dokter_list, pasien_list=pasien_list)


    # return render_template('home.html', cform = cform, dform = dform, uform = uform, \
    #         data = data, reset = reset)

if __name__=='__main__':
    app.run(debug=True)