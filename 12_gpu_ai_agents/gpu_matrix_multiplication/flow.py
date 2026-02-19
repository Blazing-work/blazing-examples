"""
GPU Matrix Multiplication

Demonstrates running a GPU-accelerated matrix multiplication step on an A100 GPU.
The step auto-selects the best available device (MPS on Apple Silicon, CUDA on
NVIDIA, or CPU as fallback) and multiplies two random matrices using PyTorch.

Patterns shown:
  1. @app.step(gpu='A100') to request an A100 GPU worker for the step
  2. torch.backends.mps / torch.cuda.is_available() for device auto-selection
  3. torch.matmul on the selected device, returning device type and output shape
"""
from blazing import Blazing


async def main():
    app = Blazing()

    @app.step(gpu='A100')
    async def gpu_matmul(size: int, services=None):
        import torch

        device = None
        if torch.backends.mps.is_available():
            device = torch.device('mps')
        elif torch.cuda.is_available():
            device = torch.device('cuda')
        else:
            device = torch.device('cpu')

        a = torch.randn(size, size, device=device)
        b = torch.randn(size, size, device=device)
        c = torch.matmul(a, b)
        return {'device': str(device), 'shape': list(c.shape)}

    @app.workflow
    async def run_gpu(size: int, services=None):
        return await gpu_matmul(size, services=services)

    await app.publish()
    result = await app.run_gpu(size=512).wait_result()
    print(result)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
