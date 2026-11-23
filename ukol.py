import socket, time, sys

HOST, PORT = "167.114.184.11", 9100
NAME = sys.argv[1] if len(sys.argv) > 1 else "oskar"

def attempt(offset):
    with socket.create_connection((HOST, PORT), timeout=5) as s:
        s.settimeout(5)
        s.recv(1024)
        time.sleep(1 - (time.time() % 1) + 0.05)
        T = int(time.time()) + offset
        code = (T * 7919) % 100000
        s.sendall(f"{code}:{NAME}\n".encode())
        return code, s.recv(1024).decode(errors="replace").strip()

offsets = [0] + [d*s for d in range(1, 31) for s in (1, -1)]
for off in offsets:
    try:
        code, resp = attempt(off)
        print(f"offset={off:+d} code={code:05d} -> {resp}")
        if "ERR" not in resp:
            print(f"\n=> JOINED ✅  server clock is {off:+d}s off yours")
            sys.exit(0)
    except Exception as e:
        print(f"offset={off:+d} err: {e}")
print("\nNo offset in ±30s worked — paste output, we'll go wider / diagnose.")
