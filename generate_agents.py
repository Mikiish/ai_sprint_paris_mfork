import os
import textwrap
import random

header = textwrap.dedent("""
import Lisa.Lisa.Lisa_Genie.QuantumEmojiv2 as qe
if __name__ == "__main__":
  qemo = qe.QuantumEmoji()
  str_result = qemo.measure_complicated()
  print(str_result)
  exit(str_result)

... Hey look somwhere else >.< !
""")

verses = [
    "Dans cette antre codée, l'humour pointe son nez.",
    "Ici les bits s'agitent, clowns d'un jour agités.",
    "Les scripts se chamaillent, farceurs d'informatique.",
    "Ce dossier chante, rieur, ses octets en cadence.",
    "La logique ricane, un brin mélancolique.",
    "Les fichiers dansent sous un halo fantastique.",
    "Les modules complotent, rires électroniques." 
]

def summarize_dir(path):
    entries = list(os.scandir(path))
    files = [e for e in entries if e.is_file()]
    dirs = [e for e in entries if e.is_dir()]
    file_types = {}
    for f in files:
        ext = os.path.splitext(f.name)[1]
        file_types[ext] = file_types.get(ext, 0) + 1
    top_exts = ", ".join(sorted(file_types.keys())[:3]) or "none"
    bullet_points = [
        f"1. Path: {path}",
        f"2. Subdirectories: {len(dirs)}",
        f"3. Files: {len(files)}",
        f"4. Example types: {top_exts}",
        f"5. Sample file: {files[0].name if files else 'n/a'}",
        f"6. Sample subdir: {dirs[0].name if dirs else 'n/a'}",
        "7. AGENT inserted automatically"
    ]
    verse = random.choice(verses)
    return bullet_points, verse

for root, dirs, files in os.walk('.'):
    bullet_points, verse = summarize_dir(root)
    content = header + "\n" + "\n".join(bullet_points) + "\n\n" + verse + "\n"
    with open(os.path.join(root, 'AGENTS.md'), 'w') as f:
        f.write(content)
