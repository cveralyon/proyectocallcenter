import psycopg2
from tabulate import tabulate
from string import ascii_letters
print ()
print ("-----------------------------Bienvenido al portal Crossnot-------------------------------")
print ()


def sql(accion,tabla,lista_columnas,lista_valores,condicion=0):
    columnavalores=""
    if accion.lower()=="update":
        for i in range(len(lista_columnas)):
            a=str(lista_columnas[i])+"="+str(lista_valores[i])+", "
            columnavalores=columnavalores+a
        if not condicion==0:
            sentencia= accion+" " +tabla+" "+"set "+columnavalores+" where "+condicion
            return sentencia
    if accion.lower()=="insert":
        for i in range(len(lista_columnas)):
            a=str(lista_columnas[i])
        if condicion==0:
            sentencia=accion+"into "+tabla+"("
    if accion.lower()=="delete":
        sentencia=accion+" from "+tabla+" where "+condicion
        return sentencia




def evaluarllamada(t):
    conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
    cur = conn.cursor()
    cur.execute("SELECT t.id, t.nombre FROM tennant t")
    content=cur.fetchall()    
    print ()   
    cur=conn.cursor()
    cur.execute("select t1.nombre_archivo, t1.aprobacion from (aprobacion a join supervisores s on a.id_supervisor=s.id) as t1 join tennant t on t1.id_tennant=t.id where t.id='"+str(t)+"' and t1.eliminar_ap=False;")
    aprov =cur.fetchall()
    print(tabulate(aprov,headers=["Nombre archivo", "Aprobada"]))
    print()
    print()
    print ("Lista de subopciones:")
    print ('i) Agregar calificacion')
    print ('iii) Eliminar calificacion')
    print ('ii) Editar calificacion')
    subopcion=pdenuev4(3)
    if subopcion==1:
        print ("ID's de supervisor:")
        cur=conn.cursor()
        cur.close()
        cur.execute("SELECT id from supervisores where id_tennant="+str(t))
        content=cur.fetchall()
        for i in content:
            print (i[0])

                    
        sup =input("Ingrese su ID de supervisor para poder continuar: ")
        cur.execute("SELECT EXISTS(select * from supervisores s join tennant t on t.id=s.id_tennant where s.id="+str(sup)+" and t.id='"+str(t)+"')")
        valid= cur.fetchone()
        if valid[0]==True:
            print("Tu identificacion fue validada con exito")
            cur.execute("select s.id, t.nombre, s.nombre, s.apellido from supervisores s join tennant t on t.id=s.id_tennant where s.id="+str(sup)+";" )
            superv=cur.fetchall()
            print(tabulate(superv,headers=["ID", "Tennant", "Nombre", "Apellido"]))
            
            cur.execute("select l.nombre_archivos from llamadas l, tennant t, agente a where t.id=a.id_tennant and a.id=l.id_agente and t.id=1 and not exists (select nombre_archivo from aprobacion ap where ap.nombre_archivo=l.nombre_archivos)")
            llamadassinaprovar=cur.fetchall()
            for i in llamadassinaprovar:
                print (i[0])
            revision=0
            select= input("Ingrese y seleccione de la lista de arriba, el nombre de archivo de la llamada que desea calificar:" )
            for i in llamadassinaprovar[0]:
                if select in i[0]:
                    revision=1
            if revision==0:
                print ("llamada no puede ser calificada, porque no se encuentra en la lista de llamadas sin calificar")
                return None
            #revisar si la llamada ingresada esta en la lista de no calificadas, si existe y si corresponde al tennant.
            cur.execute("select * from llamadas where nombre_archivos='"+select+"';")
            #cur.execute("select t2.nombre_archivos, t2.id_agente, t2.id_tel_cliente, t2.fecha_hora, t2.duracion_seg, t2.transcripcion, t2.motivo_llamada, t2.saliente from (((llamadas l eliminar as eliminado join telefono_cliente tc on l.id_tel_cliente= tc.id ) as t0 join agente a on t0.id_agente=a.id)as t1 join clientes c on c.id= t1.id_cliente) as t2 join tennant t on t2.id_tennant=t.id where t.id ='"+str(t)+"' and t2.nombre_archivos='"+str(select)+"' and t2.eliminado=False")
            elec =cur.fetchall()
            print(tabulate(elec,headers=["Nombre archivo", "ID Agente", "ID Tel. Cliente", "Fecha y Hora", "Duracion (seg)", "Transcripcion", "Motivo de llamda", "Saliente"]))
            print()
            apro=input("Inserte (1) si desea aprobar la llamada, de manera contraria incerte (0): ")
            if apro==1:

                cur.execute("insert into aprobacion(nombre_archivo, id_supervisor, aprobacion)values('"+str(select)+"',"+str(sup)+",'True');" )
            if apro==0:

                cur.execute("insert into aprobacion(nombre_archivo, id_supervisor, aprobacion)values('"+str(select)+"',"+str(sup)+",'False');" )
            print()
            print('La llamada a sido calificada satisfactoriamente')
    if subopcion==2:
        sup =input("Ingrese su ID de supervisor para poder continuar: ")
        cur.execute("SELECT EXISTS(select * from supervisores s join tennant t on t.id=s.id_tennant where s.id="+str(sup)+" and t.nombre='"+str(content[t-1][1])+"')")
        valid= cur.fetchone()
        if valid[0]==True:
            print("Tu identificacion fue validada con exito")
            cur.execute("select s.id, t.nombre, s.nombre, s.apellido from supervisores s join tennant t on t.id=s.id_tennant where s.id="+str(sup)+";" )
            superv=cur.fetchall()
            print(tabulate(superv,headers=["ID", "Tennant", "Nombre", "Apellido"]))

            calif= input("Ingrese y seleccione de la lista de arriba, el nombre de archivo de la llamada de la cual desea editar su calificacion:" )
            cur.execute("select t1.nombre_archivo, t1.aprobacion from (aprobacion a join supervisores s on a.id_supervisor=s.id) as t1 join tennant t on t1.id_tennant=t.id where t.nombre='"+str(content[t-1][1])+"' and t1.eliminar_ap=False and t1.nombre_archivo='"+str(calif)+"';")
            aprov =cur.fetchall()
            print(tabulate(aprov,headers=["Nombre archivo", "Aprobada"]))
            print()
            apro1=input("Inserte (1) si desea aprobar la llamada, de manera contraria incerte (0): ")
            if apro1==1:

                cur.execute("update aprobacion set aprovacion='True' where nombre_archivos='"+str(aprov)+"'")
            if apro1==0:

                cur.execute("update aprobacion set aprovacion='False' where nombre_archivos='"+str(aprov)+"'")
            print()
            print('La llamada a sido calificada satisfactoriamente')
            
    if subopcion==3:
        sup =input("Ingrese su ID de supervisor para poder continuar: ")
        cur.execute("SELECT EXISTS(select * from supervisores s join tennant t on t.id=s.id_tennant where s.id="+str(sup)+" and t.nombre='"+str(content[t-1][1])+"')")
        valid= cur.fetchone()
        if valid[0]==True:
            print("Tu identificacion fue validada con exito")
            cur.execute("select s.id, t.nombre, s.nombre, s.apellido from supervisores s join tennant t on t.id=s.id_tennant where s.id="+str(sup)+";" )
            superv=cur.fetchall()
            print(tabulate(superv,headers=["ID", "Tennant", "Nombre", "Apellido"]))
            eliminar= input("Ingrese y seleccione de la lista de arriba, el nombre de archivo de la llamada cuya calificacion que desea eliminar :" )
            print()
            print()
            print("---------Esta segur@ de que desea eliminar la calificacion de la llamada "+eliminar+"? Una vez realizada esta accion no podra volver atras--------" )
            print()
            print()
            print("Confirme la eliminacion de la calificacion de "+eliminar+": ")
            print("\t1 para confirmar que desea eliminar la llamada")
            print("\t2 para deshaser esta accion")
            print()
            delete1=pdenuev4(2)
            if delete1==1:
                cur.execute("select a.eliminar_ap from aprobacion a where a.nombre_archivos ='"+eliminar+"';")
                eliminar=cur.fetchall()
                if eliminar[0][0]==False:
                    cur.execute("update aprobacion set eliminar_ap=True' where nombre_archivos='"+eliminar+"'")
                    conn.commit()
                    print("Llamada eliminada con exito")
                else:
                    print("La llamada ingresada no existe o ya a sido eliminada")

            elif delete1==2:
                print("Operacion cancelada")                
    subopcion=pdenuev4(3)
    if subopcion==1:
        idcamp=input("Ingrese el ID de la campaña que desea agregar (este cumplir con que sea un numero con al menos 3 digitos y sea mayor a 100): ")
        fechainicio=input("Ingrese la fecha de inicio de la campaña (Formato: AAAA/MM/DD) : ")
        fechafin=input("Ingrese la fecha de termino de la campaña (Formato: AAAA/MM/DD) : ")
        nombrecamp=input(" Ingrese el nombre de la campaña:" )
        cur.execute("insert into campana(id_tennant, fecha_inicio, fecha_fin, nombre)values("+str(idcamp)+",'"+str(fechainicio)+"','"+str(fechafin)+"','"+str(nombrecamp)+"');")
        conn.commit()
        print("Campaña agregada con exito")
    if subopcion==2:
        
        eliminar= input("Ingrese y seleccione de la lista de arriba, el nombre de archivo de la llamada cuya calificacion que desea eliminar :" )
        print()
        print()
        print("---------Esta segur@ de que desea eliminar la calificacion de la llamada "+eliminar+"? Una vez realizada esta accion no podra volver atras--------" )
        print()
        print()
        print("Confirme la eliminacion de la calificacion de "+eliminar+": ")
        print("\t1 para confirmar que desea eliminar la llamada")
        print("\t2 para deshaser esta accion")
        print()
        delete1=pdenuev4(2)
        if delete1==1:
            cur.execute("select a.eliminar_ap from aprobacion a where a.nombre_archivos ='"+eliminar+"';")
            eliminar=cur.fetchall()
            if eliminar[0][0]==False:
                cur.execute("update aprobacion set eliminar_ap=True' where nombre_archivos='"+eliminar+"'")
                conn.commit()
                print("Llamada eliminada con exito")
            else:
                print("La llamada ingresada no existe o ya a sido eliminada")

        elif delete1==2:
            print("Operacion cancelada")

    if subopcion==3:
        
        sup =input("Ingrese su ID de supervisor para poder continuar: ")
        cur.execute("SELECT EXISTS(select * from supervisores s join tennant t on t.id=s.id_tennant where s.id="+str(sup)+" and t.nombre='"+str(content[t-1][1])+"')")
        valid= cur.fetchone()
        if valid[0]==True:
            print("Tu identificacion fue validada con exito")
            cur.execute("select s.id, t.nombre, s.nombre, s.apellido from supervisores s join tennant t on t.id=s.id_tennant where s.id="+str(sup)+";" )
            superv=cur.fetchall()
            print(tabulate(superv,headers=["ID", "Tennant", "Nombre", "Apellido"]))

            calif= input("Ingrese y seleccione de la lista de arriba, el nombre de archivo de la llamada de la cual desea editar su calificacion:" )
            cur.execute("select t1.nombre_archivo, t1.aprobacion from (aprobacion a join supervisores s on a.id_supervisor=s.id) as t1 join tennant t on t1.id_tennant=t.id where t.nombre='"+str(content[t-1][1])+"' and t1.eliminar_ap=False and t1.nombre_archivo='"+str(calif)+"';")
            aprov =cur.fetchall()
            print(tabulate(aprov,headers=["Nombre archivo", "Aprobada"]))
            print()
            apro1=input("Inserte (1) si desea aprobar la llamada, de manera contraria incerte (0): ")
            if apro1==1:

                cur.execute("update aprobacion set aprovacion='True' where nombre_archivos='"+str(aprov)+"'")
            if apro1==0:

                cur.execute("update aprobacion set aprovacion='False' where nombre_archivos='"+str(aprov)+"'")
            print()
            print('La llamada a sido calificada satisfactoriamente')
            

