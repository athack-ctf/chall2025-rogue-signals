# How to Solve the Challenge?

Step 1: Extracting the exfiltrated data (Zip Archive) 

The data is being exfiltrated via common technique called DNS TUNNELING. You google about it to know more.

After analysing the network capture with wireshark (or any other helpful tool), we conculde that there is a suspicious DNS trrafic between the IP adresses : 172.21.27.190 ==> ip.dst==171.112.111.35 invloving the domain name athackctf.com
It is important to distinguish the victim IP adress and the attacker IP adress, because if we filter out by Protocol only (DNS), we will get duplicate packets (Check how DNS works).  

Full command:
`tshark -r Rogue_Signals.pcapng -Y "dns && ip.src==172.21.27.190 && ip.dst==171.112.111.35" -T fields -e dns.qry.name | cut -c -8 | sed '$s/\.a$//' | tr -d "\n" | xxd -r -p > output.zip`

Step-by-Step Breakdown:
`tshark -r Rogue_Signals.pcapng -Y "dns && ip.src==172.21.27.190 && ip.dst==171.112.111.35" -T fields -e dns.qry.name`

Reads the packet capture file Rogue_Signals.pcapng.
Filters for DNS packets where:
Source IP is 172.21.27.190.
Destination IP is 171.112.111.35.
Extracts the dns.qry.name field (domain names from DNS queries).
Outputs the domain names.

| cut -c -8

Truncates the output to the first 8 characters of each domain name.

| sed '$s/\.a$//'

Removes the .a suffix from the last line (if present).

| tr -d "\n"

Removes all newline characters, creating a single continuous string.

| xxd -r -p > output.zip

Converts the processed string from hex (plaintext hex) to binary data.
Saves the binary data as `output.zip`

after unzipping the archive, we get two files `important.txt` and `secret_protected.pdf` 
trying to open the pdf file but it is a password protected. Moving to the txt file, it says:
"""Hello Defender!

If you arrived here, you are already a 1337.


Have you ever seen a password protected PDF file !


What's your next move ?


The flag is waiting for YOUUUUUUUUU !!!""" 



