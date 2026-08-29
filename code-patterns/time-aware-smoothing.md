# Time-aware smoothing

Frame-rate independent exponential convergence is useful for camera and presentation smoothing:

```text
function exp_smooth(current, target, sharpness, delta_seconds):
    t = 1 - exp(-sharpness * delta_seconds)
    return lerp(current, target, t)
```

For designer-friendly half-life:

```text
function smooth_half_life(current, target, half_life, dt):
    if half_life <= 0: return target
    remaining = pow(0.5, dt / half_life)
    return target + (current - target) * remaining
```

Use appropriate interpolation for rotations. Clamp pathological `dt`, test across frame rates and do not apply presentation smoothing inside authoritative collision rules.
