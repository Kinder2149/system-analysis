import platform
import psutil
import GPUtil
import os
import datetime

def get_size(bytes):
    """
    Convertit les bytes en format lisible
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def system_info():
    print("="*40, "Informations Système", "="*40)
    uname = platform.uname()
    print(f"Système: {uname.system}")
    print(f"Nom du PC: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processeur: {uname.processor}")

def cpu_info():
    print("="*40, "Informations CPU", "="*40)
    print("Cœurs physiques:", psutil.cpu_count(logical=False))
    print("Total des threads:", psutil.cpu_count(logical=True))
    print("\nFréquences CPU:")
    cpu_freq = psutil.cpu_freq()
    print(f"Max: {cpu_freq.max:.2f}Mhz")
    print(f"Min: {cpu_freq.min:.2f}Mhz")
    print(f"Actuelle: {cpu_freq.current:.2f}Mhz")
    
    print("\nUtilisation CPU par cœur:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")

def memory_info():
    print("="*40, "Informations Mémoire", "="*40)
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Disponible: {get_size(svmem.available)}")
    print(f"Utilisé: {get_size(svmem.used)}")
    print(f"Pourcentage: {svmem.percent}%")

def disk_info():
    print("="*40, "Informations Disque", "="*40)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"\nDisque: {partition.device}")
        print(f"  Point de montage: {partition.mountpoint}")
        print(f"  Système de fichiers: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Total: {get_size(partition_usage.total)}")
            print(f"  Utilisé: {get_size(partition_usage.used)}")
            print(f"  Libre: {get_size(partition_usage.free)}")
            print(f"  Pourcentage: {partition_usage.percent}%")
        except Exception as e:
            print(f"  Erreur: {e}")

def gpu_info():
    print("="*40, "Informations GPU", "="*40)
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            print(f"GPU ID: {gpu.id}")
            print(f"Nom GPU: {gpu.name}")
            print(f"Charge GPU: {gpu.load*100}%")
            print(f"Mémoire GPU libre: {gpu.memoryFree}MB")
            print(f"Mémoire GPU utilisée: {gpu.memoryUsed}MB")
            print(f"Mémoire GPU totale: {gpu.memoryTotal}MB")
            print(f"Température: {gpu.temperature} °C")
    except Exception as e:
        print(f"Impossible d'obtenir les informations GPU: {e}")

def network_info():
    print("="*40, "Informations Réseau", "="*40)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        print(f"\nInterface: {interface_name}")
        for addr in interface_addresses:
            print(f"  Adresse: {addr.address}")

def main():
    print(f"Analyse système - {datetime.datetime.now()}\n")
    system_info()
    cpu_info()
    memory_info()
    disk_info()
    gpu_info()
    network_info()

if __name__ == "__main__":
    main()