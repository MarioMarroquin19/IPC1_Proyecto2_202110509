from zoneinfo import available_timezones
from flask import Flask,jsonify,request
from datetime import datetime
from iteration_utilities import duplicates


app = Flask(__name__)

numero =1
libros = []
usuarios = []
prestamos = []
data_id=[]
repetidos=[]
data_id_user = []


#COMPROBAR ESTADO DEL SERVIDOR--------------------------------------------------------------------
@app.route('/')
def home():
    diccionario_envio ={
        "msg": 'servidor funcionando correctamente',
        "status": 200

    }
    return jsonify(diccionario_envio)
#--------------------------------------------------------------------------------------------------


#USUARIOS------------------------------------------------------------------------------------------
@app.route('/user',methods=['POST'])
def crear_usuario():
    data_usuarios = request.get_json()
    it_is=True
    for usuario in data_usuarios:
        ids=usuario.get('id_user')
        data_id_user.append(ids)

    duplicados = list(duplicates(data_id_user))
    if len(duplicados)>0:
        it_is = False
        data_id_user.clear()
        return jsonify({
        "msg":'ERROR:Usuarios con ID repetido',
        "status":405
    })
    
    if it_is == True:
        for usuario in data_usuarios:
            usuarios.append(usuario)
        return jsonify({
        "msg": 'Usuario creado con éxito',
        "status": 201

    })





@app.route('/user/:id',methods=['GET'])
def ver_usuario():
    usuarios_out=[]
    data = request.get_json()
    id_user = data.get('id_user')
    for usuario in usuarios:
       if usuario.get('id_user') == id_user:
            usuarios_out.append(usuario)
    if len(usuarios_out)>0:
            return jsonify(usuarios_out)
    return jsonify({
                    "msg": 'No hay coincidencias encontradas',
                    "status": 422
            })


@app.route('/user',methods=['PUT'])
def modificar_usuario():
    data = request.get_json()
    id_user = data.get('id_user')
    user_name = data.get('user_name')
    user_nickname = data.get('user_nickname')
    user_password =data.get('user_password')
    user_rol=data.get('user_rol')
    available=data.get('available')

    for i in range(len(usuarios)):
        if usuarios[i].get('id_user') == id_user:
            usuarios[i]['user_name'] = user_name
            usuarios[i]['user_nickname'] = user_nickname
            usuarios[i]['user_password'] = user_password
            usuarios[i]['user_rol'] = user_rol 
            usuarios[i]['available']=available        
            return jsonify({
                    "msg": 'Usuario actualizado',
                    "status": 201
            })

    return jsonify({
            "msg": 'Usuario no encontrado',
            "status": 404
    })

#-----------------------------------------------------------------------------





#LIBROS-----------------------------------------------------------------------
@app.route('/book',methods=['POST'])
def crear_libro():
    data_libros = request.get_json()
    data1_libros =request.get_json()
    #data_id.clear()
    for libro in data_libros:

        edicion = libro.get('book_edition')
        try:
            int(edicion)
            it_is = True
            if(int(edicion) < 0):
                it_is=False
                break
        except ValueError:
            it_is = False
            break

        anio = libro.get('book_year')
        try:
            int(anio)
            it_is = True
            if(int(anio) < 0):
                it_is=False
                break
        except ValueError:
            it_is = False
            break

        copias_disponibles = libro.get('book_available_copies')
        try:
            int(copias_disponibles)
            it_is = True
            if(int(copias_disponibles) < 0):
                it_is=False
                break
        except ValueError:
            it_is = False
            break

        no_copias = libro.get('book_unavailable_copies')
        try:
            int(no_copias)
            it_is = True
            if(int(no_copias) < 0):
                it_is=False
                break
        except ValueError:
            it_is = False
            break
        
        copias=libro.get('book_copies')
        try:
            int(copias)
            it_is = True
            if(int(copias) < 0):
                it_is=False
                break
        except ValueError:
            it_is = False
            break    

    if it_is == True:
        for libro in data_libros:
            ids= libro.get('id_book')
            data_id.append(ids)      

    duplicados = list(duplicates(data_id))
    if len(duplicados)>0:
        it_is = False
        data_id.clear()
        return jsonify({
        "msg":'ERROR:Libros con ID repetido',
        "status":405
    })

    if it_is == True:
        for libro1 in data1_libros:
            libros.append(libro1)
        return jsonify({
            "msg": 'Libros cargados',
            "status": 200
            })
    
    return jsonify({
        "msg":'Error en la sintaxis de los libros',
        "status":450
    })


@app.route('/book',methods=['PUT'])
def modificar_libro():
    data = request.get_json()
    id_book = data.get('id_book')
    book_author = data.get('book_author')
    book_title = data.get('book_title')
    book_edition= data.get('book_edition')
    book_editorial=data.get('book_editorial')
    book_year=data.get('book_year')
    book_description=data.get('book_description')
    book_available_copies=data.get('book_available_copies')
    book_unavailable_copies=data.get('book_unavailable_copies')
    book_copies= data.get('book_copies')

    for i in range(len(libros)):
        if libros[i].get('id_book') == id_book:
            libros[i]['book_author'] = book_author
            libros[i]['book_title'] = book_title
            libros[i]['book_edition'] = book_edition
            libros[i]['book_editorial'] = book_editorial
            libros[i]['book_year'] = book_year
            libros[i]['book_description'] = book_description
            libros[i]['book_available_copies'] = book_available_copies
            libros[i]['book_unavailable_copies'] = book_unavailable_copies
            libros[i]['book_copies'] = book_copies

            return jsonify({
                    "msg": 'Libro actualizado',
                    "status": 201
            })

    return jsonify({
                    "msg": 'Libro no encontrado',
                    "status": 404
            })


