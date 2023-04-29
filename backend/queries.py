from datetime import datetime

class queries:
    
    def captainIdGetJson(cursor, requestJson, n = ""):
        if('captainid' in requestJson):
            return requestJson['captainid']
        emptyBool = True
        for i in ('firstname', 'lastname','captain_rank','homeplanet'):
            if (n+i) in requestJson:
                emptyBool = False
                requestJson[i]=requestJson[n+i]
        if(emptyBool):
            return None
        query1, values1 = queries.captainGetJson(requestJson)
        cursor.execute(query1, values1)
        captainList = cursor.fetchone()
        if captainList is not None:
            captainNewId = captainList[0]
            return captainNewId
        return None
    
    def captainIdGetParam(cursor, request):
        if(request.args.get('captainid') is not None):
            return request.args.get('captainid')
        emptyBool = True
        for i in ('firstname', 'lastname','captain_rank','homeplanet'):
            if i in request.args:
                emptyBool = False
        if(emptyBool):
            return None
        query1, values = queries.captainGet(request)
        cursor.execute(query1, values)
        captainList = cursor.fetchone()
        if captainList is not None:
            captainNewId = captainList[0]
            return captainNewId
        return None
    
###############################################
    
    def captainGet(request):
        returnstring = "SELECT * FROM captain"
        values = []
        totalConditions = 0
        for i in ('id', 'firstname', 'lastname','captain_rank','homeplanet'):
            if i in request.args:
                if(totalConditions > 0):
                    returnstring += " AND"
                else:
                    returnstring += " WHERE"
                returnstring += " " + i + " = %s"
                values.append(request.args.get(i))
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
    def captainGetJson(request):
        returnstring = "SELECT * FROM captain"
        values = []
        totalConditions = 0
        for i in ('id', 'firstname', 'lastname','captain_rank','homeplanet'):
            if i in request:
                if(totalConditions > 0):
                    returnstring += " AND"
                else:
                    returnstring += " WHERE"
                returnstring += " " + i + " = %s"
                values.append(request[i])
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
    captainInsert = """INSERT INTO captain (id, firstname, lastname, captain_rank, homeplanet) 
            VALUES (UUID_TO_BIN(UUID()), %s, %s, %s, %s);"""
    
    def captainUpdate(request):
        captain = request.get_json()
        returnstring = "UPDATE captain SET"
        values = []
        totalConditions = 0
        for i in ('new_firstname', 'new_lastname','new_captain_rank','new_homeplanet'):
            if i in captain:
                if(totalConditions > 0):
                    returnstring += ","
                if(len(i)>4):
                    temp = i[4:]
                returnstring += " " + temp + " = %s"
                values.append(captain[i])
                totalConditions+=1
        returnstring += " WHERE"
        totalConditions = 0
        for i in ('id', 'old_firstname', 'old_lastname','old_captain_rank','old_homeplanet'):
            if i in captain:
                if(totalConditions > 0):
                    returnstring += " AND"
                if(len(i)>4):
                    temp = i[4:]
                returnstring += " " + temp + " = %s"
                values.append(captain[i])
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
    def captainDelete(request):
        captain = request.get_json()
        returnstring = "DELETE FROM captain WHERE"
        values = []
        totalConditions = 0
        for i in ('id', 'firstname', 'lastname','captain_rank','homeplanet'):
            if i in captain:
                if(totalConditions > 0):
                    returnstring += " AND"
                returnstring += " " + i + " = %s"
                values.append(captain[i])
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
###############################################
    
    def spaceshipGet(request):
        returnstring = "SELECT * FROM spaceship"
        values = []
        totalConditions = 0
        for i in ('id', 'name', 'maxweight','captainid'):
            if i in request.args:
                if(totalConditions > 0):
                    returnstring += " AND"
                else:
                    returnstring += " WHERE"
                returnstring += " " + i + " = %s"
                values.append(request.args.get(i))
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
    def spaceshipGetJson(request):
        returnstring = "SELECT * FROM spaceship"
        values = []
        totalConditions = 0
        for i in ('id', 'name', 'maxweight','captainid'):
            if i in request:
                if(totalConditions > 0):
                    returnstring += " AND"
                else:
                    returnstring += " WHERE"
                returnstring += " " + i + " = %s"
                values.append(request[i])
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
    spaceshipInsert = """INSERT INTO spaceship (id, name, maxweight, captainid) 
            VALUES (UUID_TO_BIN(UUID()), %s, %s, %s);"""

    
    def spaceshipUpdate(spaceship):
        returnstring = "UPDATE spaceship SET"
        values = []
        totalConditions = 0
        for i in ('new_name', 'new_maxweight','new_captainid'):
            if i in spaceship:
                if(totalConditions > 0):
                    returnstring += ","
                if(len(i)>4):
                    temp = i[4:]
                returnstring += " " + temp + " = %s"
                values.append(spaceship[i])
                totalConditions+=1
        returnstring += " WHERE"
        totalConditions = 0
        for i in ('id', 'old_name', 'old_maxweight','old_captainid'):
            if i in spaceship:
                if(totalConditions > 0):
                    returnstring += " AND"
                if(len(i)>4):
                    temp = i[4:]
                returnstring += " " + temp + " = %s"
                values.append(spaceship[i])
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
    def spaceshipDelete(spaceship):
        returnstring = "DELETE FROM spaceship WHERE"
        values = []
        totalConditions = 0
        for i in ('id', 'name', 'maxweight','captainid'):
            if i in spaceship:
                if(totalConditions > 0):
                    returnstring += " AND"
                returnstring += " " + i + " = %s"
                values.append(spaceship[i])
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
###############################################
    
    def spaceshipIdGetJson(cursor, requestJson, m = ""):
        if('shipid' in requestJson):
            return requestJson['shipid']
        emptyBool = True
        for i in ('name', 'maxweight','captainid','firstname', 'lastname','captain_rank','homeplanet'):
            if (m+i) in requestJson:
                emptyBool = False
                requestJson[i]=requestJson[m+i]
        if(emptyBool):
            return None
        captainid= queries.captainIdGetJson(cursor, requestJson, n = m)
        if captainid is not None:
            requestJson['captainid'] = captainid
        query1, values1 = queries.spaceshipGetJson(requestJson)
        cursor.execute(query1, values1)
        spaceshipList = cursor.fetchone()
        if spaceshipList is not None:
            spaceshipNewId = spaceshipList[0]
            return spaceshipNewId
        return None
    
    def spaceshipIdGetParam(cursor, request):
        if(request.args.get('shipid') is not None):
            return request.args.get('shipid')
        emptyBool = True
        for i in ('name', 'maxweight','captainid','firstname', 'lastname','captain_rank','homeplanet'):
            if i in request.args:
                emptyBool = False
        if(emptyBool):
            return None
        captainid = queries.captainIdGetParam(cursor, request)
        if(captainid is not None):
            return None
        assert request.args['captainid'] == captainid
        query1, values1 = queries.spaceshipGet(request)
        cursor.execute(query1, values1)
        spaceshipList = cursor.fetchone()
        if spaceshipList is not None:
            spaceshipNewId = spaceshipList[0]
            return spaceshipNewId
        return None

