$ErrorActionPreference = 'SilentlyContinue'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$root = Join-Path $env:TEMP 'batch3'
Remove-Item $root -Recurse -Force; New-Item -ItemType Directory $root | Out-Null
$log = Join-Path $root 'log.txt'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
function Get-F($folder, $name, $url) {
  $d = Join-Path $root $folder; if (-not (Test-Path $d)) { New-Item -ItemType Directory $d | Out-Null }
  $f = Join-Path $d $name
  try {
    Invoke-WebRequest ([Uri]::EscapeUriString([Uri]::UnescapeDataString($url))) -OutFile $f -UseBasicParsing -TimeoutSec 90 -UserAgent $ua
    $h = [IO.File]::ReadAllBytes($f)[0..3]
    if ([Text.Encoding]::ASCII.GetString($h) -ne '%PDF' -and $name -like '*.pdf') { Add-Content $log "NOTPDF $folder/$name $url"; Remove-Item $f -Force; return $false }
    Add-Content $log "OK $folder/$name $url"; return $true
  } catch { Add-Content $log "FAIL $folder/$name $url"; Remove-Item $f -Force; return $false }
}
$list = @(
  @('usa-tstst','2025_main.pdf','https://github.com/usa-tst-public/USA-TST-Archive/raw/main/TSTST2025Problems.pdf'),
  @('usa-tstst','2025_master.pdf','https://github.com/usa-tst-public/USA-TST-Archive/raw/master/TSTST2025Problems.pdf'),
  @('usa-tstst','2026_main.pdf','https://github.com/usa-tst-public/USA-TST-Archive/raw/main/TSTST2026Problems.pdf'),
  @('usa-tstst','2026_master.pdf','https://github.com/usa-tst-public/USA-TST-Archive/raw/master/TSTST2026Problems.pdf'),
  @('korea-kmo','2025a.pdf','http://www.kms.or.kr/file/fileboard/3068357271_ff0f204c_2025kmo2-h.pdf'),
  @('korea-kmo','2025b.pdf','https://www.kms.or.kr/inc/attach_download.php?r_name=3068357271_ff0f204c_2025kmo2-h.pdf&f_name=2025kmo2-h.pdf'),
  @('hungary','2018.pdf','https://www.bolyai.hu/files/Kurschak_2018_feladatok.pdf'),
  @('hungary','2019.pdf','https://www.bolyai.hu/files/Kurschak_2019_feladatok.pdf'),
  @('hungary','2020.pdf','https://www.bolyai.hu/files/Kurschak_2020_Feladatok.pdf'),
  @('hungary','2021.pdf','https://www.bolyai.hu/files/Kurschak_feladatok_2021.pdf'),
  @('hungary','2022.pdf','https://www.bolyai.hu/files/Kurschak_2022_feladatok.pdf'),
  @('hungary','2023.pdf','https://www.bolyai.hu/files/Kurschak_2023_feladatlap.pdf'),
  @('hungary','2024.pdf','https://www.bolyai.hu/files/Kurschak_2024_megoldasok.pdf'),
  @('bulgaria','2017.pdf','https://www.matematika.bg/olimpiadi/olimpiadi/natsionalen-krag/2017-9-12.pdf'),
  @('bulgaria','2018.pdf','https://www.matematika.bg/olimpiadi/olimpiadi/natsionalen-krag/2018-9-12.pdf'),
  @('bulgaria','2019.pdf','https://www.matematika.bg/olimpiadi/olimpiadi/natsionalen-krag/2019-9-12.pdf'),
  @('bulgaria','2020_1.pdf','https://www.matematika.bg/olimpiadi/olimpiadi/natsionalen-krag/2020-9-12-1den.pdf'),
  @('bulgaria','2020_2.pdf','https://www.matematika.bg/olimpiadi/olimpiadi/natsionalen-krag/2020-9-12-2den.pdf'),
  @('bulgaria','2021_1.pdf','https://www.matematika.bg/olimpiadi/olimpiadi/natsionalen-krag/2021-9-12-1den.pdf'),
  @('bulgaria','2021_2.pdf','https://www.matematika.bg/olimpiadi/olimpiadi/natsionalen-krag/2021-9-12-2den.pdf'),
  @('australia','2016.pdf','https://amt.edu.au/wp-content/uploads/2019/02/2016-AMO-Paper-and-Solutions.pdf'),
  @('australia','2017.pdf','https://amt.edu.au/wp-content/uploads/2019/02/2017-AMO-Paper-and-Solutions.pdf'),
  @('australia','2018.pdf','https://amt.edu.au/wp-content/uploads/2019/02/AMO-2018-Problems-and-Solutions.pdf'),
  @('australia','2019.pdf','https://amt.edu.au/wp-content/uploads/2020/05/AMO-2019-paper-and-solutions.pdf'),
  @('australia','2020.pdf','https://amt.edu.au/wp-content/uploads/2020/05/AMO-2020-paper-and-solutions.pdf'),
  @('newzealand','2015_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2015'),
  @('newzealand','2015_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2015'),
  @('newzealand','2016_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2016'),
  @('newzealand','2016_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2016'),
  @('newzealand','2017_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2017'),
  @('newzealand','2017_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2017'),
  @('newzealand','2018_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2018'),
  @('newzealand','2018_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2018'),
  @('newzealand','2019_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2019'),
  @('newzealand','2019_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2019'),
  @('newzealand','2020_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2020'),
  @('newzealand','2020_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2020'),
  @('newzealand','2021_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2021'),
  @('newzealand','2021_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2021'),
  @('newzealand','2022_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2022'),
  @('newzealand','2022_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2022'),
  @('newzealand','2023_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2023'),
  @('newzealand','2023_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2023'),
  @('newzealand','2024_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2024'),
  @('newzealand','2024_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2024'),
  @('newzealand','2025_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2025'),
  @('newzealand','2025_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2025'),
  @('newzealand','2026_r1.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=1&year=2026'),
  @('newzealand','2026_r2.pdf','http://www.mathsolympiad.org.nz/competitions/nzmo/files/problems.php?round=2&year=2026'),
  @('kazakhstan','2018_math11_1_sol.pdf','https://daryn.kz/ro/2018/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2018_math11_2_sh.pdf','https://daryn.kz/ro/2018/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2018_math11_1_sh.pdf','https://daryn.kz/ro/2018/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2018_math11_2_sol.pdf','https://daryn.kz/ro/2018/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2018_math11.pdf','https://daryn.kz/ro/2018/tasks/math11.pdf'),
  @('kazakhstan','2019_math11_1_sol.pdf','https://daryn.kz/ro/2019/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2019_math11_2_sh.pdf','https://daryn.kz/ro/2019/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2019_math11_1_sh.pdf','https://daryn.kz/ro/2019/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2019_math11_2_sol.pdf','https://daryn.kz/ro/2019/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2019_math11.pdf','https://daryn.kz/ro/2019/tasks/math11.pdf'),
  @('kazakhstan','2020_math11_1_sol.pdf','https://daryn.kz/ro/2020/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2020_math11_2_sh.pdf','https://daryn.kz/ro/2020/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2020_math11_1_sh.pdf','https://daryn.kz/ro/2020/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2020_math11_2_sol.pdf','https://daryn.kz/ro/2020/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2020_math11.pdf','https://daryn.kz/ro/2020/tasks/math11.pdf'),
  @('kazakhstan','2021_math11_1_sol.pdf','https://daryn.kz/ro/2021/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2021_math11_2_sh.pdf','https://daryn.kz/ro/2021/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2021_math11_1_sh.pdf','https://daryn.kz/ro/2021/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2021_math11_2_sol.pdf','https://daryn.kz/ro/2021/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2021_math11.pdf','https://daryn.kz/ro/2021/tasks/math11.pdf'),
  @('kazakhstan','2022_math11_1_sol.pdf','https://daryn.kz/ro/2022/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2022_math11_2_sh.pdf','https://daryn.kz/ro/2022/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2022_math11_1_sh.pdf','https://daryn.kz/ro/2022/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2022_math11_2_sol.pdf','https://daryn.kz/ro/2022/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2022_math11.pdf','https://daryn.kz/ro/2022/tasks/math11.pdf'),
  @('kazakhstan','2023_math11_1_sol.pdf','https://daryn.kz/ro/2023/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2023_math11_2_sh.pdf','https://daryn.kz/ro/2023/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2023_math11_1_sh.pdf','https://daryn.kz/ro/2023/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2023_math11_2_sol.pdf','https://daryn.kz/ro/2023/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2023_math11.pdf','https://daryn.kz/ro/2023/tasks/math11.pdf'),
  @('kazakhstan','2024_math11_1_sol.pdf','https://daryn.kz/ro/2024/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2024_math11_2_sh.pdf','https://daryn.kz/ro/2024/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2024_math11_1_sh.pdf','https://daryn.kz/ro/2024/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2024_math11_2_sol.pdf','https://daryn.kz/ro/2024/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2024_math11.pdf','https://daryn.kz/ro/2024/tasks/math11.pdf'),
  @('kazakhstan','2025_math11_1_sol.pdf','https://daryn.kz/ro/2025/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2025_math11_2_sh.pdf','https://daryn.kz/ro/2025/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2025_math11_1_sh.pdf','https://daryn.kz/ro/2025/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2025_math11_2_sol.pdf','https://daryn.kz/ro/2025/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2025_math11.pdf','https://daryn.kz/ro/2025/tasks/math11.pdf'),
  @('kazakhstan','2026_math11_1_sol.pdf','https://daryn.kz/ro/2026/tasks/math11_1_sol.pdf'),
  @('kazakhstan','2026_math11_2_sh.pdf','https://daryn.kz/ro/2026/tasks/math11_2_sh.pdf'),
  @('kazakhstan','2026_math11_1_sh.pdf','https://daryn.kz/ro/2026/tasks/math11_1_sh.pdf'),
  @('kazakhstan','2026_math11_2_sol.pdf','https://daryn.kz/ro/2026/tasks/math11_2_sol.pdf'),
  @('kazakhstan','2026_math11.pdf','https://daryn.kz/ro/2026/tasks/math11.pdf'),
  @('ukraine','2024.pdf','https://api.man.gov.ua/api/assets/man/5374435a-c9c1-47c8-94da-a6df343bf70e'),
  @('ukraine','2025.pdf','https://api.man.gov.ua/api/assets/man/46438623-7f88-489a-a087-1be7622e1639'),
  @('macedonia','2020.pdf','https://smm.org.mk/wp-content/uploads/2020/08/reshenija_za_natprevarot.pdf'),
  @('macedonia','2021.pdf','https://smm.org.mk/wp-content/uploads/2021/05/MMO-reshenija.pdf'),
  @('macedonia','2022.pdf','https://smm.org.mk/wp-content/uploads/2022/04/reshenija_web.pdf'),
  @('macedonia','2023.pdf','https://smm.org.mk/wp-content/uploads/2023/04/resenija-1.pdf'),
  @('macedonia','2024.pdf','https://smm.org.mk/wp-content/uploads/2024/04/kombinacija-za-MMO-2024.pdf'),
  @('macedonia','2025.pdf','https://smm.org.mk/wp-content/uploads/2025/03/ММО-2025-решенија-и-распределба-на-поени.pdf'),
  @('macedonia','2026.pdf','https://smm.org.mk/wp-content/uploads/2026/04/решенија-и-распределба-на-поени.pdf')
)
$i = 0
foreach ($p in $list) { $i++; $r = Get-F $p[0] $p[1] $p[2]; Write-Host ("[{0}/{1}] {2} {3}/{4}" -f $i, $list.Count, ($(if ($r) {'ok'} else {'--'})), $p[0], $p[1]) }
$scrape = @(
  @('korea-kmo','https://www.kmo.or.kr/kmo/sub07.html','(?i)2025.*kmo2.*h'),
  @('hungary','https://www.bolyai.hu/versenyek-kurschak-jozsef-matematikai-tanuloverseny/','(?i)kurschak[^"]*\.pdf'),
  @('bulgaria','https://www.matematika.bg/olimpiadi/olimpiadi/12klas.html','(?i)natsionalen-krag[^"]*\.pdf'),
  @('macedonia','https://smm.org.mk/natprevari/natprevari-za-sredno-obrazovanie/','(?i)\.pdf'),
  @('australia','https://amt.edu.au/department/past-papers','(?i)AMO[^"]*\.pdf'),
  @('germany-mo','https://www.mathematik-olympiaden.de/moev/index.php/aufgaben/aufgabenarchiv','(?i)(\d{2}4[^"/]*1[23]|bundesrunde|4\.?\s*stufe)[^"]*\.pdf'),
  @('germany-mo','https://www.mathematik-olympiaden.de/moev/','(?i)(\d{2}4[^"/]*1[23]|bundesrunde)[^"]*\.pdf'),
  @('germany-mo','https://www.mathematik-olympiaden.de/','(?i)(\d{2}4[^"/]*1[23]|bundesrunde)[^"]*\.pdf')
)
foreach ($s in $scrape) {
  try { $page = Invoke-WebRequest $s[1] -UseBasicParsing -TimeoutSec 90 -UserAgent $ua } catch { Add-Content $log "PAGEFAIL $($s[1])"; Write-Host "-- page $($s[1])"; continue }
  $d = Join-Path $root $s[0]; New-Item -ItemType Directory $d -Force | Out-Null
  $pn = '_page_' + (($s[1] -replace '^https?://', '') -replace '[^A-Za-z0-9]', '_') + '.html'
  if ($pn.Length -gt 100) { $pn = $pn.Substring(0,100) + '.html' }
  [IO.File]::WriteAllText((Join-Path $d $pn), $page.Content)
  $base = [Uri]$s[1]
  $hrefs = [regex]::Matches($page.Content, 'href="([^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Where-Object { $_ -match $s[2] } | Select-Object -Unique
  foreach ($h in $hrefs) {
    $u = (New-Object Uri($base, [Net.WebUtility]::HtmlDecode($h).Replace('\','/'))).AbsoluteUri
    $name = ($u -replace '^https?://[^/]+/', '') -replace '[\\/:*?"<>|%&=]', '_'
    if ($name.Length -gt 120) { $name = $name.Substring($name.Length - 120) }
    if (Test-Path (Join-Path $d $name)) { continue }
    $r = Get-F $s[0] $name $u; Write-Host ("{0} {1}/{2}" -f ($(if ($r) {'ok'} else {'--'})), $s[0], $name)
  }
}
$zip = Join-Path "$HOME\Downloads" 'batch3.zip'
Remove-Item $zip -Force
Compress-Archive -Path (Join-Path $root '*') -DestinationPath $zip
$ok = (Select-String -Path $log -Pattern '^OK').Count
Write-Host "OK - $ok αρχεία στο $zip. Ανέβασέ το εδώ." -ForegroundColor Green
