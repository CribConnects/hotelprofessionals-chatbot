# Chatbot-Hotelprofessionals
Chatbot for hotelprofessionals. Digital assistant answer questions of clients on the site.

## Deploying to Railway
1. Push this project to a Git provider (GitHub/GitLab) and create a new Railway project from that repository.
2. When Railway detects the Python project it will install packages from requirements.txt and use the Procfile (web: bash start.sh) to launch uvicorn.
3. In the Railway dashboard add an environment variable named PPLX_API_KEY containing your Perplexity API key.
4. Redeploy the service. Once the build finishes the FastAPI app will be available on the Railway-generated URL.

### Useful notes
- De backend belt rechtstreeks naar de Perplexity REST API, dus er is geen aparte SDK-installatie nodig.
- The start.sh script expects the PORT variable that Railway injects automatically.