def manejarcampana(t):
    conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
    cur = conn.cursor()
    cur.execute("SELECT t.id, t.nombre FROM tennant t")
    content=cur.fetchall()    
    print ()   
    cur=conn.cursor()
    cur.execute("select c.id, c.nombre from campana c where c.id_tennant='"+str(t)+"' and c.eliminar_ca=False;")
    aprov =cur.fetchall()
    print(tabulate(aprov,headers=["ID Campaña", "Nombre"]))
    print()
    print()
    print ("Lista de subopciones:")
    print ('i) Agregar campaña')
    print ('ii) Eliminar campaña')
    print ('iii) Editar campaña')
                
    subopcion=pdenuev4(3)
    if subopcion==1:
        idcamp=input("Ingrese el ID de la campaña que desea agregar (este cumplir con que sea un numero con al menos 3 digitos y sea mayor a 100): ")
        fechainicio=input("Ingrese la fecha de inicio de la campaña (Formato: AAAA/MM/DD) : ")
        fechafin=input("Ingrese la fecha de termino de la campaña (Formato: AAAA/MM/DD) : ")
        nombrecamp=input(" Ingrese el nombre de la campaña:" )
        cur.execute("insert into campana(id_tennant, fecha_inicio, fecha_fin, nombre)values("+str(idcamp)+",'"+str(fechainicio)+"','"+str(fechafin)+"','"+str(nombrecamp)+"');")
        conn.commit()
        print("Campaña agregada con exito")
    if subopcion==2:
        
        eliminar= input("Ingrese y seleccione de la lista de arriba, el ID de la campaña que desea eliminar :" )
        print()
        print()
        print("---------Esta segur@ de que desea eliminar la campaña ID: "+eliminar+"? Una vez realizada esta accion no podra volver atras--------" )
        print()
        print()
        print("Confirme la eliminacion de la campaña de ID: "+eliminar+": ")
        print("\t1 para confirmar que desea eliminar la llamada")
        print("\t2 para deshaser esta accion")
        print()
        delete1=pdenuev4(2)
        if delete1==1:
            cur.execute("select c.eliminar_ca from  campana c where c.id ="+eliminar+";")
            eliminar1=cur.fetchall()
            if eliminar[0][0]==False:
                cur.execute("update campana set eliminar_ca='True' where c.id="+eliminar1+";")
                conn.commit()
                print("Llamada eliminada con exito")
            else:
                print("La llamada ingresada no existe o ya a sido eliminada")

        elif delete1==2:
            print("Operacion cancelada")

    if subopcion==3:
        
        llam=input("Ingrese un ID de la lista de arriba de la campana que desea modificar:  ")
        conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
        cur=conn.cursor()
        cur.execute("select c.id, c.id_tennant, c.fecha_inicio, c.fecha_fin, c.nombre from campana c where c.id_tennant='"+str(t)+"' and c.eliminar_ca=False and c.id="+str(llam)+";")
        aprov =cur.fetchall()
        print(tabulate(aprov,headers=["(1)ID Campaña", "(2)ID Tennant", "(3)Fecha inicio", " (4)Fecha Termino", "(5)Nombre Campaña"]))
        llam2=pdenuev4(8)
        aux1=['id', 'id_tennant', 'fecha_inicio', 'fecha_fin','nombre']
        nuevo=input("Ingrese el/la nuev@ "+str(aux1[llam2-1])+":")
        nombcol=aux1[llam2-1]
        cur.execute("update campana set "+nombcol+"="+nuevo+"where id='"+llam+"'")
        conn.commit()
        print("Cambio guardado exitosamente")

