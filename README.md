# start up mail win
Send mail notification when computer is started up with photo taken from webcam

## Usage
1. Copy `internal_config_sample.py` as `internal_config.py` and edit the email connect info
2. Compile it with pyinstaller, use compile.bat
3. Set it as run when windows starts

PS:
`cam_cap.py` uses openCV2 to capture image
`cam_cap_pygame.py` use pygame to capture image, install
[Videocapture](http://videocapture.sourceforge.net/ "Videocapture") before running.