# 🤖 JARVIS AI

A local voice-controlled AI assistant built from scratch using Python.

JARVIS listens for the wake word **"Hey Jarvis"**, records your voice command, converts speech to text using Whisper, routes the request to the appropriate tool or local LLM, and responds using local text-to-speech.

The project is designed to run locally on a consumer NVIDIA GPU without relying on a cloud-hosted LLM.

---

## ✨ Features

- 🎤 Real-time microphone input
- 🔥 Wake-word detection using OpenWakeWord
- 🛑 Voice Activity Detection using WebRTC VAD
- 📝 Speech-to-Text using OpenAI Whisper
- 🧠 Local LLM using Qwen2.5-0.5B-Instruct
- 🧮 Calculator tool
- 🌐 Web search using Tavily
- 🔊 Local Text-to-Speech using Piper
- ⚡ NVIDIA CUDA GPU acceleration
- 🔁 Continuous voice interaction
- 🔐 API keys stored using environment variables

---

## 🏗️ Architecture

```text
                    🎤 MICROPHONE
                         │
                         ▼
                🔥 OPENWAKEWORD
                 "Hey Jarvis"
                         │
                         ▼
                    🛑 VAD
              Voice Activity Detection
                         │
                         ▼
                    📝 WHISPER
                  Speech → Text
                         │
                         ▼
                  🤖 JARVIS AGENT
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
        🧮 Calculator  🌐 Tavily   🧠 Qwen
             │           │           │
             └───────────┼───────────┘
                         │
                         ▼
                    🔊 PIPER TTS
                    Text → Speech
                         │
                         ▼
                  🎤 LISTEN AGAIN