def listatennants(imprimir=0):
    conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
    cur = conn.cursor()
    cur.execute("SELECT t.id, t.nombre FROM tennant t where eliminar_t='false'")
    content=cur.fetchall()
    l=[]
    for i in content:
        l.append(i[0])
    if imprimir==1:
        print ("Lista Tennants: ")
        print ()
        for i in content:
           print (str(i[0])+":"+i[1])
    cur.close()
    conn.close()
    return l






def siono():
    print()
    while True:
         try:
             print ("Ingrese [1] para ingresar al portal, [0] para salir")
             p = int(input("Por favor ingrese numero: "))
             if p not in [1,0]:
                 print("Oops! Su numero no es válido. Intente nuevamente...")
                 print()
                 continue
             else:
                 break
         except ValueError:
             print("Oops! Su numero no es válido. Intente nuevamente...")
    if p==0:
        print ("- - - - - - P O R T A L   T E R M I N A D O - - - - - - -")
        return False
    return True

def tennantSelect(listaidtennants):
    while True:
        try:
            p=input("Seleccione un id de los Tennant de la lista, o presione '0' para volver al menu anterior.\
 Si de lo contrario quiere agregar un tennant, presione 'tennant': ")
            if p=='tennant':
                agregarEntidad("tennant")
                a=1
                continue
            p=int(p)
            if p in listaidtennants:
                break
            if p==0:
                break
            print ("El Tennant no existe, intente nuevamente")
        except ValueError:
            print ("El Tennant no existe, intente nuevamente")
    return p

