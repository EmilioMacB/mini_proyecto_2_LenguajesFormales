
import ply.yacc as yacc
from lexer_json import tokens

def p_json(p):
    'json : LBRACKET elements RBRACKET'
    p[0] = p[2]  # La raiz es una lista de elementos

def p_elements_multiple(p):
    'elements : object COMMA elements'
    p[0] = [p[1]] + p[3] # Agrega el objeto actual a la lista restante

def p_elements_single(p):
    'elements : object'
    p[0] = [p[1]] 
    
def p_object(p):
    'object : LBRACE members RBRACE'
    p[0] = p[2] # El objeto es el diccionario de sus miembros

def p_members_multiple(p):
    'members : pair COMMA members'
    p[3].update(p[1]) # Agrega el par al diccionario
    p[0] = p[3]

def p_members_single(p):
    'members : pair'
    p[0] = p[1] # Retorna un diccionario con un solo par

def p_pair(p):
    'pair : STRING COLON value'
    # Quitamos las comillas de la clave (key) para usarla en python
    key = p[1].strip('"') 
    p[0] = { key: p[3] }

def p_value_string(p):
    'value : STRING'
    # Quitamos las comillas del valor
    p[0] = p[1].strip('"')

def p_value_number(p):
    'value : NUMBER'
    p[0] = p[1]

def p_value_object(p):
    'value : object'
    p[0] = p[1] # Permite anidamiento (ej. destinatario)

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis al final del archivo")

# Construir el parser
parser = yacc.yacc()

# --- LECTURA Y GENERACIÓN DE SALIDA ---

def procesar_datos():
    try:
        # 1. Leer archivo de entrada
        with open('datos.json', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # 2. Parsear (Analizar)
        print("Leyendo archivo datos.json y analizando...")
        resultado = parser.parse(contenido)
        
        if resultado:
            print("Se analizo correctamente. Generando el txt...")
            
            # 3. Generar salida formato TOON
            # Formato: id_envio, servicio, costo, destinatario{nombre, ciudad}
            
            lines = []
            # Cabecera
            lines.append("id_envio, servicio, costo, destinatario{nombre, ciudad}")
            
            for item in resultado:
                
                # Extraer datos simples
                id_envio = str(item.get('id_envio', ''))
                servicio = str(item.get('servicio', ''))
                costo = str(item.get('costo', ''))

                # Procesar objeto anidado (destinatario)
                destinatario = item.get('destinatario', {})
                nombre = destinatario.get('nombre', '')
                ciudad = destinatario.get('ciudad', '')
                
                # Formatear estilo TOON compacto: {valor1, valor2}
                destinatario_str = "{" + f"{nombre}, {ciudad}" + "}"
                
                # Unir todo
                linea = f"{id_envio}, {servicio}, {costo}, {destinatario_str}"
                lines.append(linea)

            # 4. Guardar archivo txt
            with open('salida.txt', 'w', encoding='utf-8') as f_out:
                f_out.write('\n'.join(lines))
                
            print("Archivo salida.txt creado correctamente.")
            
    except FileNotFoundError:
        print("Error: No se encuentra el archivo datos.json")
    except Exception as e:
        print(f"Ocurrio un error: {e}")

if __name__ == '__main__':
    procesar_datos()