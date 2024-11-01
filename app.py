from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analizar_lexico(curp):
    tokens = [
        {"Tipo": "Apellido Paterno", "Token": curp[0:2]},
        {"Tipo": "Apellido Materno", "Token": curp[2:3]},
        {"Tipo": "Nombre", "Token": curp[3:4]},
        {"Tipo": "Año de Nacimiento", "Token": curp[4:6]},
        {"Tipo": "Mes de Nacimiento", "Token": curp[6:8]},
        {"Tipo": "Día de Nacimiento", "Token": curp[8:10]},
        {"Tipo": "Sexo", "Token": curp[10:11]},
        {"Tipo": "Estado", "Token": curp[11:13]},
        {"Tipo": "Consonante Paterno", "Token": curp[13:14]},
        {"Tipo": "Consonante Materno", "Token": curp[14:15]},
        {"Tipo": "Consonante Nombre", "Token": curp[15:16]},
        {"Tipo": "Número asignado con año de nacimiento", "Token": curp[16:17]},
        {"Tipo": "Código verificador", "Token": curp[17:18]},
    ]
    return tokens

def analizar_sintactico(curp):
    errores = []
    
    # Verificar longitud
    if len(curp) != 18:
        errores.append("Error de sintaxis: La CURP debe tener exactamente 18 caracteres.")
        return errores
    
    # Verificar cada componente con mensajes específicos
    if not re.match(r'^[A-Z]{2}$', curp[0:2]):
        errores.append("Error de sintaxis: Debe contener Primera letra y vocal del primer apellido.")
        
    if not re.match(r'^[A-Z]$', curp[2:3]):
        errores.append("Error de sintaxis: Debe contener primera letra del apellido materno.")
        
    if not re.match(r'^[A-Z]$', curp[3:4]):
        errores.append("Error de sintaxis: Debe contener primera letra del nombre .")
    
    # Verificación del año de nacimiento
    año_nacimiento = int(curp[4:6])
    if not (0 <= año_nacimiento <= 23 or 50 <= año_nacimiento <= 99):
        errores.append("Error de sintaxis: Debe estar entre 1950 y 2023.")
    
    # Verificación del mes de nacimiento
    mes_nacimiento = int(curp[6:8])
    if not (1 <= mes_nacimiento <= 12):
        errores.append("Error de sintaxis: Debe ser un mes valido.")
    
    # Verificación del día de nacimiento según el mes
    dia_nacimiento = int(curp[8:10])
    dias_por_mes = {
        1: 31, 2: 29 if año_nacimiento % 4 == 0 else 28, 3: 31, 4: 30,
        5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    if not (1 <= dia_nacimiento <= dias_por_mes.get(mes_nacimiento, 31)):
        errores.append(f"Error de sintaxis: Debe estar entre 01 y {dias_por_mes.get(mes_nacimiento, 31)} para el mes {mes_nacimiento:02}.")

    # Continuar con las demás validaciones (sexo, estado, etc.)
    if curp[10:11] not in ['H', 'M']:
        errores.append("Error de sintaxis: Debe ser 'H' (Hombre) o 'M' (Mujer).")
        
    estados_validos = ["AS", "BC", "BS", "CC", "CL", "CM", "CS", "CH", "DF", "DG", "GT", "GR", "HG", "JC", "MC", "MN", "MS", "NT", "NL", "OC", "PL", "QT", "QR", "SP", "SL", "SR", "TC", "TS", "TL", "VZ", "YN", "ZS", "NE"]
    if curp[11:13] not in estados_validos:
        errores.append("Error de sintaxis: Código de estado no válido.")
        
    if not re.match(r'^[A-Z]$', curp[13:14]):
        errores.append("Error de sintaxis: Debe ser una letra.")
        
    if not re.match(r'^[A-Z]$', curp[14:15]):
        errores.append("Error de sintaxis: Debe ser una letra.")
        
    if not re.match(r'^[A-Z]$', curp[15:16]):
        errores.append("Error de sintaxis: Debe ser una letra.")
        
    if not re.match(r'^[A-Z0-9]$', curp[16:17]):
        errores.append("Error de sintaxis: Debe ser un dígito o una letra.")
        
    if not re.match(r'^[0-9A-Z]$', curp[17:18]):
        errores.append("Error de sintaxis: Debe ser un dígito o una letra.")
    
    return errores if errores else ["Sintaxis Correcto "]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analizar', methods=['POST'])
def analizar():
    curp = request.form.get("curp").upper()
    tokens = analizar_lexico(curp)
    errores = analizar_sintactico(curp)
    es_valido = "Sintaxis Correcto" in errores
    return render_template("index.html", tokens=tokens, errores=errores, es_valido=es_valido, curp=curp)

if __name__ == "__main__":
    app.run(debug=True)
