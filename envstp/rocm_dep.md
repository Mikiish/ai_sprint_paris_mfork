Some ROCm dependencies are available in the base container `rocm/vllm-dev:nightly_0610_rc2_0610_rc2_20250605` that is provided:

```bash
pip freeze | grep aiter
# aiter @ file:///install/aiter-0.1.3.dev25%2Bg64876494-py3-none-any.whl#sha256=72290db37bac124739cf37ad0486d73b78cb91796dbbd346e3611e1e7dc410c1
pip freeze | grep torch
# torch @ file:///install/torch-2.7.0%2Bgitf717b2a-cp312-cp312-linux_x86_64.whl#sha256=f5a514d055081411e3a1779889f06840cff490eadc0bf83f587b6b3e8cab6f4b
pip freeze | grep triton
# triton @ file:///install/triton-3.2.0%2Bgite5be006a-cp312-cp312-linux_x86_64.whl#sha256=5ab00b333450c7179db7034795d0c70be6fa5e9a6ed2e203b11fb52cea116efc
```
