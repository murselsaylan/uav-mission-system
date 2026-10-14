# UAV Mission System

Software for an autonomous fixed-wing UAV competition (fighter-UAV style: find, follow and lock on to other UAVs while
staying inside the arena and avoiding air-defence zones). It is split into the parts I worked on:

| Folder | What it does |
|---|---|
| [mission-planner](mission-planner/) | Latest version (v3.2). Reads the telemetry of all UAVs, checks threats (altitude limits, arena polygon, being followed, air-defence circles), picks the target and writes the next waypoint. Includes a PyQt5 GUI and a local mission simulator. |
| [ground-control-station](ground-control-station/) | PyQt5 ground-control GUI (v3.1): arena map, UAV positions, threat zones, flight-mode switching, camera feed (OpenCV) and manual/automatic waypoint sending. |
| [target-tracking](target-tracking/) | Target selection and pursuit logic: distance / speed / heading to every rival, safe-zone and escape checks, route generation, scoring. `bölünmüş kodlar/` holds the same logic split into modules (route, escape, waypoint, threats, QR mission). |
| [simulation](simulation/) | 2D Pygame simulator of the arena: several UAVs, air-defence sites, target lock sounds; writes the same JSON telemetry the planner reads, so the planner can be tested without hardware. |
| [heatmap](heatmap/) | Builds heat maps of where targets appear in a labelled image dataset (YOLO-format labels) to study detection coverage. |

## How it fits together

```
simulation (or real telemetry) --> ihas.json --> mission-planner / target-tracking --> next waypoint (son_waypoint.json)
                                                        |
                                           ground-control-station (GUI, flight mode, manual override)
```

The parts exchange data through small JSON files (`ihas.json`, `oyun_alani.json`, `ucus_modu.json`, `son_waypoint.json`),
which keeps every part testable on its own.

## Run

```bash
pip install pyqt5 opencv-python numpy matplotlib pygame
cd simulation/sim && python simv4.py          # start the simulator
cd mission-planner && python main.py          # planner + GUI
```

Note: the simulator uses `pywin32` (`win32api`) for window handling and runs on Windows.

## Türkçe özet

İHA yarışması için yazdığım yazılımlar: görev planlayıcı (tehdit kontrolü, hedef seçimi, waypoint üretimi),
PyQt5 yer kontrol istasyonu arayüzü, hedef takip algoritmaları, Pygame ile 2B simülasyon ve etiketli görüntü verisinden
ısı haritası çıkaran araç. Parçalar JSON dosyaları üzerinden haberleşir. Kişisel görüntü verileri ve eski yedek kopyalar
bu klasöre alınmadı.
