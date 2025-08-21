from pathlib import Path
from wav_loo import NoiseSegmentsConfig, generate_noise_segments

cfg = NoiseSegmentsConfig(
    input_dir=Path("/kanas/signal/liul/source_separation/T26/real_record/real_noise/wav_output/不削波"),
    output_dir=Path("/kanas/signal/liul/source_separation/T26/real_record/real_noise/noise_segments_30s_unclipped"),
    duration_seconds=30.0,
    total_segments=60000,
    random_seed=42,
)
generate_noise_segments(cfg)

cfg = NoiseSegmentsConfig(
    input_dir=Path("/kanas/signal/liul/source_separation/T26/real_record/real_noise/wav_output/削波"),
    output_dir=Path("/kanas/signal/liul/source_separation/T26/real_record/real_noise/noise_segments_30s_clipped"),
    duration_seconds=30.0,
    total_segments=60000,
    random_seed=42,
)
generate_noise_segments(cfg)