@app.route('/book/:id',methods=['DELETE'])
def eliminar_libro():

    data = request.get_json()

    id_book = data.get('id_book')
    

    for i in range(len(libros)):
        if libros[i].get('id_book') == id_book:
            libros.pop(i)
            return jsonify({
                    "msg": 'Libro eliminado',
                    "status": 200
            })

    return jsonify({
                    "msg": 'Libro no encontrado, NO ELIMINADO',
                    "status": 403
            })


@app.route('/book',methods=['GET'])
def buscar_libro():

    libros_out=[]

    data = request.get_json()

    book_author = data.get('book_author')
    book_title = data.get('book_title')

    for libro in libros:
        if libro.get('book_author') == book_author or libro.get('book_title') == book_title:
            libros_out.append(libro)

    if len(libros_out)>0:
         return jsonify(libros_out)


    return jsonify({
                    "msg": 'No hay coincidencias encontradas',
                    "status": 404
            })



@app.route('/book/list',methods=['GET'])
def obtener_libro():

    return jsonify(libros)
#----------------------------------------------------------------------------------



#PRESTAMOS-------------------------------------------------------------------------


@app.route('/borrow',methods=['POST'])
def crear_prestamo():
    global numero
    data = request.get_json()
    id_user = data.get('id_user')
    id_book = data.get('id_book')
    libros_out=[]

    for id in usuarios:
        if id.get('id_user')==id_user and id.get('available') != False:
            for libro in libros:
                if libro.get('id_book') == id_book and int(libro.get('book_copies')) > 0 and int(libro.get('book_available_copies')) >0:
                    libros_out.append(libro)
            if len(libros_out)>0:
                    prestamo = {
                                    "id_borrow":numero,
                                    "borrow_date":datetime.today().strftime('%d-%m-%Y'),
                                    "returned":False,
                                    "id_user":id_user,
                                    "borrow_book":tuple(libros_out)
                                }
                    prestamos.append(prestamo)
                    numero +=1
                    for libro in libros:
                        if libro.get('id_book') == id_book:
                            dispo = int(libro.get('book_available_copies'))
                            dispo1 =int(libro.get('book_unavailable_copies'))
                            dispo -=1  
                            dispo1 +=1
                    for i in range(len(libros)):
                        if libros[i].get('id_book') == id_book:
                            libros[i]['book_available_copies'] = dispo
                            libros[i]['book_unavailable_copies'] = dispo1


                    return jsonify({
                            "msg": 'Se ha aceptado el prestamo',
                            "status": 200
                        })
            return jsonify({
                            "msg": 'El libro no está disponible',
                            "status": 422
            })
    return jsonify({
                            "msg": 'Usuario NO autorizado para préstamos',
                            "status": 410
            })


@app.route('/borrow/:id',methods=['PUT'])
def devolver_prestamo():
    data = request.get_json()
    id_borrow = data.get('id_borrow')
    
    for prestamo in prestamos:
        if prestamo.get('id_borrow') == id_borrow:
            for j in range(len(prestamos)):
                if prestamos[j].get('id_borrow') == id_borrow and prestamos[j].get('returned') != True:
                    prestamos[j]['returned'] = True

                    for h in range(len(prestamos[j]['borrow_book'])):
                        id=(prestamos[j]['borrow_book'][h]).get('id_book')
                        for libro in libros:
                            if libro.get('id_book') == id:
                                dispo = int(libro.get('book_available_copies'))
                                dispo1 =int(libro.get('book_unavailable_copies'))
                                dispo +=1  
                                dispo1 -=1
                        for i in range(len(libros)):
                            if libros[i].get('id_book') == id:
                                libros[i]['book_available_copies'] = dispo
                                libros[i]['book_unavailable_copies'] = dispo1
                    return jsonify({
                    "msg": 'Se ha devuelto el libro',
                    "status": 202
                    }) 
           
    return jsonify({
                    "msg": 'No hay prestamos con ese id',
                    "status": 422
    })   




@app.route('/borrow/:id',methods=['GET'])
def ver_prestamo():
    prestamos_out=[]
    data = request.get_json()
    id_borrow = data.get('id_borrow')
    for prestamo in prestamos:
        if prestamo.get('id_borrow') == id_borrow:
            prestamos_out.append(prestamo)
    if len(prestamos_out)>0:
            return jsonify(prestamos_out) 
    return jsonify({
                    "msg": 'No hay prestamos con ese id',
                    "status": 422
    })



#REPORTE--------------------------------------------------------------------------

@app.route('/report',methods=['GET'])
def reporte():

   Reporte = ["USUARIOS REGISTRADOS:",usuarios, "LIBROS REGISTRADOS:",libros,"PRESTAMOS REALIZADOS:",prestamos]
   return jsonify(Reporte)






#----------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(port=3004,debug=True)

