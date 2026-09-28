# Paired statistics over the committed ten-seed sweeps

Metric `test_loss`, 78 paired comparisons, alpha = 0.05. Differences are `A - B`, so **negative favours A**.

Every interval and p-value below comes from the committed per-seed files; no experiment was
re-run to produce this. The sign test and the Wilcoxon signed-rank test are computed by
enumeration (exact for ten pairs), the interval under the median is a deterministic percentile
bootstrap, and the last p-value column is Holm-adjusted across the whole table, so a single
p < 0.05 in a run of this many comparisons is not by itself a result.

A failed test is written as **no evidence of a difference at this budget**. With ten seeds the
power to detect anything but a large effect is low, and that sentence is deliberately not the
same as "no difference".

The **MDE** column is the smallest true difference this design could detect with 80% power at
this spread — about one per-seed standard deviation of the paired differences. It is the number
that makes a non-significant result readable: an interval that excludes effects larger than the
MDE bounds the effect, it does not establish its absence.

## The comparisons the headline claims rest on

| suite | comparison | wins/n | median diff [95% boot] | mean diff [95% t] | d_z | MDE(80%) | sign p | wilcoxon p | holm p | verdict |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---|
| `activation-gelu` | schedule_free_adamw vs adamw_cosine | 8/10 | -0.00208 [-0.00499, +0.00048] | -0.00273 [-0.00571, +0.00025] | -0.66 | 0.00414 | 0.1094 | 0.0645 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `activation-relu` | schedule_free_adamw vs adamw_cosine | 8/10 | -0.00306 [-0.00591, -0.00100] | -0.00560 [-0.01237, +0.00117] | -0.59 | 0.00941 | 0.1094 | 0.0195 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `ademamix-mlp` | ademamix_no_warmups vs adamw | 2/10 | +0.00036 [+0.00004, +0.00052] | +0.00030 [+0.00010, +0.00050] | +1.09 | 0.00028 | 0.1094 | 0.0195 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `capacity-h16x16` | schedule_free_adamw vs adamw_cosine | 10/10 | -0.02692 [-0.04536, -0.01102] | -0.02977 [-0.04746, -0.01207] | -1.20 | 0.02460 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `capacity-h32` | schedule_free_adamw vs adamw_cosine | 8/10 | -0.00170 [-0.00514, +0.00024] | -0.00373 [-0.00856, +0.00109] | -0.55 | 0.00671 | 0.1094 | 0.1055 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `capacity-h64` | schedule_free_adamw vs adamw_cosine | 9/10 | -0.00507 [-0.01381, -0.00187] | -0.00904 [-0.01847, +0.00038] | -0.69 | 0.01311 | 0.0215 | 0.0098 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `init-he` | schedule_free_adamw vs adamw_cosine | 9/10 | -0.00335 [-0.01013, -0.00061] | -0.00566 [-0.01079, -0.00054] | -0.79 | 0.00712 | 0.0215 | 0.0039 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `init-plain` | schedule_free_adamw vs adamw_cosine | 5/10 | -0.00002 [-0.00114, +0.00029] | -0.00052 [-0.00146, +0.00041] | -0.40 | 0.00130 | 1.0000 | 0.5566 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-batchnorm` | schedule_free_adamw vs adamw_cosine | 5/10 | -0.00040 [-0.00256, +0.00053] | -0.00094 [-0.00216, +0.00028] | -0.55 | 0.00169 | 1.0000 | 0.2324 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-layernorm` | schedule_free_adamw vs adamw_cosine | 3/10 | +0.00198 [-0.00015, +0.00856] | +0.00374 [-0.00112, +0.00860] | +0.55 | 0.00676 | 0.3438 | 0.1309 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `optimizers` | adam vs baseline | 10/10 | -0.08096 [-0.08640, -0.07089] | -0.07905 [-0.08507, -0.07303] | -9.39 | 0.00837 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `schedule-free-mlp` | schedule_free_adamw vs adamw_cosine | 9/10 | -0.00130 [-0.00273, -0.00063] | -0.00128 [-0.00352, +0.00096] | -0.41 | 0.00311 | 0.0215 | 0.0645 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |

## Each claim inside the family it was actually tested in

Correcting across every printed table answers a question nobody asked. These are the
repository's two negative results, each treated as **one** claim tested repeatedly, with the
correction applied over the repetitions only.

| claim | suites in family | smallest raw p | smallest adjusted p | comparisons surviving |
|---|---:|---:|---:|---:|
| schedule-free beats a tuned cosine (one claim, ten suites) | 10 | 0.0020 | 0.0195 | 1/10 |
| AdEMAMix has no advantage over AdamW at matched settings (one claim, twelve suites) | 11 | 0.0215 | 0.2363 | 0/11 |

Per suite, inside that family:

| claim | suite | wins/n | median diff [95% boot] | raw p | adjusted p | verdict |
|---|---|---:|---|---:|---:|---|
| schedule-free beats a tuned cosine | `schedule-free-mlp` | 9/10 | -0.00130 [-0.00273, -0.00063] | 0.0645 | 0.4512 | no evidence of a difference at this budget (not the same claim as no difference) |
| schedule-free beats a tuned cosine | `capacity-h32` | 8/10 | -0.00170 [-0.00514, +0.00024] | 0.1094 | 0.6562 | no evidence of a difference at this budget (not the same claim as no difference) |
| schedule-free beats a tuned cosine | `capacity-h64` | 9/10 | -0.00507 [-0.01381, -0.00187] | 0.0215 | 0.1934 | no evidence of a difference at this budget (not the same claim as no difference) |
| schedule-free beats a tuned cosine | `capacity-h16x16` | 10/10 | -0.02692 [-0.04536, -0.01102] | 0.0020 | 0.0195 | evidence of a difference (both tests agree; A is better on this metric) |
| schedule-free beats a tuned cosine | `activation-relu` | 8/10 | -0.00306 [-0.00591, -0.00100] | 0.1094 | 0.6562 | no evidence of a difference at this budget (not the same claim as no difference) |
| schedule-free beats a tuned cosine | `activation-gelu` | 8/10 | -0.00208 [-0.00499, +0.00048] | 0.1094 | 0.6562 | no evidence of a difference at this budget (not the same claim as no difference) |
| schedule-free beats a tuned cosine | `norm-layernorm` | 3/10 | +0.00198 [-0.00015, +0.00856] | 0.3438 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| schedule-free beats a tuned cosine | `norm-batchnorm` | 5/10 | -0.00040 [-0.00256, +0.00053] | 1.0000 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| schedule-free beats a tuned cosine | `init-he` | 9/10 | -0.00335 [-0.01013, -0.00061] | 0.0215 | 0.1934 | evidence of a difference (both tests agree; A is better on this metric) |
| schedule-free beats a tuned cosine | `init-plain` | 5/10 | -0.00002 [-0.00114, +0.00029] | 1.0000 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `ademamix` | 6/10 | -0.00004 [-0.00013, +0.00040] | 0.8457 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `ademamix-mlp` | 2/10 | +0.00036 [+0.00004, +0.00052] | 0.1094 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `capacity-h32` | 2/10 | +0.00067 [+0.00010, +0.00168] | 0.1094 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `capacity-h64` | 2/10 | +0.00081 [+0.00001, +0.00147] | 0.1094 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `capacity-h16x16` | 2/10 | +0.00411 [-0.00126, +0.00977] | 0.1934 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `norm-layernorm` | 8/10 | -0.00005 [-0.00021, +0.00001] | 0.1309 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `norm-batchnorm` | 2/10 | +0.00003 [+0.00000, +0.00011] | 0.1094 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `init-he` | 1/10 | +0.00190 [+0.00030, +0.00430] | 0.0215 | 0.2363 | evidence of a difference (both tests agree; A is worse on this metric) |
| AdEMAMix has no advantage over AdamW at matched settings | `init-plain` | 3/10 | +0.00034 [-0.00023, +0.00151] | 0.3438 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `activation-relu` | 3/10 | +0.00005 [-0.00014, +0.00027] | 0.5566 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| AdEMAMix has no advantage over AdamW at matched settings | `activation-gelu` | 3/10 | +0.00011 [-0.00000, +0.00031] | 0.3438 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |

## Every comparison (arm versus its suite's baseline)

| suite | comparison | wins/n | median diff [95% boot] | mean diff [95% t] | d_z | MDE(80%) | sign p | wilcoxon p | holm p | verdict |
|---|---|---:|---|---|---:|---:|---:|---:|---:|---|
| `activation-gelu` | adamw_constant vs adamw_cosine | 7/10 | -0.00080 [-0.00550, +0.00008] | -0.00269 [-0.00582, +0.00044] | -0.62 | 0.00435 | 0.3438 | 0.0840 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `activation-gelu` | adam vs adamw_cosine | 7/10 | -0.00080 [-0.00550, +0.00008] | -0.00269 [-0.00582, +0.00044] | -0.62 | 0.00435 | 0.3438 | 0.0840 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `activation-gelu` | adagrad vs adamw_cosine | 9/10 | -0.00158 [-0.00578, -0.00053] | -0.00344 [-0.00686, -0.00001] | -0.72 | 0.00477 | 0.0215 | 0.0137 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `activation-gelu` | ademamix vs adamw_cosine | 6/10 | -0.00074 [-0.00533, +0.00015] | -0.00255 [-0.00562, +0.00053] | -0.59 | 0.00428 | 0.7539 | 0.1055 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `activation-gelu` | schedule_free_adamw vs adamw_cosine | 8/10 | -0.00208 [-0.00499, +0.00048] | -0.00273 [-0.00571, +0.00025] | -0.66 | 0.00414 | 0.1094 | 0.0645 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `activation-relu` | adamw_constant vs adamw_cosine | 9/10 | -0.00289 [-0.00787, -0.00036] | -0.00449 [-0.00827, -0.00070] | -0.85 | 0.00526 | 0.0215 | 0.0137 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `activation-relu` | adam vs adamw_cosine | 9/10 | -0.00289 [-0.00787, -0.00036] | -0.00449 [-0.00827, -0.00070] | -0.85 | 0.00526 | 0.0215 | 0.0137 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `activation-relu` | adagrad vs adamw_cosine | 9/10 | -0.00452 [-0.00698, -0.00214] | -0.00715 [-0.01485, +0.00054] | -0.66 | 0.01070 | 0.0215 | 0.0059 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `activation-relu` | ademamix vs adamw_cosine | 9/10 | -0.00281 [-0.00834, -0.00015] | -0.00453 [-0.00833, -0.00073] | -0.85 | 0.00528 | 0.0215 | 0.0137 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `activation-relu` | schedule_free_adamw vs adamw_cosine | 8/10 | -0.00306 [-0.00591, -0.00100] | -0.00560 [-0.01237, +0.00117] | -0.59 | 0.00941 | 0.1094 | 0.0195 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `ademamix` | ademamix_tuned vs adamw | 6/10 | -0.00004 [-0.00013, +0.00040] | +0.00005 [-0.00018, +0.00028] | +0.15 | 0.00032 | 0.7539 | 0.8457 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `ademamix` | ademamix_paper_warmups vs adamw | 3/10 | +0.00249 [-0.00040, +0.00479] | +0.00265 [+0.00063, +0.00468] | +0.94 | 0.00282 | 0.3438 | 0.0273 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `ademamix` | ademamix_no_slow_ema vs adamw | 0/10 | +0.00000 [+0.00000, +0.00000] | +0.00000 [+0.00000, +0.00000] | +0.00 | 0.00000 | 1.0000 | 1.0000 | 1.0000 | the two arms are identical in every seed, so there is nothing to test |
| `ademamix` | sgd_momentum vs adamw | 4/10 | +0.00148 [-0.00192, +0.00296] | +0.00094 [-0.00097, +0.00286] | +0.35 | 0.00266 | 0.7539 | 0.2754 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `ademamix-mlp` | ademamix_no_warmups vs adamw | 2/10 | +0.00036 [+0.00004, +0.00052] | +0.00030 [+0.00010, +0.00050] | +1.09 | 0.00028 | 0.1094 | 0.0195 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `ademamix-mlp` | ademamix_warmup_45 vs adamw | 3/10 | +0.00738 [-0.00072, +0.02362] | +0.01051 [+0.00059, +0.02043] | +0.76 | 0.01379 | 0.3438 | 0.0488 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `ademamix-mlp` | ademamix_warmup_120 vs adamw | 2/10 | +0.01762 [+0.00139, +0.04166] | +0.02043 [+0.00603, +0.03483] | +1.01 | 0.02002 | 0.1094 | 0.0195 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `ademamix-mlp` | sgd_momentum vs adamw | 8/10 | -0.00144 [-0.00332, -0.00038] | -0.00193 [-0.00404, +0.00019] | -0.65 | 0.00294 | 0.1094 | 0.0488 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `capacity-h16x16` | adamw_constant vs adamw_cosine | 0/10 | +0.03810 [+0.02600, +0.06397] | +0.04500 [+0.02740, +0.06259] | +1.83 | 0.02446 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h16x16` | adam vs adamw_cosine | 0/10 | +0.03810 [+0.02600, +0.06397] | +0.04500 [+0.02740, +0.06259] | +1.83 | 0.02446 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h16x16` | adagrad vs adamw_cosine | 9/10 | -0.02199 [-0.04435, -0.00214] | -0.02563 [-0.04840, -0.00286] | -0.81 | 0.03166 | 0.0215 | 0.0195 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `capacity-h16x16` | ademamix vs adamw_cosine | 0/10 | +0.04192 [+0.03312, +0.06648] | +0.04828 [+0.03059, +0.06596] | +1.95 | 0.02459 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h16x16` | schedule_free_adamw vs adamw_cosine | 10/10 | -0.02692 [-0.04536, -0.01102] | -0.02977 [-0.04746, -0.01207] | -1.20 | 0.02460 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `capacity-h32` | adamw_constant vs adamw_cosine | 1/10 | +0.00424 [+0.00085, +0.01694] | +0.00838 [+0.00017, +0.01659] | +0.73 | 0.01142 | 0.0215 | 0.0039 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h32` | adam vs adamw_cosine | 1/10 | +0.00424 [+0.00085, +0.01694] | +0.00838 [+0.00017, +0.01659] | +0.73 | 0.01142 | 0.0215 | 0.0039 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h32` | adagrad vs adamw_cosine | 9/10 | -0.00984 [-0.01426, -0.00450] | -0.01032 [-0.01671, -0.00394] | -1.16 | 0.00888 | 0.0215 | 0.0039 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `capacity-h32` | ademamix vs adamw_cosine | 1/10 | +0.00458 [+0.00108, +0.01871] | +0.00921 [+0.00048, +0.01794] | +0.75 | 0.01214 | 0.0215 | 0.0039 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h32` | schedule_free_adamw vs adamw_cosine | 8/10 | -0.00170 [-0.00514, +0.00024] | -0.00373 [-0.00856, +0.00109] | -0.55 | 0.00671 | 0.1094 | 0.1055 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `capacity-h64` | adamw_constant vs adamw_cosine | 1/10 | +0.00481 [+0.00118, +0.01288] | +0.00672 [+0.00215, +0.01129] | +1.05 | 0.00635 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h64` | adam vs adamw_cosine | 1/10 | +0.00481 [+0.00118, +0.01288] | +0.00672 [+0.00215, +0.01129] | +1.05 | 0.00635 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h64` | adagrad vs adamw_cosine | 9/10 | -0.00772 [-0.01990, -0.00553] | -0.01238 [-0.02223, -0.00252] | -0.90 | 0.01370 | 0.0215 | 0.0039 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `capacity-h64` | ademamix vs adamw_cosine | 1/10 | +0.00530 [+0.00132, +0.01430] | +0.00760 [+0.00235, +0.01285] | +1.04 | 0.00730 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h64` | schedule_free_adamw vs adamw_cosine | 9/10 | -0.00507 [-0.01381, -0.00187] | -0.00904 [-0.01847, +0.00038] | -0.69 | 0.01311 | 0.0215 | 0.0098 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `capacity-h8x8` | adamw_constant vs adamw_cosine | 1/10 | +0.03187 [+0.01310, +0.03819] | +0.02685 [+0.01071, +0.04299] | +1.19 | 0.02244 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h8x8` | adam vs adamw_cosine | 1/10 | +0.03187 [+0.01310, +0.03819] | +0.02685 [+0.01071, +0.04299] | +1.19 | 0.02244 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h8x8` | adagrad vs adamw_cosine | 10/10 | -0.05091 [-0.06369, -0.00751] | -0.03949 [-0.06109, -0.01788] | -1.31 | 0.03004 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `capacity-h8x8` | ademamix vs adamw_cosine | 1/10 | +0.03272 [+0.01435, +0.04254] | +0.02999 [+0.01347, +0.04652] | +1.30 | 0.02298 | 0.0215 | 0.0059 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `capacity-h8x8` | schedule_free_adamw vs adamw_cosine | 8/10 | -0.02211 [-0.04761, -0.00269] | -0.02314 [-0.03965, -0.00663] | -1.00 | 0.02295 | 0.1094 | 0.0195 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `init-he` | adamw_constant vs adamw_cosine | 2/10 | +0.00516 [+0.00101, +0.01537] | +0.01059 [-0.00116, +0.02234] | +0.64 | 0.01634 | 0.1094 | 0.0273 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `init-he` | adam vs adamw_cosine | 2/10 | +0.00516 [+0.00101, +0.01537] | +0.01059 [-0.00116, +0.02234] | +0.64 | 0.01634 | 0.1094 | 0.0273 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `init-he` | adagrad vs adamw_cosine | 9/10 | -0.00827 [-0.02139, -0.00291] | -0.01196 [-0.02130, -0.00262] | -0.92 | 0.01299 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `init-he` | ademamix vs adamw_cosine | 1/10 | +0.00706 [+0.00130, +0.01853] | +0.01296 [-0.00029, +0.02622] | +0.70 | 0.01843 | 0.0215 | 0.0137 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `init-he` | schedule_free_adamw vs adamw_cosine | 9/10 | -0.00335 [-0.01013, -0.00061] | -0.00566 [-0.01079, -0.00054] | -0.79 | 0.00712 | 0.0215 | 0.0039 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
| `init-plain` | adamw_constant vs adamw_cosine | 1/10 | +0.00812 [+0.00498, +0.01416] | +0.01092 [+0.00213, +0.01971] | +0.89 | 0.01222 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `init-plain` | adam vs adamw_cosine | 1/10 | +0.00812 [+0.00498, +0.01416] | +0.01092 [+0.00213, +0.01971] | +0.89 | 0.01222 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `init-plain` | adagrad vs adamw_cosine | 1/10 | +0.00561 [+0.00021, +0.01496] | +0.00765 [+0.00038, +0.01491] | +0.75 | 0.01011 | 0.0215 | 0.0195 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `init-plain` | ademamix vs adamw_cosine | 1/10 | +0.00983 [+0.00591, +0.01926] | +0.01287 [+0.00356, +0.02219] | +0.99 | 0.01295 | 0.0215 | 0.0059 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `init-plain` | schedule_free_adamw vs adamw_cosine | 5/10 | -0.00002 [-0.00114, +0.00029] | -0.00052 [-0.00146, +0.00041] | -0.40 | 0.00130 | 1.0000 | 0.5566 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `main` | adam_reproduction vs baseline | 10/10 | -0.17727 [-0.18567, -0.17082] | -0.17797 [-0.18349, -0.17245] | -23.07 | 0.00767 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `main` | adam_regularized vs baseline | 10/10 | -0.06304 [-0.07009, -0.05783] | -0.06434 [-0.06891, -0.05978] | -10.09 | 0.00634 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `main` | sgd_control vs baseline | 10/10 | -0.10125 [-0.10323, -0.09802] | -0.10128 [-0.10381, -0.09874] | -28.56 | 0.00353 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `norm-batchnorm` | adamw_constant vs adamw_cosine | 3/10 | +0.00028 [-0.00002, +0.00057] | +0.00030 [-0.00027, +0.00086] | +0.38 | 0.00078 | 0.3438 | 0.1309 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-batchnorm` | adam vs adamw_cosine | 3/10 | +0.00028 [-0.00002, +0.00057] | +0.00030 [-0.00027, +0.00086] | +0.38 | 0.00078 | 0.3438 | 0.1309 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-batchnorm` | adagrad vs adamw_cosine | 6/10 | -0.00090 [-0.00213, +0.00033] | -0.00094 [-0.00196, +0.00008] | -0.66 | 0.00142 | 0.7539 | 0.1309 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-batchnorm` | ademamix vs adamw_cosine | 3/10 | +0.00037 [-0.00002, +0.00061] | +0.00035 [-0.00023, +0.00094] | +0.44 | 0.00081 | 0.3438 | 0.1309 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-batchnorm` | schedule_free_adamw vs adamw_cosine | 5/10 | -0.00040 [-0.00256, +0.00053] | -0.00094 [-0.00216, +0.00028] | -0.55 | 0.00169 | 1.0000 | 0.2324 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-layernorm` | adamw_constant vs adamw_cosine | 5/10 | +0.00122 [-0.00082, +0.00352] | +0.00137 [-0.00031, +0.00305] | +0.58 | 0.00234 | 1.0000 | 0.2324 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-layernorm` | adam vs adamw_cosine | 5/10 | +0.00122 [-0.00082, +0.00352] | +0.00137 [-0.00031, +0.00305] | +0.58 | 0.00234 | 1.0000 | 0.2324 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-layernorm` | adagrad vs adamw_cosine | 4/10 | +0.00020 [-0.00105, +0.00326] | +0.00132 [-0.00096, +0.00359] | +0.41 | 0.00316 | 0.7539 | 0.3223 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-layernorm` | ademamix vs adamw_cosine | 5/10 | +0.00114 [-0.00085, +0.00381] | +0.00128 [-0.00035, +0.00292] | +0.56 | 0.00227 | 1.0000 | 0.2324 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `norm-layernorm` | schedule_free_adamw vs adamw_cosine | 3/10 | +0.00198 [-0.00015, +0.00856] | +0.00374 [-0.00112, +0.00860] | +0.55 | 0.00676 | 0.3438 | 0.1309 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `optimizers` | sgd_momentum vs baseline | 10/10 | -0.08123 [-0.08669, -0.07120] | -0.07930 [-0.08524, -0.07335] | -9.54 | 0.00827 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `optimizers` | adagrad vs baseline | 10/10 | -0.08221 [-0.08917, -0.07058] | -0.08012 [-0.08679, -0.07346] | -8.60 | 0.00927 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `optimizers` | rmsprop vs baseline | 10/10 | -0.08086 [-0.09156, -0.07063] | -0.08089 [-0.08837, -0.07341] | -7.73 | 0.01040 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `optimizers` | adam vs baseline | 10/10 | -0.08096 [-0.08640, -0.07089] | -0.07905 [-0.08507, -0.07303] | -9.39 | 0.00837 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `optimizers` | adam_no_bias_correction vs baseline | 10/10 | -0.08316 [-0.09135, -0.06905] | -0.08046 [-0.08815, -0.07278] | -7.49 | 0.01068 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is better on this metric) |
| `optimizers-mlp` | sgd_momentum vs sgd | 2/10 | +0.00604 [+0.00084, +0.00789] | +0.00463 [+0.00158, +0.00768] | +1.09 | 0.00424 | 0.1094 | 0.0137 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `optimizers-mlp` | adagrad vs sgd | 2/10 | +0.00476 [+0.00030, +0.00863] | +0.00452 [+0.00155, +0.00750] | +1.09 | 0.00414 | 0.1094 | 0.0137 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `optimizers-mlp` | rmsprop vs sgd | 3/10 | +0.00171 [-0.00198, +0.00484] | +0.00167 [-0.00139, +0.00473] | +0.39 | 0.00426 | 0.3438 | 0.2754 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `optimizers-mlp` | adam vs sgd | 2/10 | +0.00845 [+0.00104, +0.05678] | +0.02319 [+0.00332, +0.04306] | +0.83 | 0.02762 | 0.1094 | 0.0195 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `schedule-free` | adamw_constant vs adamw_cosine | 7/10 | -0.00193 [-0.00318, +0.00038] | -0.00162 [-0.00291, -0.00032] | -0.89 | 0.00180 | 0.3438 | 0.0273 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `schedule-free` | schedule_free_adamw vs adamw_cosine | 0/10 | +0.00027 [+0.00014, +0.00047] | +0.00032 [+0.00017, +0.00047] | +1.54 | 0.00021 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is worse on this metric) |
| `schedule-free` | sgd_cosine vs adamw_cosine | 0/10 | +0.09228 [+0.08208, +0.09720] | +0.09045 [+0.08422, +0.09669] | +10.38 | 0.00867 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is worse on this metric) |
| `schedule-free` | schedule_free_sgd vs adamw_cosine | 0/10 | +0.07187 [+0.06290, +0.07681] | +0.07029 [+0.06457, +0.07601] | +8.79 | 0.00795 | 0.0020 | 0.0020 | 0.1523 | evidence of a difference (both tests agree; A is worse on this metric) |
| `schedule-free-mlp` | adamw_constant vs adamw_cosine | 1/10 | +0.00385 [+0.00138, +0.01088] | +0.00574 [+0.00143, +0.01005] | +0.95 | 0.00599 | 0.0215 | 0.0098 | 1.0000 | evidence of a difference (both tests agree; A is worse on this metric) |
| `schedule-free-mlp` | schedule_free_adamw vs adamw_cosine | 9/10 | -0.00130 [-0.00273, -0.00063] | -0.00128 [-0.00352, +0.00096] | -0.41 | 0.00311 | 0.0215 | 0.0645 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `schedule-free-mlp` | sgd_cosine vs adamw_cosine | 8/10 | -0.00668 [-0.01029, -0.00198] | -0.00619 [-0.01036, -0.00202] | -1.06 | 0.00580 | 0.1094 | 0.0137 | 1.0000 | no evidence of a difference at this budget (not the same claim as no difference) |
| `schedule-free-mlp` | schedule_free_sgd vs adamw_cosine | 9/10 | -0.00610 [-0.01000, -0.00169] | -0.00633 [-0.00966, -0.00299] | -1.36 | 0.00463 | 0.0215 | 0.0039 | 1.0000 | evidence of a difference (both tests agree; A is better on this metric) |
