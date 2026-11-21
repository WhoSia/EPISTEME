#requires -Version 5.1
<#
EPISTEME P77 — bounded download of small, publicly released scientific evidence.
This script DOES NOT download whole S-BIAD602 images, alter Drive, or resolve
F05 historical runtime provenance. Default: only one known small F02 note.
Optional: two ~4 MB Zenodo versioned source archives. SHA256 receipt is local.
Review the allowlisted URLs before running.
#>
[CmdletBinding()]
param(
    [string]$Destination = (Join-Path $env:USERPROFILE 'Downloads\EPISTEME-P77-W57'),
    [ValidateRange(1,200)][int]$MaxFileMiB = 25,
    [switch]$IncludeZenodo
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$allowedHosts = @('ftp.ebi.ac.uk','zenodo.org')
$items = @(
    [pscustomobject]@{
        id = 'F02-public-note'
        name = 'Gehrels_S-BIAD602_wildtype_EmbryoInfo210122.rtf'
        uri = 'https://ftp.ebi.ac.uk/biostudies/fire/S-BIAD/602/S-BIAD602/Files/DataRepository/TwoPhoton/wildtype/EmbryoInfo210122.rtf'
        md5 = ''
        note = 'Known deposit note only; does NOT solve the two unknown t0 cases'
    }
)
if ($IncludeZenodo) {
    $items += [pscustomobject]@{
        id = 'A05-Zenodo-v1'
        name = 'Sundaram_2026_Zenodo_v1_Data.zip'
        uri = 'https://zenodo.org/api/records/15617183/files/Data.zip/content'
        md5 = '8ae6475067de8ae03ba4a9a0c1efd8c5'
        note = 'Original manuscript-cited dataset release'
    }
    $items += [pscustomobject]@{
        id = 'A06-Zenodo-v3'
        name = 'Sundaram_2026_Zenodo_v3_Data.zip'
        uri = 'https://zenodo.org/api/records/17555722/files/Data.zip/content'
        md5 = '9ebd58bd9770bdb75722d0e3fe6c06ef'
        note = 'Later release; v2 and v3 reported identical MD5'
    }
}

$receipts = @()
$maximumBytes = [long]$MaxFileMiB * 1048576L
foreach ($item in $items) {
    $target = Join-Path $Destination $item.name
    $partial = $target + '.part'
    try {
        $source = [Uri]$item.uri
        if ($source.Scheme -ne 'https' -or $allowedHosts -notcontains $source.Host) {
            throw ('Disallowed source host: ' + $source.Host)
        }
        if (Test-Path -LiteralPath $partial) { Remove-Item -LiteralPath $partial -Force }
        if (-not (Test-Path -LiteralPath $target)) {
            & curl.exe --fail --location --retry 3 --retry-delay 2 --connect-timeout 20 --max-filesize $maximumBytes --output $partial $item.uri
            if ($LASTEXITCODE -ne 0) { throw ('curl failed (exit ' + $LASTEXITCODE + ')') }
            if (-not (Test-Path -LiteralPath $partial)) { throw 'Downloaded file not found' }
            $actualSize = (Get-Item -LiteralPath $partial).Length
            if ($actualSize -gt $maximumBytes) { throw 'File larger than allowed budget' }
            if ($item.md5 -ne '') {
                $md5 = (Get-FileHash -LiteralPath $partial -Algorithm MD5).Hash.ToLowerInvariant()
                if ($md5 -ne $item.md5) { throw ('MD5 mismatch: ' + $md5) }
            }
            Move-Item -LiteralPath $partial -Destination $target
        }
        $size = (Get-Item -LiteralPath $target).Length
        if ($size -gt $maximumBytes) { throw 'Existing file larger than allowed budget' }
        $actualMd5 = (Get-FileHash -LiteralPath $target -Algorithm MD5).Hash.ToLowerInvariant()
        if ($item.md5 -ne '' -and $actualMd5 -ne $item.md5) { throw 'Existing file MD5 mismatch' }
        $receipts += [pscustomobject]@{
            id = $item.id; status = 'verified'; file = $target; bytes = $size
            md5 = $actualMd5
            sha256 = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
            source = $item.uri; note = $item.note
        }
        Write-Host ('VERIFIED ' + $item.id + ' (' + $size + ' bytes)')
    } catch {
        if (Test-Path -LiteralPath $partial) { Remove-Item -LiteralPath $partial -Force }
        $receipts += [pscustomobject]@{
            id = $item.id; status = 'failed'; file = $target
            source = $item.uri; error = $_.Exception.Message; note = $item.note
        }
        Write-Warning ('FAILED ' + $item.id + ': ' + $_.Exception.Message)
    }
}
$receiptPath = Join-Path $Destination 'acquisition_receipt.json'
$receipts | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
Write-Host ('Receipt: ' + $receiptPath)
if (@($receipts | Where-Object { $_.status -eq 'failed' }).Count -gt 0) { exit 2 }
