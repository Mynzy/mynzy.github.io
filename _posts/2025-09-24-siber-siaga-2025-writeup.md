---
title: "Siber Siaga 2025 CTF Writeup"
date: 2025-09-24 12:00:00 +0800
categories: [CTF, Writeups, Online]
tags: [cybersecurity, ctf, siber-siaga, reverse-engineering, web-exploitation, pwn]
author: Mynz
---

# Siber Siaga 2025 CTF Writeup (Online)

My team, pulupuluultraman has managed to get 9th place and represent IIUM in Code Combat 2025 😆. This is my 1st CTF writeup and this writeup covers my solutions for 5 challenges from the Siber Siaga 2025 CTF competition.

## Challenge 1: Spelling Bee

**Challenge Creator:** @penguincat  
**Connection:** `nc 5.223.49.127 57004`

### Description
Just spell the flag correctly then I will give it to you.

### Solution
Given the connection credentials, each attempt allows only 5 tries, but the 5th attempt never shows results, so effectively only 4 attempts are available.

![Spelling Bee Challenge](/assets/img/posts/SiberSiaga/SpellingBee.png )

Here is the result of my try and i combine it to get the flag

```
______5_____7___5____3______3________3_____7__
____R_______7___________4__________________7__
S_B__2_______1___________________1____________
_________0______________________________0___0_
___________________________b______tt_____t____
__________m___m__________n____________________
__________________l_____________l___l__p______
___________e___e_______c______________________
____________________f_____________tt_____t____
______________________________a___________a___
_I_E___{_____________________________________}
S_______s__________i__________________________
```

**Flag:** `SIBER25{s0me71me5_lif3_c4n_b3_a_l1ttl3_p0ta70}`

---

## Challenge 2: Entry to Meta City

**Challenge Creator:** @penguincat  
**URL:** `http://5.223.49.127:47001/`  
**Flag Format:** SIBER25{flag}

### Description
To gain entry to the prestige city, you will first need to prove your worth unless you are an admin.

### Solution
This challenge was quite straightforward. Just enter admin and you will get the flag

![Entry to Meta City Interface](/assets/img/posts/SiberSiaga/EntryToMetaCity.png)
_The login interface for Meta City_


![Flag Retrieved](/assets/img/posts/SiberSiaga/EntryToMetaCity2.png)
_Successfully retrieved flag after entering "admin" in the login page_

**Flag:** `SIBER25{w3lc0m3_70_7h3_c00l357_c17y}`

---

## Challenge 3: A Byte Tales

**Challenge Creator:** @penguincat  
**Connection:** `nc 5.223.49.127 57001`  
**Flag Format:** SIBER25{flag}

### Description
Choose your path and decide your own fate.

### Solution
Based on the source code given, you can see `flag.txt` which means the server will also have a file named `flag.txt` in it, now we just need to find ways to exploit it.

![A Byte Tales Source Code](/assets/img/posts/SiberSiaga/AByteTalesSourceCode.png)
![A Byte Tales Source Code](/assets/img/posts/SiberSiaga/AByteTalesSourceCode2.png)

In the code, you can find critical things which are `eval()` functions which can execute any command we put in the story as long as it is not in banned words.

For this im trying different combinations to get the flag

- `[open('flag.txt').read()]`
- `f"{open('flag.txt').read()}"`
- `repr(open('flag.txt').read())`

The successful payload that bypassed the filter was:
```python
__builtins__.__dict__['pr'+'int'](open('flag.txt').read())
```

![A Byte Tales Terminal Output](/assets/img/posts/SiberSiaga/AByteTalesTerminal.png)

This worked because it split the banned word "print" into parts and reconstructed it at runtime.

**Flag:** `SIBER25{St1ck_70_7h3_5toryl1n3!}`

---

## Challenge 4: Guess PWD

**Challenge Creator:** @y_1_16  
**Flag Format:** SIBER25{flag}

### Description
Only 4 digits, guess it!

### Solution
I guess I'm pushing my luck again today.
Given an apk file, so I'm using apktool (Sorry I'm just googling how to analyse apk files and apktool is one of the options) and in the command prompt i run this command to extract it.

```bash
apktool d app-debug.apk
```

After that, im opening vscode and just find SIBER25{

![Flag Search in VS Code](/assets/img/posts/SiberSiaga/GuessPWD.png)

Sorry for unintended solution 🙏

**Flag:** `SIBER25{y0u_cr4ck_l061n_w17h_wh47_w4y?}`

---

## Challenge 5: Deep on Adversarial

**Challenge Creator:** @penguincat  
**Flag Format:** SIBER25{flag}

### Description
Recently, our AI Tech Support behaved strangely. During investigation, we discovered two odd files on the culprit device are identical to a suspicious file from our server. We suspect something malicious is hidden inside the image itself, but we couldn't see it directly. Can you figure out how to uncover what's within the image that can only be seen by AI?

### Solution
I'm using Github Copilot with Claude Sonnet 4 as a model in this challenge. After a series of interrogation, im able to get the flag.

So, here's the [code](/assets/code/challenge5_solution.py) for solving the challenge. Below is one of the results from executing the program.

![Adversarial Image](/assets/img/posts/SiberSiaga/DeepOnAdversarial.png "ICECTF{t00_ear1y_f0r_4_ctf}")

**Flag:** `SIBER25{l3arn1ng_m4ch1n3_l3arn1ng}`