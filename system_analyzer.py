import os
import sys
import psutil
import platform
import datetime
import GPUtil
from pathlib import Path

# Créer le dossier output s'il n'existe pas
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

def write_to_file(filename, content):
    """Écrire le contenu dans un fichier dans le dossier output"""
    with open(output_dir / filename, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # En-tête avec la date et l'heure
    output = f"Analyse système - {datetime.datetime.now()}\n\n"

    # Information système
    output += "="*40 + " Informations Système " + "="*40 + "\n"
    output += f"Système: {platform.system()}\n"
    output += f"Nom du PC: {platform.node()}\n"
    output += f"Release: {platform.release()}\n"
    output += f"Version: {platform.version()}\n"
    output += f"Machine: {platform.machine()}\n"
    output += f"Processeur: {platform.processor()}\n"

    # Information CPU
    output += "="*40 + " Informations CPU " + "="*40 + "\n"
    output += f"Cœurs physiques: {psutil.cpu_count(logical=False)}\n"
    output += f"Total des threads: {psutil.cpu_count(logical=True)}\n"

    # Fréquences CPU
    cpu_freq = psutil.cpu_freq()
    output += "\nFréquences CPU:\n"
    output += f"Max: {cpu_freq.max:.2f}Mhz\n"
    output += f"Min: {cpu_freq.min:.2f}Mhz\n"
    output += f"Actuelle: {cpu_freq.current:.2f}Mhz\n"

    # Utilisation CPU par cœur
    output += "\nUtilisation CPU par cœur:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        output += f"Core {i}: {percentage}%\n"

    # Information mémoire
    output += "="*40 + " Informations Mémoire " + "="*40 + "\n"
    memory = psutil.virtual_memory()
    output += f"Total: {memory.total/1024/1024/1024:.2f}GB\n"
    output += f"Disponible: {memory.available/1024/1024:.2f}MB\n"
    output += f"Utilisé: {memory.used/1024/1024/1024:.2f}GB\n"
    output += f"Pourcentage: {memory.percent}%\n"

    # Information disque
    output += "="*40 + " Informations Disque " + "="*40 + "\n"
    partitions = psutil.disk_partitions()
    for partition in partitions:
        output += f"\nDisque: {partition.device}\n"
        output += f"  Point de montage: {partition.mountpoint}\n"
        output += f"  Système de fichiers: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            output += f"  Total: {partition_usage.total/1024/1024/1024:.2f}GB\n"
            output += f"  Utilisé: {partition_usage.used/1024/1024/1024:.2f}GB\n"
            output += f"  Libre: {partition_usage.free/1024/1024/1024:.2f}GB\n"
            output += f"  Pourcentage: {partition_usage.percent}%\n"
        except Exception as e:
            output += f"  Erreur: {str(e)}\n"

    # Information GPU
    output += "="*40 + " Informations GPU " + "="*40 + "\n"
    try:
        gpus = GPUtil.getGPUs()
        for i, gpu in enumerate(gpus):
            output += f"GPU ID: {i}\n"
            output += f"Nom GPU: {gpu.name}\n"
            output += f"Charge GPU: {gpu.load*100}%\n"
            output += f"Mémoire GPU libre: {gpu.memoryFree}MB\n"
            output += f"Mémoire GPU utilisée: {gpu.memoryUsed}MB\n"
            output += f"Mémoire GPU totale: {gpu.memoryTotal}MB\n"
            output += f"Température: {gpu.temperature} °C\n"
    except Exception as e:
        output += f"Erreur lors de la récupération des informations GPU: {str(e)}\n"

    # Information réseau
    output += "="*40 + " Informations Réseau " + "="*40 + "\n"
    interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in interfaces.items():
        output += f"\nInterface: {interface_name}\n"
        for addr in interface_addresses:
            output += f"  Adresse: {addr.address}\n"

    # Écrire les résultats dans le fichier de sortie
    write_to_file("system_analysis.txt", output)
    
    # Écrire d'autres fichiers spécifiques
    write_to_file("cpu_info.txt", f"CPU cores: {psutil.cpu_count()}\nCPU usage: {psutil.cpu_percent()}%")
    write_to_file("memory_info.txt", f"Memory total: {memory.total/1024/1024/1024:.2f}GB\nMemory used: {memory.used/1024/1024/1024:.2f}GB")
    
    print(output)  # Afficher également dans la console

if __name__ == "__main__":
    main()