def listaIdEntidadSegunTennant(entidad,t,imprimir=False):
    if entidad=="tennant": content=listatennants()
    l=[]
    if entidad== "supervisores":
        texto="select id from "+entidad+" where eliminar_s='false' and id_tennant= "+str(t)+" ;"
    if entidad== "agente":
        texto="select id from "+entidad+" where eliminar_a='false' and id_tennant= "+str(t)+" ;"
    if entidad=="llamadas":
        texto="select id from "+entidad+" where eliminar_l='false' and id_tennant= "+str(t)+" ;"
    if entidad!="tennant":
        conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
        cur=conn.cursor()
        t=str(t)
        cur.execute(texto)
        content=cur.fetchall()
        cur.close()
        conn.close()
        for i in content:
            if imprimir==True:
                print (i[0])
            l.append(i[0])
    if entidad=="tennant":
        for i in content:
            if imprimir==True:
                print (i)
            l.append(i)
    
    return l

def pdenuev4(k):
    while True:
         try:
             x =int(input("Introduzca una opcion 1-"+str(k)+": "))
             if x>=k+1 or x<=0:
                 print("Oops! La opcion ingresada no es válida. Intente nuevamente...")
                 continue
             else:
                 break
         except ValueError:
             print("Oops! La opcion ingresada no es válida. Intente nuevamente...")
    return x
        
