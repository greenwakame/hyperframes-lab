# HyperFrames Lab

AI-assisted motion design case studies and practical knowledge built with HyperFrames and coding agents.

HyperFrames + Codexによる動画制作の事例と、実制作から得たナレッジをまとめています。

## Featured Case Study

### greenwakame Profile PV

[![Poster for the greenwakame Profile PV: a game-inspired profile scene](case-studies/greenwakame-profile-pv/assets/poster.webp)](case-studies/greenwakame-profile-pv/README.md)

**20 sec · 1920 × 1080 · 30 fps · HyperFrames · Codex · FFmpeg**

A six-scene, game-inspired GitHub profile video. Its most useful lesson came from a failed iteration: adding more generated character poses made the motion feel less continuous. The final version kept a small, stable set of sprites and made them act with movement, rotation, squash, and carefully timed UI reactions.

[Watch the delivery MP4](case-studies/greenwakame-profile-pv/media/greenwakame-profile-pv-v6-github.mp4) · [Read the case study](case-studies/greenwakame-profile-pv/README.md)

## What This Repository Contains

- [Case studies](case-studies/README.md): finished work, decisions, failures, and validation.
- [Animation design notes](docs/animation-design.md): sprite continuity and character-driven UI.
- [HyperFrames workflow](docs/workflow.md): a repeatable production and review sequence.
- [Troubleshooting](docs/troubleshooting.md): failures encountered in this production environment.
- [Reproducible examples](examples/README.md): small demonstrations without project-specific artwork.

## Production Workflow

**Design → Codex implementation → HyperFrames check → Studio preview → Human visual QA → Fix → Final render → FFprobe → Delivery**

A passing check is a technical gate. It does not prove the animation looks good. [Read why v5 failed visual QA](case-studies/greenwakame-profile-pv/ITERATIONS.md#v5-more-sprites-less-continuity).

## Knowledge

Start with the [Japanese knowledge index](docs/README.md), or go directly to [environment](docs/environment.md), [getting started](docs/getting-started.md), [validation](docs/validation-and-render.md), and [GitHub delivery](docs/github-delivery.md).

## Environment

The documented production used Apple Silicon, macOS 26.5.2, mise 2026.7.18, Node 24.18.0, pnpm 11.28.0, HyperFrames CLI 0.8.80, FFmpeg 9.0.2, and Chrome. These are recorded versions, not universal requirements. [Details](docs/environment.md).

## Future Experiments

Each future work gets its own `case-studies/<slug>/` folder, delivery media, poster, and optional focused example. [See the case index](case-studies/README.md).

## Licensing / Rights

[Example code: MIT](LICENSE-CODE) · [Documentation: CC BY 4.0](LICENSE-DOCS) · Project media: rights reserved, with publication approved by the repository owner · Third-party content: respective owners and licenses. [Scope and credits](RIGHTS-AND-CREDITS.md).
