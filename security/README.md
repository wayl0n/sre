# This is a Python script I wrote for the TryHackMe (https://tryhackme.com/) CTF called "Hammer"

![Alt text](hammer.png?raw=true "hammer ctf room")

* NB: This README contains spoliers so please don't read any further if you want to do this room yourself.

The script was created in order to capture the first flag for User on the box.

(This was done after basic enumeration of the host: reading the HTML source lead to a comment by a Dev that revealed a clue as to where the logfiles for the application might be stored.  Fuzzing for the directory eventually got a hit and from there, reading through the logs led to a username for the password reset to be used on)

I first thought the way to evade the brute force protection for password recovery was to rotate User Agents but what was needed was to spoof the IPs in the X-Forwarded-For Headers.

Ultimately, a single threaded application was not fast enough before the timer for the PIN recovery code expired.  Creating a script that created 20 separate worker threads proved to be fast enough to beat the clock.
