# generate_precomputed.py
import json
import time
import os
import QuantumEmojiv2 as qe

def build_precomputed_data(intervals):
    map_cp_to_fused_states = {}
    map_cp_to_all_states = {}

    for (start, end) in intervals:
        for cp_x in range(start, end + 1):
            char_x = chr(cp_x)
            if qe.is_printable_noncontrol(char_x):
                fused_states, all_states = qe.generate_states_for(cp_x, intervals)
                map_cp_to_fused_states[cp_x] = fused_states
                map_cp_to_all_states[cp_x]   = all_states

    return map_cp_to_fused_states, map_cp_to_all_states

def save_as_json(filepath, intervals):
    time_start = time.time()
    print(f"Il est  {time_start}.\n")
    fused, all_states = build_precomputed_data(intervals)
    time_end = time.time()
    print(f"Il est {time_end}.\nIl s'est écoulé {time_end - time_start}.\n")

    # Convertir les clés (codepoints int) en chaînes, car JSON n’autorise pas les clés int
    fused_str_keys = {str(cp): states for cp, states in fused.items()}
    all_states_str_keys = {str(cp): states for cp, states in all_states.items()}

    data = {
        "fused": fused_str_keys,
        "all_states": all_states_str_keys
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    time_finish = time.time()
    print(f"Il est {time_finish}.\nIl s'est écoulé {time_finish - time_start}.\n")
if __name__ == "__main__":
    # ex. intervals = ...
    # On définit INTERVALS quelque part ou on l’importe
    quantum_intervals = qe.INTERVALS  # par ex.
    out_file = "precomputed_emoji_data.json"

    # Lance le gros scan
    print("Démarrage du pré-calcul, ça peut prendre un moment...")
    save_as_json(out_file, quantum_intervals)
    print(f"Fichier JSON généré : {out_file}")
    print(f"Il est {time.time()}.\n")
