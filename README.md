# ADK Trade and Position Agent

This agent accepts a natural-language prompt and uses Gemini on Vertex AI to
choose one or both private Cloud Run APIs:

- Trade Data API
- Position Data API

## Expected APIs

```http
GET /api/trades?tradeId=&accountId=&productId=&tradeDate=&limit=
GET /api/positions?accountId=&productId=&asOfDate=&limit=
```

Update `app/tools.py` if your paths or parameter names differ.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gcloud auth application-default login
cp .env.example .env
# Edit .env
uvicorn app.main:app --reload --port 8080
```

Test:

```bash
curl -X POST http://localhost:8080/prompt   -H "Content-Type: application/json"   -d '{"prompt":"Show trades for account A100 on 2026-07-22","user_id":"demo"}'
```

## GCP setup

```bash
export PROJECT_ID="your-project-id"
export REGION="asia-south1"
export AGENT_SERVICE="trade-position-agent"

gcloud config set project "$PROJECT_ID"

gcloud services enable   aiplatform.googleapis.com   run.googleapis.com   cloudbuild.googleapis.com   artifactregistry.googleapis.com   iam.googleapis.com

gcloud iam service-accounts create trade-position-agent   --display-name="Trade Position ADK Agent"

export AGENT_SA="trade-position-agent@$PROJECT_ID.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$PROJECT_ID"   --member="serviceAccount:$AGENT_SA"   --role="roles/aiplatform.user"
```

Allow the agent to invoke the two private services:

```bash
gcloud run services add-iam-policy-binding trade-data   --region="$REGION"   --member="serviceAccount:$AGENT_SA"   --role="roles/run.invoker"

gcloud run services add-iam-policy-binding position-data   --region="$REGION"   --member="serviceAccount:$AGENT_SA"   --role="roles/run.invoker"
```

Get their URLs:

```bash
export TRADE_SERVICE_URL="$(gcloud run services describe trade-data   --region="$REGION" --format='value(status.url)')"

export POSITION_SERVICE_URL="$(gcloud run services describe position-data   --region="$REGION" --format='value(status.url)')"
```

Deploy:

```bash
gcloud run deploy "$AGENT_SERVICE"   --source=.   --region="$REGION"   --service-account="$AGENT_SA"   --no-allow-unauthenticated   --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=global,AGENT_MODEL=gemini-2.5-flash,TRADE_SERVICE_URL=$TRADE_SERVICE_URL,POSITION_SERVICE_URL=$POSITION_SERVICE_URL"   --memory=1Gi   --cpu=1   --min=0   --max=3   --timeout=300
```

Grant yourself permission to call the agent:

```bash
gcloud run services add-iam-policy-binding "$AGENT_SERVICE"   --region="$REGION"   --member="user:YOUR_EMAIL"   --role="roles/run.invoker"
```

Test the deployed service:

```bash
export AGENT_URL="$(gcloud run services describe "$AGENT_SERVICE"   --region="$REGION" --format='value(status.url)')"

curl -X POST "$AGENT_URL/prompt"   -H "Authorization: Bearer $(gcloud auth print-identity-token)"   -H "Content-Type: application/json"   -d '{"prompt":"Show trades and positions for account A100 and product IBM","user_id":"demo"}'
```

## Why tool selection works

ADK sends the tool names, Python docstrings, and parameter schemas to Gemini.
Gemini uses those descriptions plus the agent instruction to decide whether to
call `get_trade_data`, `get_position_data`, or both.

## Security notes

- Keep all Cloud Run services private.
- Do not create or store service-account JSON keys.
- Give the agent service account `roles/run.invoker` only on the two data APIs.
- The data APIs must still enforce business authorization for accounts and portfolios.
- The template is read-only and limits result size.
- Replace in-memory sessions with durable session storage for production.
