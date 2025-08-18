#!/usr/bin/env python3
import os
from pathlib import Path

from wav_loo.data_gen import CarDataGenerator, GenerationConfig


def main():
    base = Path(__file__).resolve().parent
    ir_root = base / 'ir'
    clean_root = base / 'clean'
    out_dir = base / 'out_debug'

    cfg = GenerationConfig(
        ir_root_dir=str(ir_root),
        clean_root_dir=str(clean_root),
        output_dir=str(out_dir),
        sample_rate=16000,
        num_samples=6,
        zones=2,
        random_seed=2,
        max_clean_seconds=30.0,
    )

    print("Config:", cfg)
    gen = CarDataGenerator(cfg)
    gen.generate()
    print("Done. Outputs at:", out_dir)


if __name__ == '__main__':
    main() 