def editarInfoEntidad(t,entidad):
    asd=""
    nombre=""
    apellido=""
    columnas=[]
    valores=[]
    listaentidadtennant= listaIdEntidadSegunTennant(entidad,t)    
    while True:
        try:
            tupla=int(input("Seleccione el id del "+entidad+" que quiere modificar, o presione '0' para volver al menu anterior: "))
            if tupla==0:
                break
            if not (tupla in listaentidadtennant):
                print ("Seleccion imposible")
            break
        except ValueError:
            print ("Debes ingresar un dato numerico")
    if tupla==0:
        return None
    if entidad=="agente":
        asd="telefono, "
        columnas2=["id tennant: ","telefono: ","nombre: ","apellido: "]
    texto="Select id_tennant, "+asd+"nombre, apellido from "+entidad+" where id="+str(tupla)+";"
    conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
    cur=conn.cursor()
    cur.execute(texto)
    content=cur.fetchall()
    cur.close()
    conn.close()
    if entidad=="supervisores":
        columnas2=["id tennant: ","telefono: ","nombre: ","apellido: "]
    for i in range(len(content[0])):
        print (columnas2[i]+str(content[0][i]))
    while True:
        o4=input("Desea modificar el id del tennant? (s/n), o presione '0' para volver al menu anterior: ")
        if o4=="0": break
        if o4 not in ["s","n"]:
            print ("Opcion invalida")
            continue
        break
    if o4=="0":
        return None
    if o4=="s":
        columnas.append("id_tennant")
        l=listatennants()
        while True:
            listatennants(1)
            try:
                idtennant=int(input("Escriba un nuevo id de tennant de la lista: "))
                if idtennant not in l:
                    print ("Opcion inválida")
                    continue
                valores.append(idtennant)
                break
            except ValueError:
                print ("Debes ingresar un dato numerico")
    if entidad=="agente":
        while True:
            o3=input("Desea modificar el telefono? (s/n), o presione '0' para volver al menu anterior: ")
            if o3=="0": break
            if o3 not in ["s","n"]:
                print ("Opcion invalida")
                continue
            break
        if o3=="0": return None
        if o3=="s":
            columnas.append("telefono")
            while True:
                telefono=input("Escriba el nuevo telefono: ")
                numbersstr=["1","2","3","4","5","6","7","8","9","0"]
                b=0
                for i in telefono:
                    if i not in numbersstr:
                        b=1
                if b==1:
                    print ("Telefono invalido, ingreselo nuevamente")
                    continue
                conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
                cur=conn.cursor()
                cur.execute("select a. telefono from agente a;")
                content=cur.fetchall()
                cur.close()
                conn.close()
                a=0
                for i in content:
                    if i[0]==int(telefono):
                        print ("Teléfono en uso, ingrese otro")
                        a=1
                if a==1: continue
                break                
            valores.append(telefono)
    while True:
        o1=input("Desea modificar el nombre? (s/n), o presione '0' para volver al menu anterior: ")
        if o1=='0':
            break
        if o1 not in ["s","n"]:
            print ("Opcion invalida, ingresela nuevamente")
            continue
        break
    if o1=='0': return None
    if o1=="s":
        columnas.append("nombre")
        a=0
        while True:
            nombre=input("Ingrese el nuevo nombre del "+entidad+", o presione '0' para volver al menu anterior: ")
            if nombre=="0":
                break
            for i in nombre:
                if i not in ascii_letters:
                    a=1
                    break
                else: a=0
            if a==1:
                print ("el campo nombre no acepta caracteres especiales")
                continue
            if nombre=="":
                print ("ese no es un nombre válido")
                continue
            valores.append(nombre)
            break
    if nombre=="0": return
    while True:
        o2=input("Desea modificar el apellido? (s/n), o presione '0' para volver al menu anterior: ")
        if o2=='0':
            break
        if o2 not in ["s","n"]:
            print ("Opcion invalida, ingresela nuevamente")
            continue
        break
    if o2=='0': return None
    if o2=="s":
        columnas.append("apellido")
        a=0
        while True:
            apellido=input("Ingrese el nuevo apellido del "+entidad+", o presione '0' para volver al menu anterior: ")
            if apellido=="0":
                break
            for i in apellido:
                if i not in ascii_letters:
                    a=1
                    break
                else: a=0
            if a==1:
                print ("El campo apellido no acepta caracteres especiales")
                continue
            if apellido=="":
                print ("Ese no es un apellido válido")
                continue
            valores.append(apellido)
            break
    if apellido=="0": return
    if columnas==[]:
        return None
    texto=sql("update",entidad,columnas,valores,"id="+str(tupla))    
    conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
    cur=conn.cursor()
    cur.execute(texto)
    conn.commit()
    cur.close()

def agente(t,sp):
    if sp==1:
        return agregarEntidad("agente",t)
    if sp==2:
        return editarInfoEntidad(t,"agente")
    if sp==3:
        return eliminarEntidad(t,"agente")
    return None

def supervisor(t,sp):
    if sp==1:
        return agregarEntidad("supervisores",t)
    if sp==2:
        return editarInfoEntidad(t,"supervisores")
    if sp==3:
        return eliminarEntidad(t,"supervisores")
    return None

def agregarEntidad(entidad,t=0):
    a=0
    while True:
        nombre=input("Ingrese el nombre del "+entidad+", o presione '0' para volver al menu anterior: ")
        if nombre=="0":
            break
        for i in nombre:
            if i not in ascii_letters:
                a=1
                break
            a=0
        if a==1:
            print ("el campo nombre no acepta caracteres especiales")
            continue
        if nombre=="":
            print ("ese no es un nombre válido")
            continue
        break
    if nombre=="0": return
    if entidad!="tennant" and entidad!="campana":
        while True:
            apellido=input("Ingrese el apellido del "+entidad+", o presione '0' para volver al menu anterior: ")
            if apellido=="0":
                break
            for i in apellido:
                if i not in ascii_letters:
                    a=1
                    break
                else: a=0
            if a==1:
                print ("el campo apellido no acepta caracteres especiales")
                continue
            if apellido=="":
                print ("ese no es un apellido válido")
                continue
            break
        if apellido=="0": return
        a=0
    if idtennant=='0':
        return 
    if entidad=="agente" or entidad=="tennant":
        optelefono="telefono"
        while True:
            asf=9
            if a==1:
                print ("Telefono solo acepta caracteres del tipo int, ingreselo nuevamente")
            telefono=input("Ingrese el telefono del "+entidad+", o presione 'inicio' para volver al menu anterior: ")
            if telefono=="inicio":
                break
            a=0
            for i in telefono:
                if i not in numbersstr:
                    a=1
            if a==1: continue
            conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
            cur=conn.cursor()
            cur.execute("select telefono from "+entidad)
            content=cur.fetchall()
            cur.close()
            conn.close()
            
            for i in content:
                if i[0]==int(telefono):
                       print ("Este telefono ya esta en uso, ingreselo nuevamente")
                       asf=0
                       break
            if asf==0: continue
            telefono=int(telefono)
            break
        if telefono=="inicio": return
