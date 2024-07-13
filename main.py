try:
    with open('main.py', encoding='utf-8') as f:
        exec(f.read())
except ImportError as e:
    if 'keyboard' not in str(e):
        raise ImportError
    from subprocess import run
    print("Module 'package' not installed.")
    if input("Consent to install module (y/n): ").lower() == 'y':
        run("pip install keyboard".split())
    else:
        print("Aborting execution.")
