<div align="center">

# Hi, I'm Pranjal Agarwal 👋

### Full-stack engineer · Computer vision · AI agents

Final-year B.Tech CSE student at Lovely Professional University.<br>
I build software that gets deployed and keeps running — with tests, CI and a live demo you can click.

[![Portfolio](https://img.shields.io/badge/Portfolio-pranjalagarwal.me-2856c7?style=for-the-badge&logo=googlechrome&logoColor=white)](https://pranjalagarwal.me)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0yMC40NSAyMC40NWgtMy41NXYtNS41N2MwLTEuMzMtLjAzLTMuMDQtMS44NS0zLjA0LTEuODYgMC0yLjE0IDEuNDUtMi4xNCAyLjk0djUuNjdIOS4zNVY5aDMuNDF2MS41NmguMDVjLjQ4LS45IDEuNjQtMS44NSAzLjM3LTEuODUgMy42IDAgNC4yNyAyLjM3IDQuMjcgNS40NnY2LjI4ek01LjM0IDcuNDNhMi4wNiAyLjA2IDAgMSAxIDAtNC4xMiAyLjA2IDIuMDYgMCAwIDEgMCA0LjEyek03LjEyIDIwLjQ1SDMuNTZWOWgzLjU2djExLjQ1ek0yMi4yMiAwSDEuNzdDLjc5IDAgMCAuNzcgMCAxLjczdjIwLjU0QzAgMjMuMjMuNzkgMjQgMS43NyAyNGgyMC40NWMuOTggMCAxLjc4LS43NyAxLjc4LTEuNzNWMS43M0MyNCAuNzcgMjMuMiAwIDIyLjIyIDB6Ii8+PC9zdmc+)](https://www.linkedin.com/in/pranjal-agarwal01)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:agarwalpranjal2006@gmail.com)

</div>

---

## 🚀 About me

- 🎓 B.Tech in Computer Science & Engineering, Lovely Professional University (2023 – 2027)
- 🛠️ I work across the stack: React and Node.js products, Python and Java backends, computer-vision pipelines and multi-agent LLM systems
- ⚙️ I also build n8n automation pipelines for freelance clients
- 🔍 Open to **SDE, full-stack and ML roles**
- 📍 India

---

## 🏗️ Featured projects

### 🚉 [StationWatch](https://github.com/pranjal-agarwal01/Station-Facility-Monitor-Escalator-using-Computer-Vision-) — escalator fault detection from CCTV

Tells you whether an escalator is **working**, **stopped with people on it** or **idle**, using the CCTV camera that's already pointed at it. No new hardware and no training data. It combines YOLO11 person detection, dense optical flow and a hysteresis state machine, and raised **zero false fault alarms across 8 benchmark scenarios**. The demo runs entirely in your browser.

**Stack:** Python · OpenCV · YOLO11 · ONNX Runtime Web · GitHub Actions CI<br>
▶️ **[Live demo](https://stationwatch.pranjalagarwal.me)** · 💻 [Code](https://github.com/pranjal-agarwal01/Station-Facility-Monitor-Escalator-using-Computer-Vision-)

### 📦 [SupplySense AI](https://github.com/pranjal-agarwal01/SupplySenseAI---Prototype-Phase1) — demand forecasting & inventory optimisation

Forecasts material demand with five time-series models written from scratch and picks the best one per material using rolling-origin cross-validation. It then turns each forecast into safety stock, reorder points and order quantities, and runs purchase orders from request to receipt. Multi-tenant with role-based access, **30 automated tests** and CI.

**Stack:** React 19 · Node.js · Express 5 · MongoDB · Chart.js<br>
▶️ **[Live demo](https://supplysenseai.pranjalagarwal.me)** · 💻 [Code](https://github.com/pranjal-agarwal01/SupplySenseAI---Prototype-Phase1)

### ⚖️ [Debator](https://github.com/pranjal-agarwal01/Debator) — multi-agent AI debate arena

One agent argues FOR a motion, one argues AGAINST, and a judge agent scores every turn on a weighted rubric. Code, not the model, totals the scores and picks the winner, so the verdict can't be faked. Debates stream live over SSE and resume after a server restart. Tuning cut output tokens per debate from **27k to 3.8k**.

**Stack:** Python · FastAPI · PostgreSQL · Azure OpenAI · 34 tests<br>
▶️ **[Live demo](https://debator.pranjalagarwal.me)** · 💻 [Code](https://github.com/pranjal-agarwal01/Debator)

### 🔗 [Everlink](https://github.com/pranjal-agarwal01/Everlink) — links that never break

A URL shortener where you can repoint a link at any time, so the link on your résumé, a printed QR code or your bio keeps working after the destination moves. It supports custom or generated slugs, click tracking with an atomic counter, JWT auth over bcrypt-hashed passwords, and rate limiting.

**Stack:** React · Node.js · Express · MongoDB<br>
💻 [Code](https://github.com/pranjal-agarwal01/Everlink)

### 🎟️ [Event Booking API](https://github.com/pranjal-agarwal01/Event-Booking) — the last-seat race, solved

A Spring Boot API built around the bug most booking systems skip: two people booking the last seat in the same millisecond. Exactly one wins. **A 50-thread test proves it** against real PostgreSQL for both optimistic and pessimistic locking. Also includes JWT with refresh-token rotation, Flyway migrations and a Docker build.

**Stack:** Java 21 · Spring Boot 3 · PostgreSQL · Testcontainers · Docker<br>
▶️ **[Live demo](https://booking-api-rdhs.onrender.com)** <sub>(free hosting — the first visit can take a minute to wake up)</sub> · 💻 [Code](https://github.com/pranjal-agarwal01/Event-Booking)

### 📰 [AI Newsletter](https://github.com/pranjal-agarwal01/AI_Newsletter) — a personalised AI news digest, twice a day

Collects AI news from RSS blogs, Hacker News and arXiv. It removes duplicate stories, ranks what's left against a reader profile, then uses a single LLM call to pick and summarise the ~10 items that matter and emails the digest. It runs on a schedule in GitHub Actions, with no server to keep alive.

**Stack:** Python · GitHub Actions · SQLite · OpenRouter<br>
💻 [Code](https://github.com/pranjal-agarwal01/AI_Newsletter) · 🔁 [Run history](https://github.com/pranjal-agarwal01/AI_Newsletter/actions)

### 🚑 [SEVCS](https://github.com/pranjal-agarwal01/Smart-Emergency-Vehicle-Clearance-System-SEVCS-) — clearing the way for emergency vehicles

A traffic-video pipeline that detects and tracks vehicles and flags the ones blocking an emergency-vehicle lane, logging each one. The detector is YOLOv8 fine-tuned on the KITTI dataset, using a scripted KITTI-to-YOLO conversion and train/val split, and tuned with a **20-trial Optuna search**. SORT handles tracking.

**Stack:** Python · YOLOv8 · PyTorch · Optuna · OpenCV<br>
💻 [Code](https://github.com/pranjal-agarwal01/Smart-Emergency-Vehicle-Clearance-System-SEVCS-)

---

## 🧠 Tech stack

**Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)

**Frontend**

![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)

**Backend & databases**

![Node.js](https://img.shields.io/badge/Node.js-43853D?style=flat-square&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express-404D59?style=flat-square&logo=express&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=flat-square&logo=mongodb&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)

**AI / ML & computer vision**

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLO-111F68?style=flat-square&logo=yolo&logoColor=white)
![Azure OpenAI](https://img.shields.io/badge/Azure_OpenAI-0078D4?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)

**Tools & platforms**

![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=black)
![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat-square&logo=n8n&logoColor=white)

---

<div align="center">

![GitHub streak](https://streak-stats.demolab.com?user=pranjal-agarwal01&theme=tokyonight&hide_border=true)

</div>

---

## 🤝 Let's connect

Open to SDE, full-stack and ML roles, and to freelance automation work.<br>
The fastest way to reach me is [email](mailto:agarwalpranjal2006@gmail.com) or [LinkedIn](https://www.linkedin.com/in/pranjal-agarwal01). More about my work at **[pranjalagarwal.me](https://pranjalagarwal.me)**.
