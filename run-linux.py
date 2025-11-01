import subprocess
import sys
import os
from pathlib import Path

BOTS = {
    "charon": "Charon-The-Ferryman/charonTheFerryman.py",
    "argus": "Argus-The-All-Seeing/argusTheAllSeeing.py",
    "themis": "Themis-The-Just/themisTheJust.py",
    "hermes": "Hermes-The-Messenger/hermesTheMessenger.py",
}

def run_bot(name: str):
    if name not in BOTS:
        print(f"❌ Unknown bot: {name}")
        print(f"Available bots: {', '.join(BOTS.keys())}")
        sys.exit(1)

    path = Path(BOTS[name])
    if not path.exists():
        print(f"⚠️ Bot file not found: {path}")
        sys.exit(1)

    print(f"⚡ Summoning {name.title()}...")
    subprocess.run(["python3", str(path)])

def run_all():
    print("⚡ Summoning the full Council of Olympus...")
    processes = []
    for name, path in BOTS.items():
        print(f"  ➤ Starting {name.title()}...")
        proc = subprocess.Popen(["python3", path])
        processes.append(proc)

    print("🕊️  All bots are running. Press Ctrl+C to dismiss the gods.")
    try:
        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        print("\n⚔️  Shutting down Olympus...")
        for proc in processes:
            proc.terminate()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 run.py <botname>   — run a single bot")
        print("  python3 run.py all         — run all bots")
        sys.exit(0)

    target = sys.argv[1].lower()
    if target == "all":
        run_all()
    else:
        run_bot(target)
