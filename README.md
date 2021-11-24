### Creating a pyinstaller spec file for a new platform
From the desire platform, run:  
`pyinstaller --onefile --windowed -n FlexLMConverter --specpath spec/<platform> src/license_converter/main.py
`