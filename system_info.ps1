# Créer le dossier output s'il n'existe pas
$outputDir = "output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir
}

# Fonction pour écrire dans un fichier
function Write-ToFile {
    param(
        [string]$filename,
        [string]$content
    )
    $fullPath = Join-Path $outputDir $filename
    $content | Out-File -FilePath $fullPath -Encoding UTF8
}

# Récupérer les informations système
$computerSystem = Get-CimInstance CIM_ComputerSystem
$operatingSystem = Get-CimInstance CIM_OperatingSystem
$processor = Get-CimInstance CIM_Processor
$physicalMemory = Get-CimInstance CIM_PhysicalMemory
$videoController = Get-CimInstance Win32_VideoController
$diskDrive = Get-CimInstance Win32_DiskDrive

# Créer le rapport principal
$report = @"
=== Informations Système ===
Nom de l'ordinateur: $($computerSystem.Name)
Fabricant: $($computerSystem.Manufacturer)
Modèle: $($computerSystem.Model)

=== Système d'exploitation ===
OS: $($operatingSystem.Caption)
Version: $($operatingSystem.Version)
Architecture: $($operatingSystem.OSArchitecture)

=== Processeur ===
CPU: $($processor.Name)
Nombre de coeurs: $($processor.NumberOfCores)
Threads logiques: $($processor.NumberOfLogicalProcessors)

=== Mémoire RAM ===
RAM Totale: $([math]::Round($computerSystem.TotalPhysicalMemory/1GB, 2)) GB

=== Carte Graphique ===
$($videoController.Name)
RAM Video: $([math]::Round($videoController.AdapterRAM/1GB, 2)) GB

=== Disques ===
"@

foreach ($disk in $diskDrive) {
    $report += @"

Disque: $($disk.Model)
Capacité: $([math]::Round($disk.Size/1GB, 2)) GB
"@
}

# Écrire les rapports dans des fichiers séparés
Write-ToFile -filename "system_info_detailed.txt" -content $report
Write-ToFile -filename "cpu_info_detailed.txt" -content (Get-CimInstance Win32_Processor | Format-List *)
Write-ToFile -filename "memory_info_detailed.txt" -content (Get-CimInstance Win32_PhysicalMemory | Format-List *)
Write-ToFile -filename "disk_info_detailed.txt" -content (Get-CimInstance Win32_DiskDrive | Format-List *)

# Afficher le rapport dans la console
Write-Host $report