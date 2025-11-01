import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

BOTS = {
    "charon": ROOT/"Charon-The-Ferryman"/"charonTheFerryman.py",
    "argus": ROOT/"Argus-The-All-Seeing"/"argusTheAllSeeing.py",
    "themis": ROOT/"Themis-The-Just"/"themisTheJust.py",
    "hermes": ROOT/"Hermes-The-Messenger"/"hermesTheMessenger.py",
}

def run_bot(name: str):
    if name not in BOTS:
        print(f"❌ Unknown bot: {name}")
        print(f"Available bots: {', '.join(BOTS.keys())}")
        sys.exit(1)

    path = BOTS[name]
    if not path.exists():
        print(f"⚠️ Bot file not found: {path}")
        sys.exit(1)

    print(f"⚡ Summoning {name.title()}...")
    subprocess.run([sys.executable, str(path)], check=True)

def run_all():
    print("⚡ Summoning the full Council of Olympus...")
    processes = []
    for name, path in BOTS.items():
        print(f"  ➤ Starting {name.title()}...")
        proc = subprocess.Popen([sys.executable, str(path)])
        processes.append(proc)

    print("🕊️  All bots are running. Press Ctrl+C to dismiss the gods.")
    try:
        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        print("\n⚔️  Shutting down Olympus...")
        for proc in processes:
            proc.terminate()

def list_bots():
    print("🏛️  The Pantheon of Olympus:")
    for name, path in BOTS.items():
        status = "✅" if path.exists() else "❌"
        print(f"  {status} {name.title()} — {path.relative_to(ROOT)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: olympus [botname|all|list]")
        sys.exit(1)

    target = sys.argv[1].lower()
    if target == "all":
        run_all()
    elif target == "list":
        list_bots()
    else:
        run_bot(target)

if __name__ == "__main__":
    main()
