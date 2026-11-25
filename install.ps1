# Installe les skills et l'agent dans le dossier Claude de l'utilisateur courant.
# Usage : .\install.ps1   (depuis le dossier du dépôt)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$claudeDir = Join-Path $env:USERPROFILE ".claude"
$skillsDst = Join-Path $claudeDir "skills"
$agentsDst = Join-Path $claudeDir "agents"
$dataDir = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "candidature"

New-Item -ItemType Directory -Force $skillsDst | Out-Null
New-Item -ItemType Directory -Force $agentsDst | Out-Null

Get-ChildItem (Join-Path $repo "skills") -Directory | ForEach-Object {
    $dst = Join-Path $skillsDst $_.Name
    if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
    Copy-Item -Recurse $_.FullName $dst
    Write-Host "skill installé : $($_.Name)"
}

Copy-Item (Join-Path $repo "agents\job-hunt-batch.md") (Join-Path $agentsDst "job-hunt-batch.md") -Force
Write-Host "agent installé : job-hunt-batch"

foreach ($sub in @("", "offres", "cv")) {
    New-Item -ItemType Directory -Force (Join-Path $dataDir $sub) | Out-Null
}
$profil = Join-Path $dataDir "profil-maitre.md"
if (-not (Test-Path $profil)) {
    Copy-Item (Join-Path $repo "templates\profil-maitre.template.md") $profil
    Write-Host "modèle de profil créé : $profil  <- à remplir avant la première utilisation"
} else {
    Write-Host "profil existant conservé : $profil"
}

$py = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $py) {
    Write-Warning "Python introuvable : le rendu du CV (ats-cv-tailor) a besoin de Python 3.10+ avec reportlab et pypdf."
} else {
    & python -c "import reportlab, pypdf" 2>$null
    if ($LASTEXITCODE -ne 0) { Write-Warning "Installez les dépendances du rendu CV : pip install reportlab pypdf" }
}

Write-Host ""
Write-Host "Terminé. Les skills apparaissent à la prochaine session Claude Code. Tapez /job-hunt pour commencer."