###############################################
    
    def cargoGet(request):
        returnstring = "SELECT * FROM cargo"
        values = []
        totalConditions = 0
        for i in ('id', 'weight', 'cargotype', 'departure', 'arrival', 'shipid'):
            if i in request.args:
                if(totalConditions > 0):
                    returnstring += " AND"
                else:
                    returnstring += " WHERE"
                returnstring += " " + i + " = %s"
                values.append(request.args.get(i))
                totalConditions+=1
    
        if request.args.get('completedFilter') == 'true':
            current_date = datetime.utcnow()
            if totalConditions > 0:
                returnstring += " AND arrival > %s"
            else:
                returnstring += " WHERE arrival > %s"
            values.append(current_date)
        
        returnstring += ";"
        return returnstring, values
    
    cargoInsert = """INSERT INTO cargo (id, weight, cargotype, departure, arrival, shipid) 
            VALUES (UUID_TO_BIN(UUID()), %s, %s, %s, %s, %s);"""
    
    def cargoUpdate(cargo):
        returnstring = "UPDATE cargo SET"
        values = []
        totalConditions = 0
        for i in ('new_weight', 'new_cargotype', 'new_departure', 'new_arrival', 'new_shipid'):
            if i in cargo:
                if(totalConditions > 0):
                    returnstring += ","
                if(len(i)>4):
                    temp = i[4:]
                returnstring += " " + temp + " = %s"
                values.append(cargo[i])
                totalConditions+=1
        returnstring += " WHERE"
        totalConditions = 0
        for i in ('id', 'old_weight', 'old_cargotype', 'old_departure', 'old_arrival', 'old_shipid'):
            if i in cargo:
                if(totalConditions > 0):
                    returnstring += " AND"
                if(len(i)>4):
                    temp = i[4:]
                returnstring += " " + temp + " = %s"
                values.append(cargo[i])
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    
    def cargoDelete(cargo):
        returnstring = "DELETE FROM cargo WHERE"
        values = []
        totalConditions = 0
        for i in ('id', 'weight', 'cargotype', 'departure', 'arrival', 'shipid'):
            if i in cargo:
                if(totalConditions > 0):
                    returnstring += " AND"
                returnstring += " " + i + " = %s"
                values.append(cargo[i])
                totalConditions+=1
        returnstring += ";"
        return returnstring, values
    