#        conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
 #       cur=conn.cursor()
  #      cur.execute("INSERT into "+entidad+"(nombre,apellido,"+optelefono+"id_tennant) values (%s,%s,%s,%s);",(nombre,apellido,telefono,t))
   #     conn.commit()
    #    cur.close()
     #   conn.close()
    if entidad=="supervisores":
        optelefono=""
    if entidad=="tennant":
        conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
        cur=conn.cursor()
        cur.execute("INSERT into "+entidad+"(nombre,"+optelefono+") values (%s,%s);",(nombre,telefono))
        conn.commit()
        cur.close()
        conn.close()
        print ("Tennant agregado exitosamente")
    if entidad=="agente":
        conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
        cur=conn.cursor()
        cur.execute("INSERT into "+entidad+"(nombre,apellido,telefono,id_tennant) values (%s,%s,%s,%s);",(nombre,apellido,telefono,t))
        conn.commit()
        cur.close()
        conn.close()
    if entidad=="supervisores":
        conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
        cur=conn.cursor()
        cur.execute("INSERT into "+entidad+"(nombre,apellido,id_tennant) values (%s,%s,%s);",(nombre,apellido,t))
        conn.commit()
        cur.close()
        conn.close()
        
def eliminarEntidad(tennant,entidad):
    li= listaIdEntidadSegunTennant(entidad,tennant)
    while True:
        try:
            a=0
            c=0
            if entidad!="tennant":
                for i in li:
                    print (i)
                instancia=input("Seleccione que "+entidad+" de la lista desea eliminar, o presione 'n' para volver al menu anterior: ")
                if instancia=='n':
                    break
                instancia=int(instancia)
                if instancia not in li:
                    print ("El "+entidad+" seleccionado no existe o no pertenece a este tennant")
                    a=1
                if a==1:continue
            seguro=input("Si está seguro de eliminar este "+entidad+" presione 1, de lo contrario presione cualquier otr tecla: ")
            for i in seguro:
                if i not in numbersstr:
                    c=1
            if c==1:
                continue
            if seguro=="1":
                break
            continue
        except ValueError:
            print ("Ese "+entidad+" no existe, intente nuevamente")
            continue
    if entidad!="tennant":
        if instancia=='n': return
    if entidad=="tennant":
        texto="update "+entidad+" set eliminar_t='true' where id="+str(tennant)
    if entidad=="agente":
        texto="update "+entidad+" set eliminar_a='true' where id="+str(instancia)
    if entidad=="supervisores":
        texto="update "+entidad+" set eliminar_s='true' where id="+str(instancia)
    if entidad=="llamada":
        texto="update "+entidad+" set eliminar_l='true' where nombre_archivos="+str(instancia)
    print (texto)
    conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
    cur=conn.cursor()
    cur.execute(texto)
    conn.commit()
    cur.close()
    

