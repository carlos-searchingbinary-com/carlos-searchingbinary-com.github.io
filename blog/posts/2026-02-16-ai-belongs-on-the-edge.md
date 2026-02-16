---
title: AI Belongs on the Edge
description: Why the future of AI is local, why Apple's Foundation Models are the right bet, and why Shortcuts might be the most underrated agent platform.
date: 2026-02-16
author: Carlos Martins
tags: ai, apple, mlx, edge computing, agents
---

There's a prevailing narrative in tech right now: AI lives in the cloud. You send your data up, a massive model processes it, and you get a response back. It works. It scales. And it's fundamentally wrong as a long-term architecture for most of what we'll want AI to do.

I believe the next major shift in AI isn't a bigger model. It's AI that runs where you are.

## The physics of latency

Every millisecond your data spends traveling to a data center and back is a millisecond your experience feels less like intelligence and more like waiting. For real-time applications like live transcription, meeting copilots, writing assistants, or accessibility tools, cloud latency isn't just annoying. It's disqualifying.

But latency is only half the story. The other half is privacy.

When your meeting audio, your documents, your screen content, and your calendar data all need to leave your device to be processed, you've created a surveillance architecture and called it a product. Users are starting to notice. Enterprises already have.

## Apple understood this first

When Apple announced Foundation Models running on-device at WWDC, much of the industry shrugged. The models were smaller. The benchmarks weren't chart-topping. The tech press wrote it off as Apple being behind.

They missed the point entirely.

Apple made a architectural decision: intelligence should be a property of the device, not a service you subscribe to. Your iPhone, your Mac, your iPad should be smart on their own. No network required. No data leaving the device. No API key. No monthly fee.

This isn't a compromise. It's a philosophy. And it's the right one.

Foundation Models on Apple Silicon deliver something no cloud API can: **zero-latency inference with complete privacy, available offline, at no marginal cost per query.** Once the model ships with the OS, every user gets AI capabilities without configuration, accounts, or internet access.

For developers, this means you can build AI features that work everywhere, always, for everyone. No backend to maintain. No API costs that scale with users. No terms of service that change overnight.

## The MLX revolution

While Apple built the foundation, something remarkable happened in the open source community. MLX, Apple's machine learning framework optimized for Apple Silicon, spawned an ecosystem that moves faster than most people realize.

The [mlx-community](https://huggingface.co/mlx-community) on Hugging Face now hosts thousands of models converted and optimized for local inference on Mac. Quantized LLMs, vision models, speech models, all running on the unified memory architecture of M-series chips with GPU acceleration.

What makes MLX special isn't just performance. It's the developer experience. The NumPy-like API, the lazy evaluation, the unified memory model that eliminates the CPU-GPU transfer bottleneck that plagues other frameworks. A 4-bit quantized 3B parameter model runs comfortably on a MacBook Air with 8GB of RAM. That's not a research demo. That's a product you can ship.

The community is doing what Apple alone couldn't: rapidly iterating on model architectures, quantization strategies, and fine-tuning approaches. Models like Qwen, Llama, Mistral, and specialized vision models like FastVLM are all available in MLX format, often within days of their original release.

Today, this stack enables applications that were impossible just two years ago. Live meeting transcription, translation, real-time insights, all processed locally on a Mac. No cloud. No data leaving the device. The MLX ecosystem made this possible.

## The unexplored frontier: Shortcuts as agent tools

Here's where it gets interesting, and where I think the industry is completely asleep.

Apple Shortcuts is, quietly, one of the most powerful agent tool platforms in existence. Think about what Shortcuts can do: it has deep integration with every native app on macOS and iOS. Calendar, Reminders, Mail, Messages, Files, Notes, Safari, Maps, HomeKit, Health, and hundreds of third-party apps through App Intents.

Now think about what an AI agent needs: the ability to take actions in the real world on behalf of the user. Read the calendar. Send a message. Create a reminder. Open a file. Toggle a smart home device. Every single one of these is already a Shortcut action.

The missing piece isn't capability. It's the bridge.

Imagine an on-device LLM that can reason about your request and compose Shortcuts dynamically. Not hardcoded automations, but an agent that understands "remind me to follow up with the client I'm meeting with tomorrow" and can:

1. Query your calendar for tomorrow's meetings
2. Extract the client's name
3. Create a reminder timed for after the meeting
4. All locally, all privately, all without any cloud service knowing who your clients are

The App Intents framework already provides structured, typed interfaces for thousands of actions. It's essentially a massive tool catalog with parameter schemas, exactly what function-calling LLMs are designed to use. Shortcuts is the runtime. The LLM is the reasoning layer. The combination is an agent platform that Apple accidentally built over the last decade.

No one is seriously building on this yet. They should be.

## The edge is the future

The cloud won't disappear. Training will stay centralized. The largest models will still need data centers. But inference, the part that touches users, will increasingly happen on the device.

The economics point this way. The physics point this way. The privacy regulations point this way. And the user experience, when you've felt truly local AI, makes cloud round-trips feel like dial-up.

Apple Silicon, Foundation Models, MLX, and Shortcuts aren't four separate stories. They're one story: the device is becoming the platform for intelligence. The companies and developers who understand this early will build the next generation of software.

The rest will still be waiting for an API response.
