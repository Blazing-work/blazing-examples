# DeepSeek-R1-0528

DeepSeek R1 with enhanced reasoning depth and inference capabilities. This version significantly improves performance on mathematics, programming, and general logic benchmarks, approaching leading models like O3 and Gemini 2.5 Pro.

## Key Improvements

- **AIME 2025 accuracy:** 70% -> 87.5% (via deeper reasoning, averaging 23K tokens/question vs 12K)
- **Reduced hallucination rate**
- **Enhanced function calling support**
- **Better vibe coding experience**
- **System prompt support** (not required to add `<think>` prefix)

## Benchmarks

| Category | Benchmark | DeepSeek R1 | DeepSeek R1 0528 |
|----------|-----------|-------------|------------------|
| General | MMLU-Redux (EM) | 92.9 | 93.4 |
| General | GPQA-Diamond (Pass@1) | 71.5 | 81.0 |
| Code | LiveCodeBench (Pass@1) | 63.5 | 73.3 |
| Code | SWE Verified (Resolved) | 49.2 | 57.6 |
| Math | AIME 2024 (Pass@1) | 79.8 | 91.4 |
| Math | AIME 2025 (Pass@1) | 70.0 | 87.5 |
| Math | HMMT 2025 (Pass@1) | 41.7 | 79.4 |

## Running Locally

See the [DeepSeek-R1 repository](https://github.com/deepseek-ai/DeepSeek-R1) for local deployment instructions.

### System Prompt

```
This assistant is DeepSeek-R1, created by the DeepSeek company.
Today is {current date}.
```

### Temperature

Recommended: 0.6

## Resources

- [DeepSeek Chat](https://chat.deepseek.com/) (enable "DeepThink" mode)
- [DeepSeek API Platform](https://platform.deepseek.com/) (OpenAI-compatible)
- [Paper](https://arxiv.org/pdf/2501.12948)

## License

MIT License. Supports commercial use and distillation.
