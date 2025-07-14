# ROCm and Triton setup check

## rocm_cfg_check.sh
- Added check for existing ROCm installation.
- Defines desired version `6.4.1` and compares with installed one.
- Skips installation if version matches.

## triton_build.sh
- Activates Python virtual environment before upgrading `pip`.
- General cleanup for reliable environment setup.