def verLlamada(t,subopcion):            
        if subopcion==1:
            narch= input("Ingrese el nombre de archivo de la llamada que desea ver: ")
            print ()
            conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
            cur=conn.cursor()
            cur.execute("select l.eliminar_l from llamadas l where nombre_archivos ='"+narch+"';")
            eliminado=cur.fetchall()
            #print ( type(eliminado[0][0]))
            if eliminado[0][0]==False:
                cur.execute("select t2.nombre_archivos, t2.id_agente, t2.id_tel_cliente, t2.fecha_hora, t2.duracion_seg, t2.transcripcion, t2.motivo_llamada, t2.saliente from (((llamadas l join telefono_cliente tc on l.id_tel_cliente= tc.id ) as t0 join agente a on t0.id_agente=a.id)as t1 join clientes c on c.id= t1.id_cliente) as t2 join tennant t on t2.id_tennant=t.id where t.id="+str(t)+" and t2.nombre_archivos='"+narch+"' and t2.eliminar_l=False")
                llamadas =cur.fetchall()
                print(tabulate(llamadas,headers=["Nombre archivo", "ID Agente", "ID Tel. Cliente", "Fecha y Hora", "Duracion (seg)", "Transcripcion", "Motivo de llamda", "Saliente"]))
                conn.commit()
                print ()
            else:
                    print("La llamada ingresada no existe o fue eliminada")
            
        if subopcion==2:
            print("Tipo de llamada:")
            print("\t1) Saliente") 
            print("\t2) Entrante")
            conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
            cur=conn.cursor()
            sal=pdenuev4(2)
            if sal==1:
                campana = input("Ingrese el Id de la campaña a la cual pertenece la llamada: ")
                nombarch= input("Ingrese el nombre de archivo de la llamada:")
                agente= input("Ingrese el ID del agente que realizo la llamada:" )
                tel = input("Ingrese el ID del telefono que recibio la llamada: ")
                fecha = input("Ingrese la fecha en la que se realizo la llamada(AAAA/MM/DD):")
                hora = input("Ingrese la hora en la que se realizo la llamada(HH:MM:SS):")
                dur = input("Ingrese la cantidad de segundos que duro la llamada:")
                trans = input("Ingrese la transcipcion de la llamada: ")
                horafecha = fecha+" "+hora
                saliente ="true"
                cur.execute("insert into llamadas(nombre_archivos, id_agente, id_tel_cliente, id_campana, fecha_hora, duracion_seg, transcripcion, saliente)values(%s,%s,%s,%s,%s,%s,%s,%s);",(nombarch, agente, tel, campana, horafecha, dur, trans, saliente))
                conn.commit()
                print("Llamada registrada exitosamente")
            elif sal==2:
                motivo = input("Ingrese el motivo por el cual se llamo: ")
                nombarch= input("Ingrese el nombre de archivo de la llamada:")
                agente= input("Ingrese el ID del agente que recibio la llamada:" )
                tel = input("Ingrese el ID del telefono que realizo la llamada: ")
                fecha = input("Ingrese la fecha en la que se realizo la llamada(AAAA/MM/DD):")
                hora = input("Ingrese la hora en la que se realizo la llamada(HH:MM:SS):")
                dur = input("Ingrese la cantidad de segundos que duro la llamada:")
                trans = input("Ingrese la transcipcion de la llamada: ")
                horafecha = fecha+" "+hora
                saliente ="false"
                cur.execute("insert into llamadas(nombre_archivos, id_agente, id_tel_cliente, fecha_hora, duracion_seg, transcripcion,motivo_llamada, saliente)values(%s,%s,%s,%s,%s,%s,%s,%s);",(nombarch, agente, tel, horafecha, dur, trans,  motivo, saliente))
                conn.commit()
                print("Llamada registrada exitosamente")
            
            
        if subopcion==3:
            llam=input("Ingrese el nombre de archivo de la llamada que desea modificar:  ")
            conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
            cur=conn.cursor()
            cur.execute("select t2.nombre_archivos, t2.id_agente, t2.id_tel_cliente, t2.fecha_hora, t2.duracion_seg, t2.transcripcion, t2.motivo_llamada, t2.saliente from (((llamadas l join telefono_cliente tc on l.id_tel_cliente= tc.id ) as t0 join agente a on t0.id_agente=a.id)as t1 join clientes c on c.id= t1.id_cliente) as t2 join tennant t on t2.id_tennant=t.id where t2.nombre_archivos= '"+llam+"' ;")
            llam1=cur.fetchall()
            print(tabulate(llam1,headers=["(1)Nombre archivo", "(2)ID Agente", "(3)ID Tel. Cliente", "(4)Fecha y Hora", "(5)Duracion (seg)", "(6)Transcripcion", "(7)Motivo de llamda", "(8)Saliente"]))
            llam2=pdenuev4(8)
            aux1=['nombre_archivos', 'id_agente', 'id_tel_cliente', 'fecha_hora', 'duracion_seg', 'transcripcion', 'motivo_llamada', 'saliente']
            nuevo=input("Ingrese el/la nuev@ "+str(aux1[llam2-1])+":")
            nombcol=aux1[llam2-1]
            cur.execute("update llamadas set "+nombcol+"="+nuevo+"where nombre_archivos='"+llam+"'")
            conn.commit()
            print("Cambio guardado exitosamente")
        
        if subopcion==4:
            delete=input("Ingrese el nombre de archivo de la llamada que desea eliminar : ")
            print()
            print()
            print("---------Esta segur@ de que desea eliminar la llamada "+delete+"? Una vez realizada esta accion no podra volver atras--------" )
            print()
            print()
            print("Confirme la eliminacion de la llamada "+delete+": ")
            print("\t1 para confirmar que desea eliminar la llamada")
            print("\t2 para deshacer esta accion")
            delete1=pdenuev4(2)
            if delete1==1:
                conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
                cur=conn.cursor()
                cur.execute("select l.eliminar_l from llamadas l where nombre_archivos ='"+delete+"';")
                eliminar=cur.fetchall()
                if eliminar[0][0]==False:
                    cur.execute("update llamadas set eliminar_l=true where nombre_archivos='"+delete+"'")
                    conn.commit()
                    print("Llamada eliminada con exito")
                else:
                    print("La llamada ingresada no existe o ya a sido eliminada")

            elif delete1==2:
                print("Operacion cancelada")
                
def ejecutarConsulta(t,opcion,subopcion):
    if opcion==1:
        verLlamada(t,subopcion)
    if opcion==2:
        evaluarllamada(t)
    if opcion==3:
        manejarcampana(t)
    if opcion==4:
        if subopcion==1:
            print ("agregarTipificacion(t)")
        if subopcion==2:
            print ("asociarTipificacion(t)")
        if subopcion==3:
            print ("eliminarTipificacion(t)")
        if subopcion==4:
            print ("editarTipificacion(t)")
        if subopcion==5:
            print ("editarAsociacion(t)")
    if opcion==5:
        agente(t,subopcion)
    if opcion==6:
        supervisor(t,subopcion)
    if opcion==7:
        if subopcion==1:
            print ("EditarTennant(t)")
        if subopcion==2:
            eliminarEntidad(t,"tennant")


