#!/usr/bin/env python3

import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt
import numpy as np
import sys

path = sys.argv[1]

# matching style in other SVGs
plt.rcParams['font.family'] = 'Ubuntu'
plt.rcParams['font.size'] = 12
fig, ax = plt.subplots(figsize=(1.5*6, 1.5*3.5))

# I tried to base these off of valid benchmarks. Unfortunately
# benchmark results for the runtimes are fairly sparse, perhaps because of
# the newness of Wasm.
#
# These should be taken with a HEAVY grain of salt, as they are benchmarks
# done by different teams, different benchmarks, different architectures. They
# should not be used by anything other than getting a rough idea of the Wasm
# backend ecosystem.
#
# I also couldn't find a JIT-ed backend with benchmarks, which is unfortunate,
# so here I'm just using nodejs results.

# aWsm is ~1.7x slower than native, with cond (branching load checks)
# (our paper)
# https://www2.seas.gwu.edu/~gparmer/publications/emsoft20wasm.pdf

# Cranelift is ~1.2x faster to compile than LLVM -O3
# LLVM -O3 is ~9.4x faster than Cranelift 
# https://github.com/bjorn3/rustc_codegen_cranelift/issues/133#issuecomment-439475172

# wamr is ~8x slower than wasm3
# wasm3 is ~4x slower than wasmtime w/ cranelift
# wasm3 is ~11.1x slower than native
# https://github.com/wasm3/wasm3/blob/fcad718a29866e5b285a8db288c58f1a72a4616d/docs/Performance.md

# WAMR has posted additional numbers, but I'm not sure how to parse them
# I'm going to leave out WAMR for now
# https://github.com/bytecodealliance/wasm-micro-runtime/wiki/Performance

# nodejs is ~2.7x slower than native
# https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/node-gpp.html

# nodejs is ~1.3x faster than wasm3
# https://github.com/wasm3/wasm3/blob/fcad718a29866e5b285a8db288c58f1a72a4616d/docs/Performance.md

name, x, y = "aWsm\n(LLVM)", 1.7, 4
ax.annotate(name, (x, y), ha='center', va='center')
#ax.scatter(x, y, s=6000, c='#ea9999', lw=2)
e = matplotlib.patches.Ellipse((x, y), height=1, width=1.75,
    facecolor='#ea9999')
e.set_sketch_params(1, 100, 3)
ax.add_artist(e)

name, x, y = "Wasmtime\n(Cranelift)", 2.8, 3
ax.annotate(name, (x, y), ha='center', va='center')
#ax.scatter(x, y, s=6000, c='#b4a7d6', lw=2)
e = matplotlib.patches.Ellipse((x, y), height=1, width=1.75,
    facecolor='#b4a7d6')
e.set_sketch_params(1, 100, 2)
ax.add_artist(e)

#name, x, y = "V8", (2.7 + 8.5)/2, 1.5
#ax.annotate(name, (x, y), ha='center', va='center')
#ax.scatter(x, y, s=6000, c='#b4a7d6', lw=2)
#
#name, x, y = "wasm3", 11.1, 1
#ax.annotate(name, (x, y), ha='center', va='center')
#ax.scatter(x, y, s=6000, c='#b4a7d6', lw=2)

# note the common runtime modes
ax.annotate("AoT compilers", ((1.7+2.8)/2+0.1, 4.75), ha='center', va='center')
#ax.annotate("JIT compilers", ((2.7 + 8.5)/2, 2.5), ha='center', va='center')
#ax.annotate("Interpreters", (11.1, 2), ha='center', va='center')

# more general categories
ax.annotate("JIT compilers", ((2.7 + 8.5)/2, 1.5), ha='center', va='center')
e = matplotlib.patches.Ellipse(((2.7 + 8.5)/2, 1.5), height=1, width=3,
    facecolor='#b4a7d6')
e.set_sketch_params(1, 100, 3)
ax.add_artist(e)
ax.annotate("Interpreters", (11, 1), ha='center', va='center')
e = matplotlib.patches.Ellipse((11, 1), height=1, width=3,
    facecolor='#b4a7d6')
e.set_sketch_params(1, 100, 2)
ax.add_artist(e)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_lw(2)
ax.spines['left'].set_lw(2)
ax.plot(1, 0.5, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
ax.set_title('Performance tradeoffs for WebAssembly implementations')
ax.set_yticks([])
ax.set_ylim(0.5, 6)
ax.set_ylabel('Startup cost')
ax.set_xticks([])
ax.set_xlim(0, 12.5)
ax.set_xlabel('Runtime cost')

fig.tight_layout()
plt.savefig(path)

