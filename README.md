---

##🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /chat | Send a message |
| GET | /health | API health check |
| GET | /history/{session_id} | Get chat history |
| DELETE | /history/{session_id} | Clear chat history |
| GET | /stats | Token usage stats |
| GET | /logs | Recent request logs |
| GET | /docs | Interactive API docs |

---

## 📊 How Hallucination Detection Works

| Risk | Meaning |
|---|---|
| 🟢 LOW | Answer grounded in knowledge base |
| 🟡 MEDIUM | Partially grounded — verify if important |
| 🔴 HIGH | May be unreliable — please verify |

---

## 🔮 Future Improvements

- [ ] Upgrade memory to Redis
- [ ] Add PDF document upload
- [ ] Add user authentication
- [ ] Deploy on Render / Railway
- [ ] Add more hallucination checks
- [ ] Multi-language support

---

## 📄 License

MIT License — free to use and modify.

---

Built with ❤️ by Rajesh Kumar Mahto
