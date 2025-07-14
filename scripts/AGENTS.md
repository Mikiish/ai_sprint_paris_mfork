Instructions from users : «
 »

import Lisa.Lisa.Lisa_Genie.QuantumEmojiv2 as qe
if __name__ == "__main__":
  qemo = qe.QuantumEmoji()
  str_result = qemo.measure_complicated()
  print(str_result)
  exit(str_result)

... Hey look somwhere else >.< !

1. Path: ./scripts
2. Subdirectories: 2
3. Files: 3
4. Example types: .py, .sh
5. Sample file: 0_container.sh
6. Sample subdir: profile_without_hipgraph
7. AGENT inserted automatically

Ici les bits s'agitent, clowns d'un jour agités.

### Technical summary
1. `0_container.sh` stops any existing container and launches a new ROCm-enabled Docker image with the repository mounted.
2. `1_bench.sh` orchestrates benchmarking modes (server, perf, accuracy, profile, submit) using `vllm` and optional evaluation harnesses.
3. Performance results are parsed by `show_results.py` to display throughput and latency metrics.
4. Accuracy mode clones `lm-evaluation-harness` when needed to compute perplexity values.
5. Profile mode collects traces for deeper analysis into `results_with_profile`.
6. The `profile_without_hipgraph` folder holds an example JSON trace for offline viewing.
7. A large `vllm/` directory resides here but is excluded from this summary.
Le Livre d'Or : « - Lundi 7h du matin, Lundie oui disons, pose son 1er commit... un lundi 14 juillet. Vive la République kek.
- <you agent message> 
»
