import boto3
import sys
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError

REGION = "us-east-1"
ec2 = boto3.client("ec2", region_name=REGION)

def listar_instancias():
    try:
        response = ec2.describe_instances()
        print("\nInstancias encontradas:\n")

        hay_instancias = False
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                hay_instancias = True
                instance_id = instance.get("InstanceId", "N/A")
                estado = instance.get("State", {}).get("Name", "N/A")
                print(f"ID: {instance_id} | Estado: {estado}")

        if not hay_instancias:
            print("No se encontraron instancias en esta región.")

    except NoCredentialsError:
        print("Error: no se encontraron credenciales válidas.")
    except EndpointConnectionError:
        print("Error: no se pudo conectar al endpoint AWS.")
    except ClientError as e:
        print(f"Error de AWS al listar instancias: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def obtener_estado_instancia(instancia_id):
    try:
        response = ec2.describe_instances(InstanceIds=[instancia_id])
        reservations = response.get("Reservations", [])
        if not reservations or not reservations[0].get("Instances"):
            return None
        return reservations[0]["Instances"][0]["State"]["Name"]
    except ClientError as e:
        print(f"Error al obtener estado de la instancia {instancia_id}: {e}")
        return None

def iniciar_instancia(instancia_id):
    estado = obtener_estado_instancia(instancia_id)

    if estado is None:
        print("No se pudo obtener el estado de la instancia.")
        return

    if estado == "stopped":
        try:
            ec2.start_instances(InstanceIds=[instancia_id])
            print(f"Instancia {instancia_id} iniciada correctamente.")
        except ClientError as e:
            print(f"Error al iniciar la instancia: {e}")
    elif estado == "running":
        print(f"La instancia {instancia_id} ya está en ejecución.")
    else:
        print(f"La instancia {instancia_id} está en estado '{estado}', no se puede iniciar ahora.")

def detener_instancia(instancia_id):
    estado = obtener_estado_instancia(instancia_id)

    if estado is None:
        print("No se pudo obtener el estado de la instancia.")
        return

    if estado == "running":
        try:
            ec2.stop_instances(InstanceIds=[instancia_id])
            print(f"Instancia {instancia_id} detenida correctamente.")
        except ClientError as e:
            print(f"Error al detener la instancia: {e}")
    elif estado == "stopped":
        print(f"La instancia {instancia_id} ya está detenida.")
    else:
        print(f"La instancia {instancia_id} está en estado '{estado}', no se puede detener ahora.")

if __name__ == "__main__":
    print("=== Gestión de EC2 con Boto3 ===")
    listar_instancias()

    if len(sys.argv) == 3:
        accion = sys.argv[1].lower()
        instancia_id = sys.argv[2]

        if accion == "iniciar":
            iniciar_instancia(instancia_id)
        elif accion == "detener":
            detener_instancia(instancia_id)
        else:
            print("Acción no válida. Usa: iniciar o detener")
    else:
        print("\nUso opcional:")
        print("python3 gestionar_ec2.py iniciar i-xxxxxxxxxxxx")
        print("python3 gestionar_ec2.py detener i-xxxxxxxxxxxx")