def sql(accion,tabla,lista_columnas,lista_valores,condicion=0):
    if accion.lower()=="update":
        columnavalores=""
        for i in range(len(lista_columnas)):
            a=str(lista_columnas[i])+"="+str(lista_valores[i])+", "
            columnavalores=columnavalores+a
        if not condicion==0:
            sentencia= accion+" " +tabla+" "+"set "+columnavalores+" where "+condicion
            return sentencia

def optionSelect(opciones,t):
    opcionesstr=[]
    largo=range(len(opciones))
    for i in largo:
        b= "["+str(i+1)+"]"+" "+opciones[i][0]
        opcionesstr.append(b)
    while True:
        try:
            for i in opcionesstr:
                print (i)
            p=int(input("Seleccione el numero de opcion de la lista, o seleccione '0' si quiere volver al menu anterior: "))
            if p==0:
                break
            if p-1 in largo:
                break
            print ("La opcion no existe, intente nuevamente")
        except ValueError:
            print ("La opcion no existe, intente nuevamente")
            continue
    if p==5:
        print ("Agentes del tennant cuyo id es "+str(t))
        listaIdEntidadSegunTennant("agente",t,True)
    if p==6:
        print ("Supervisores del tennant cuyo id es "+str(t))
        listaIdEntidadSegunTennant("supervisores",t,True)
    if p==1:
        print ()
        conn=psycopg2.connect(database="grupo3",user="grupo3",password="eXVu6P",host= "201.238.213.114", port="54321")
        cur=conn.cursor()
        cur.execute("select t2.nombre_archivos from (((llamadas l join telefono_cliente tc on l.id_tel_cliente=tc.id and l.eliminar_l='false') as t0 join agente a on t0.id_agente=a.id)as t1 join clientes c on c.id= t1.id_cliente) as t2 join tennant t on t2.id_tennant=t.id where t.id="+str(t))
        llamadas =cur.fetchall()
        print(tabulate(llamadas,headers=["Nombre archivo", "ID Agente", "ID Tel. Cliente", "Fecha y Hora", "Duracion (seg)", "Transcripcion", "Motivo de llamda", "Saliente"]))
        print()
        print()
    
    return p

def suboptionSelect(t,opcion):
    if opcion!=1 or opcion!=3 or opcion!=2:
        largo=range(len(opciones[opcion-1][1]))
        suboptstr=[]
        for i in largo:
            b= opciones[opcion-1][1][i]
            suboptstr.append(b)
    while True:
        try:
            for i in suboptstr:
                print (i)
            p=int(input("Seleccione la subopcion de la lista de manera ordinal ('i'=1,'ii'=2,etc), o seleccione '0' si quiere volver al menu anterior: "))
            if p==0:
                break
            if p-1 in largo:
                break
            print ("La subopcion no existe, intente nuevamente")
        except ValueError:
            print ("La subopcion no existe, intente nuevamente")
            continue
    return p


def ciclo0():
    if siono():
        ciclo1()

def ciclo1():
    t=tennantSelect(listatennants(1))
    if t==0 or t=="tennant":
        return ciclo0()
    return ciclo2(t)
    
    
def ciclo2(t):
    opcion=optionSelect(opciones,t)
    if opcion==0:
        return ciclo1()
    if opcion==2:
        evaluarllamada(t)
        
    return ciclo3(opcion,t)
    
def ciclo3(opcion,t):
    subopcion=suboptionSelect(t,opcion)
    if subopcion==0:
        return ciclo2(t)
    ejecutarConsulta(t,opcion,subopcion)
    return ciclo3(opcion,t)
    


    
numbers=[1,2,3,4,5,6,7,8,9,0]  
numbersstr=["1","2","3","4","5","6","7","8","9","0"]
opciones=[['Ver llamadas',["i) Ver llamadas","ii) Agregar llamada","iii) Editar llamada","iv) Eliminar llamada"]],\
['Evaluar llamadas',["i) Agregar calificacion","ii) Editar calificacion","iii) Eliminar calificacion"]],\
['Manejar campanas',["i) Agregar camapana","ii) Editar campana","iii) Eliminar campana"]],\
['Manejar tipificaciones',["i) Agregar tipificacion","ii) Asociar tipificacion","iii) Eliminar tipificacion","iv) Editar tipificacion","v) Editar Asociacion"]],\
['Manejar agentes',["i) Agregar agente","ii) Editar agente","iii) Eliminar agente"]],\
['Manejar supervisores',["i) Agregar supervisor","ii) Editar informacion","iii) Eliminar supervisor"]],\
['Manejar tennant',["i) Editar tennant","ii) Eliminar tennant"]]]


ciclo0()
