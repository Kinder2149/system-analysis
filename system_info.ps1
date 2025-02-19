# Créez un nouveau fichier system_info.ps1 avec ce contenu
$computerSystem = Get-CimInstance CIM_ComputerSystem
$operatingSystem = Get-CimInstance CIM_OperatingSystem
$processor = Get-CimInstance CIM_Processor
$physicalMemory = Get-CimInstance CIM_PhysicalMemory
$videoController = Get-CimInstance Win32_VideoController
$diskDrive = Get-CimInstance Win32_DiskDrive

Write-Host "=== Informations Système ==="
Write-Host "Nom de l'ordinateur: $($computerSystem.Name)"
Write-Host "Fabricant: $($computerSystem.Manufacturer)"
Write-Host "Modèle: $($computerSystem.Model)"

Write-Host "`n=== Système d'exploitation ==="
Write-Host "OS: $($operatingSystem.Caption)"
Write-Host "Version: $($operatingSystem.Version)"
Write-Host "Architecture: $($operatingSystem.OSArchitecture)"

Write-Host "`n=== Processeur ==="
Write-Host "CPU: $($processor.Name)"
Write-Host "Nombre de coeurs: $($processor.NumberOfCores)"
Write-Host "Threads logiques: $($processor.NumberOfLogicalProcessors)"

Write-Host "`n=== Mémoire RAM ==="
$totalRAM = 0
foreach ($memory in $physicalMemory) {
    $totalRAM += $memory.Capacity
}
Write-Host "RAM Totale: $([math]::Round($totalRAM/1GB, 2)) GB"

Write-Host "`n=== Carte Graphique ==="
foreach ($graphics in $videoController) {
    Write-Host "Nom: $($graphics.Name)"
    Write-Host "RAM Video: $([math]::Round($graphics.AdapterRAM/1GB, 2)) GB"
}

Write-Host "`n=== Disques ==="
foreach ($disk in $diskDrive) {
    Write-Host "Disque: $($disk.Model)"
    Write-Host "Capacite: $([math]::Round($disk.Size/1GB, 2)) GB"
}