# Install gsuper skills (and optionally rules) for Cursor CLI / servers / other agents.
param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("cursor-plugin", "cursor-skills", "project", "project-rules", "flat-skills")]
  [string]$Target,

  [Parameter(Mandatory = $true)]
  [string]$Dest
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

function Copy-SkillsInto([string]$Out) {
  New-Item -ItemType Directory -Force -Path $Out | Out-Null
  Get-ChildItem -Directory (Join-Path $Root "skills") | ForEach-Object {
    $skillMd = Join-Path $_.FullName "SKILL.md"
    if (-not (Test-Path $skillMd)) { return }
    $destSkill = Join-Path $Out $_.Name
    if (Test-Path $destSkill) { Remove-Item -Recurse -Force $destSkill }
    Copy-Item -Recurse -Force $_.FullName $destSkill
    Write-Host "skill → $destSkill"
  }
}

switch ($Target) {
  "cursor-plugin" {
    $parent = Split-Path -Parent $Dest
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
    Copy-Item -Recurse -Force $Root $Dest
    Write-Host "plugin → $Dest"
  }
  { $_ -in @("cursor-skills", "flat-skills") } {
    Copy-SkillsInto $Dest
  }
  "project" {
    Copy-SkillsInto (Join-Path $Dest ".cursor\skills")
  }
  "project-rules" {
    $rulesOut = Join-Path $Dest ".cursor\rules"
    New-Item -ItemType Directory -Force -Path $rulesOut | Out-Null
    Copy-Item -Force (Join-Path $Root "rules\*.mdc") $rulesOut
    Write-Host "rules → $rulesOut"
  }
}

Write-Host "Done. Reload Cursor window / restart cursor-agent as needed."
