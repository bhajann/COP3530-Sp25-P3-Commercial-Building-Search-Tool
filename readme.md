# COP3530 P3 Spring 2025 - Commercial Building Search Tool
## Team Name: A+ Tree
Members:
- Minji Lee
- Nickalou Bhajan
- Ricardo Santos

## Dataset source:
Link: https://catalog.data.gov/dataset/city-and-county-commercial-building-inventories-010d2
https://web.archive.org/web/20240507063457/https://data.openei.org/submissions/906
### Columns in Dataset:
- City
- County
- State
- Building Count
- Reported Property Type
- Reported Property Subtype
- Building Area (mean)
- Year Built (mean)
- Number of Stories

## Installation:
Most Python installations come with the GUI library Tkinter (e.g. Windows), but if they do not, here is how you install that on a few different operating systems:

### Ubuntu:
```sh
sudo apt install python3-tk
```

### Mac:
```sh
brew install python-tk
```

### Verify installation:
```python
python3 -m tkinter # This brings up a test Tkinter window
```

## Opening the program:
```sh
python3 UI.py
```