"""
GPU PyTorch Steps — A100 Matrix Mul + H100 Neural Network

Chain two GPU-specialized steps in a workflow: an A100 step runs matrix
multiplication and returns TFLOPS, then an H100 step builds an MLP and runs
neural network inference on the result. In local dev both fall back to
Metal/MPS on Apple Silicon or CUDA on NVIDIA; in production Blazing allocates
the matching GPU worker type for each step.

Patterns shown:
  1. @app.step(gpu='A100') — request A100 GPU worker for matrix multiplication
  2. @app.step(gpu='H100') — request H100 GPU worker for neural network inference
  3. torch.backends.mps.is_available() / torch.cuda.is_available() — device auto-selection
  4. torch.randn + torch.matmul — GPU tensor operations inside a Blazing step
  5. nn.Sequential (Linear + ReLU layers) + torch.no_grad() inference
  6. Multi-step GPU pipeline: step 1 output feeds step 2 input
  7. torch.mps.synchronize() / torch.cuda.synchronize() — GPU timing

Requires: pip install blazing torch
          GPU device (Apple Silicon MPS, NVIDIA CUDA) OR falls back to CPU
"""

import asyncio
import os

from blazing import Blazing


app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder"),
)


# ── Step 1: A100 matrix multiplication ───────────────────────────────────────
# All torch imports are INSIDE the step function — steps run remotely and
# must be self-contained; module-level imports would not be available there.

@app.step(gpu="A100")
async def gpu_matmul(size: int, services=None) -> dict:
    """
    Perform matrix multiplication on GPU.

    In production: uses allocated A100 GPU worker.
    In local dev: falls back to Metal (MPS) on Apple Silicon or CUDA on NVIDIA.
    """
    import time
    import torch

    # Device auto-selection: MPS > CUDA > CPU
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        device_name = "Metal (MPS)"
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        device_name = f"CUDA ({torch.cuda.get_device_name(0)})"
    else:
        device = torch.device("cpu")
        device_name = "CPU (no GPU available)"

    # Create random tensors on device
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)

    # Warmup pass
    _ = torch.matmul(a, b)
    if device.type == "mps":
        torch.mps.synchronize()
    elif device.type == "cuda":
        torch.cuda.synchronize()

    # Timed computation
    start = time.perf_counter()
    c = torch.matmul(a, b)
    if device.type == "mps":
        torch.mps.synchronize()
    elif device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    # 2n³ FLOPs for matrix multiplication
    tflops = 2 * size ** 3 / elapsed / 1e12

    return {
        "device": device_name,
        "size": size,
        "tflops": round(tflops, 2),
        "result_shape": list(c.shape),
    }


# ── Step 2: H100 neural network inference ─────────────────────────────────────

@app.step(gpu="H100")
async def gpu_neural_net(batch_size: int, input_dim: int, hidden_dim: int, output_dim: int, services=None) -> dict:
    """
    Run MLP inference on GPU.

    In production: uses allocated H100 GPU worker.
    In local dev: falls back to Metal (MPS) on Apple Silicon or CUDA on NVIDIA.
    """
    import time
    import torch
    import torch.nn as nn

    # Device auto-selection: MPS > CUDA > CPU
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        device_name = "Metal (MPS)"
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        device_name = f"CUDA ({torch.cuda.get_device_name(0)})"
    else:
        device = torch.device("cpu")
        device_name = "CPU"

    # Build a 3-layer MLP
    model = nn.Sequential(
        nn.Linear(input_dim, hidden_dim),
        nn.ReLU(),
        nn.Linear(hidden_dim, hidden_dim),
        nn.ReLU(),
        nn.Linear(hidden_dim, output_dim),
    ).to(device)

    x = torch.randn(batch_size, input_dim, device=device)

    # Warmup pass
    with torch.no_grad():
        _ = model(x)
    if device.type == "mps":
        torch.mps.synchronize()
    elif device.type == "cuda":
        torch.cuda.synchronize()

    # Timed inference
    start = time.perf_counter()
    with torch.no_grad():
        output = model(x)
    if device.type == "mps":
        torch.mps.synchronize()
    elif device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    throughput = batch_size / elapsed

    return {
        "device": device_name,
        "output_shape": list(output.shape),
        "throughput": round(throughput, 1),
        "output_sample": output[0, :5].tolist(),
    }


# ── Workflow: chain A100 matmul → H100 neural net ─────────────────────────────

@app.workflow
async def gpu_pipeline(services=None) -> dict:
    """
    Multi-step GPU pipeline:
      Step 1 (A100): 512x512 matrix multiplication — returns TFLOPS
      Step 2 (H100): MLP inference on 64-sample batch — returns throughput
    """
    matmul_result = await gpu_matmul(size=512, services=services)
    nn_result = await gpu_neural_net(
        batch_size=64,
        input_dim=784,
        hidden_dim=256,
        output_dim=10,
        services=services,
    )
    return {"matmul": matmul_result, "neural_net": nn_result}


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    print("=== GPU PyTorch Steps — A100 Matrix Mul + H100 Neural Network ===")
    print()

    await app.publish()
    print("[Setup] Published GPU steps (gpu_matmul A100, gpu_neural_net H100)")
    print()

    result = await app.run(gpu_pipeline)

    matmul = result["matmul"]
    nn = result["neural_net"]

    print("--- Step 1: A100 Matrix Multiplication ---")
    print(f"  Device:       {matmul['device']}")
    print(f"  Matrix size:  {matmul['size']}x{matmul['size']}")
    print(f"  Performance:  {matmul['tflops']} TFLOPS")
    print(f"  Result shape: {matmul['result_shape']}")
    print()

    print("--- Step 2: H100 Neural Network Inference ---")
    print(f"  Device:       {nn['device']}")
    print(f"  Output shape: {nn['output_shape']}")
    print(f"  Throughput:   {nn['throughput']} samples/sec")
    print(f"  Output[0,:5]: {[round(v, 4) for v in nn['output_sample']]}")
    print()

    print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())
