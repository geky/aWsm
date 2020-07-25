aWsm
==========

# What is aWsm?

aWsm is a compiler and runtime for compiling Web Assembly (Wasm) code into llvm bytecode, then into sandboxed binaries you can run on various platforms.
It focuses on generating very fast code (best of breed for Web Assembly), having a simple and extensible code-base, and on portability.

**What is Web Assembly?**
Wasm is a standard binary format that is *platform agnostic*, *debuggable*, *fast*, and *safe*.
Please see the [official webpage](https://webassembly.org/), and its [specification](https://webassembly.org/specs/).
Many languages (including C/C++, Rust, C#, Go, Kotlin, Swift, and more, see a more [complete list](https://webassembly.org/getting-started/developers-guide/)) compile to Wasm.
Wasm can be run in all the major browsers, thus is broadly deployed and available.

We're interested in taking Wasm out of the browser, and into all different types of computers (from servers to microcontrollers).
Wasm provides a number of benefits outside of the web including:

- *Sandboxing.*
	Regardless which language is compiled to Wasm, the Wasm runtime can execute them *safely* (including those languages with [footguns](https://en.wiktionary.org/wiki/footgun) like C).
	This uses Software Fault Isolation (SFI) -- to ensure that loads and stores are only within the sandbox-- and Control-Flow Integrity (CFI) -- only allowing the execution of code intentionally generated by the compiler -- to provide safe execution.
	Restricting SFI protects the surrounding code from faulty or malicious code, and CFI prevents a compromise from hijacking the flow of execution (see [buffer overflows](https://en.wikipedia.org/wiki/Buffer_overflow) and [ROP chains](https://en.wikipedia.org/wiki/Return-oriented_programming)).

	Sandboxing can act as a process replacement, especially on systems that don't have hardware support for processes, or where high-density is required.
- *Ubiquity.*
	Wasm is a high-level assembly, independent from any specific hardware.
	This has the potential to provide a universal specification of computation that can execute in the cloud, on the edge, or in an embedded device.

**A note on naming.**
aWsm started out as the `silverfish` compiler, the brainchild of Gregor Peach when he was a researcher in the group.
There are still quite a few lingering `silverfish` references.
Please have patience as we update those to `awsm`.

## Why aWsm?

Why would we implement a Wasm compiler and runtime.
The Web Assembly eco-system is still developing, and we see the need for a system focusing on:

- *Performance.*
	aWsm is an ahead-of-time compiler that leverages the LLVM compiler to optimize code, and target different architectural backends.
	We have evaluated the compiler on x86-64, aarch64 (Raspberry Pi), ARM Cortex-M7 (and M4), and performance on the microprocessors is within 10% of native, and within 40% on the microcontrollers.
- *Simplicity.*
	The entire code base for the compiler and runtime is relatively small.
	The compiler is <3.5K lines of Rust, and the runtime (for *all* platforms) is <5K lines of C.
	It is nearly trivial to implement different means of sandboxing memory accesses.
	We've implemented *seven* different mechanisms for this!
- *Portability.*
	Both the compiler and runtime are mostly platform-independent code, and porting to a new platform only really requires additional work if you need to tweak stack sizes (microcontrollers), or use architectural features (e.g., MPX, segmentation, etc...).

We believe that aWsm is one of the best options for ahead-of-time compilation for outside of the browser.

# Performance

Give us a little time, we'll post benchmarks here!

# Getting started!

```
aWsm 0.1.0
Gregor Peach <gregorpeach@gmail.com>

USAGE:
    awsm [FLAGS] [OPTIONS] <input>

FLAGS:
    -h, --help                           Prints help information
    -i, --inline-constant-globals        Force inlining of constant globals
    -u, --fast-unsafe-implementations    Allow unsafe instruction implementations that may be faster
        --runtime-globals                Don't generate native globals, let the runtime handle it
    -V, --version                        Prints version information

OPTIONS:
    -o, --output <output>    Output bc file
        --target <target>    Set compilation target

ARGS:
    <input>    Input wasm file
```

## Installation from Source

### Debian-based Systems

```sh
git clone https://github.com/gwsystems/awsm.git
cd awsm
./install_deb.sh
```

The compiler can now be run via `awsm`

The tests can run with

```
cd code_benches; python run.py
```

### Other Systems

1. [Install Rust](https://www.rust-lang.org/tools/install)
2. [Install LLVM](http://releases.llvm.org/download.html)
3. Link Your Clang Installation so `clang-9` and `llvm-config-9` are in your path and invokable as `clang` and `llvm-config`. For example, the following commands accomplish this using `update-alternatives` after replacing LLVM_VERSION with the version returned you installed above (In *NIX systems, this can be confirmed with `ls /usr/bin/clang*`)
```sh
LLVM_VERSION=9
sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-$LLVM_VERSION 100
sudo update-alternatives --install /usr/bin/llvm-config llvm-config /usr/bin/llvm-config-$LLVM_VERSION 100
```
4. [Install the C++ Standard Library for LLVM](https://libcxx.llvm.org/)
5. Clone and build awsm
```sh
git clone https://github.com/gwsystems/awsm.git
cd awsm
cargo build --release
```
6. The awsm binary is built at `target/release/awsm`. Copy this to the appropriaate place for your platform and add to your PATH if neccessary.

# Limitations and Assumptions

*Additional Wasm instruction support needed.*
aWsm has not focused on a complete implementation of every Wasm instruction, instead focusing on supporting the code generated by the LLVM front-end.
The code is extensible, and we've added instructions as needs-be.
Please make a PR with support for additional instructions if you need them!

*Limited support for future Wasm features.*
The features on the [Wasm roadmap](https://webassembly.org/roadmap/) are not supported.
We're quite interested in supporting as many of these feature sets as possible, and would happily accept PRs.

# Advice for Wasm Standardization

We've done quite a bit of work targeting microcontrollers (Arm Cortex-Ms), and have discovered a number of limitations of the current Wasm Specification for that domain.
We provide details in Section 7 of our [EMSOFT publication](https://www2.seas.gwu.edu/~gparmer/publications/emsoft20wasm.pdf).
We believe that some changes to the specification, or the creation of an embedded profile might be warranted.
The main limitations:

1. *Invariant page size.*
	Wasm uses 64KiB pages.
	That is far too large for embedded systems.
	aWsm uses smaller pages, while simulating the larger default pages.
	Enabling smaller pages would make Wasm's use on microcontrollers -- often with only 64KiB of memory total -- easier.
	In aWsm, the page size is configurable.
2. *Separation of read-only and read-write memory.*
	In Wasm, all data is accessed in linear memory, which provides strong sandboxing, but does not discriminate between RW and RO data.
	Microcontrollers often use [Execute in Place](https://en.wikipedia.org/wiki/Execute_in_place) (XIP) read-only memory, which allows RO data to be accessed and executed *directly from flash*.
	This is beneficial in microcontrollers with on the order of 64KiB of memory (SRAM), but around 1MIB of flash.
	Wasm does not separate RO and RW memory, preventing this optimization that is essential for density on such systems.
3. *Allow undefined behavior on Out of Bounds (OoB) accesses.*
	The specification requires any access outside of the allocated bounds of linear memory to be caught, and the sandbox terminated.
	We show in the publication that relaxing this requirement, and allowing undefined behavior on OoB accesses can significantly speed up execution, and shrink code sizes, while maintaining strong sandboxed isolation.
