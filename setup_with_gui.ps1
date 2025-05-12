Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Créer la fenêtre principale
$form = New-Object System.Windows.Forms.Form
$form.Text = "Installation des bibliothèques Python"
$form.Size = New-Object System.Drawing.Size(400, 200)
$form.StartPosition = "CenterScreen"

# Créer une étiquette pour afficher les messages
$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10, 20)
$label.Size = New-Object System.Drawing.Size(360, 20)
$form.Controls.Add($label)

# Créer une barre de progression
$progressBar = New-Object System.Windows.Forms.ProgressBar
$progressBar.Location = New-Object System.Drawing.Point(10, 50)
$progressBar.Size = New-Object System.Drawing.Size(360, 20)
$progressBar.Style = "Marquee"
$form.Controls.Add($progressBar)

# Afficher la fenêtre
$form.Show()

# Fonction pour mettre à jour l'étiquette
function Update-Label {
    param (
        [string]$message
    )
    $label.Text = $message
    $form.Refresh()
}

# Installer les dépendances Python
Update-Label -message "Vérification des bibliothèques Python..."
$requirementsPath = Join-Path -Path (Get-Location) -ChildPath "requirements.txt"

# Vérifier si les bibliothèques sont déjà installées
$needsInstall = $false
foreach($line in Get-Content $requirementsPath) {
    if($line.Trim()) {
        $package = $line.Split('==')[0]
        $installed = pip list | Select-String -Pattern "^$package\s"
        if(-not $installed) {
            $needsInstall = $true
            break
        }
    }
}

if($needsInstall) {
    Update-Label -message "Installation des bibliothèques manquantes..."
    pip install -r $requirementsPath
    Update-Label -message "Bibliothèques Python installées avec succès."
} else {
    Update-Label -message "Toutes les bibliothèques sont déjà installées."
}

# Fermer la fenêtre après un délai
Start-Sleep -Seconds 3
$form.Close()