# 逐场抽帧检查
# 用法： .\check_frames.ps1 -Video deliverables\成片.mp4 -Out frames
param(
  [string]$Video = "silent.mp4",
  [string]$Out = "frames",
  [double]$Step = 6.5
)

New-Item -ItemType Directory -Force -Path $Out | Out-Null
$dur = [double](ffprobe -v error -show_entries format=duration -of csv=p=0 $Video)
$t = 1.0
$i = 0
while ($t -lt $dur - 0.3) {
  $i++
  $f = Join-Path $Out ("f{0:D2}_{1:N1}.jpg" -f $i, $t)
  ffmpeg -y -loglevel error -ss $t -i $Video -frames:v 1 -q:v 2 $f
  $t += $Step
}
Write-Output "duration=$dur frames=$i out=$Out"
