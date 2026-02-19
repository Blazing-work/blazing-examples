# Expected Output

## Running

```bash
python flow.py
```

## Requirements

- `pip install blazing torch`
- GPU device: Apple Silicon (MPS), NVIDIA (CUDA), or falls back to CPU
- Running Blazing infrastructure: `docker-compose up -d`
- `BLAZING_API_URL` (defaults to `http://localhost:8000`)
- `BLAZING_API_TOKEN` (defaults to `demo-token-placeholder`)

## Output

```
=== GPU PyTorch Steps — A100 Matrix Mul + H100 Neural Network ===

[Setup] Published GPU steps (gpu_matmul A100, gpu_neural_net H100)

--- Step 1: A100 Matrix Multiplication ---
  Device:       Metal (MPS)
  Matrix size:  512x512
  Performance:  2.34 TFLOPS
  Result shape: [512, 512]

--- Step 2: H100 Neural Network Inference ---
  Device:       Metal (MPS)
  Output shape: [64, 10]
  Throughput:   15823.4 samples/sec
  Output[0,:5]: [0.1234, -0.4567, 0.2891, -0.1045, 0.3312]

=== Done ===
```

## GPU Routing

| Step | Decorator | Production Worker | Local Fallback |
|------|-----------|-------------------|----------------|
| `gpu_matmul` | `@app.step(gpu='A100')` | NVIDIA A100 | Metal (MPS) or CUDA |
| `gpu_neural_net` | `@app.step(gpu='H100')` | NVIDIA H100 | Metal (MPS) or CUDA |

## Notes

- Device name varies by hardware: `Metal (MPS)` on Apple Silicon, `CUDA (NVIDIA A100 80GB)` on NVIDIA
- TFLOPS value depends on GPU speed — expect 1–10 TFLOPS on consumer hardware
- Matrix shape is always `[512, 512]` since `size=512`
- Neural net output shape is always `[64, 10]` (batch=64, classes=10)
- `output_sample` values are random floats — exact values differ each run
- All torch imports are inside the step functions: steps run in isolated workers, module-level imports are not forwarded
- `torch.mps.synchronize()` / `torch.cuda.synchronize()` ensures timing is accurate by flushing GPU operations
