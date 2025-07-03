#PREREQUISITE

Create CloudSQL Postgresql instance,

Create user to access database
Create DATABASE
Grant access:

GRANT ALL PRIVILEGES ON DATABASE esbpoc to esbpoc;
ALTER DATABASE esbpoc OWNER TO esbpoc;

Set up Direct VPC Access:


#DEPLOYING
- BUILD IMAGE
gcloud builds submit --tag gcr.io/$PROJECT_ID/chatbot
- DEPLOY SERVICE
gcloud run deploy chatbot-service --image gcr.io/$PROJECT_ID/chatbot \
  --add-cloudsql-instances $CONNECTION_NAME \
  --set-env-vars INSTANCE_UNIX_SOCKET="$CONNECTION_NAME" \
  --set-env-vars INSTANCE_CONNECTION_NAME="$CONNECTION_NAME" \
  --set-env-vars DB_NAME="esbpoc" \
  --set-env-vars DB_USER="esbpoc" \
  --set-env-vars DB_PASS="esbpoc" \
  --set-env-vars DATABASE_URL="$DB_URL" \
  --set-env-vars TOOLBOX_URL="$TOOLBOX_URL" \
  --set-env-vars GOOGLE_API_KEY="$API_KEY" \
  --vpc $VPC_NAME \
  --subnet $SUBNET_NAME \
  --allow-unauthenticated

#TEST THE API!
curl -X POST -H "Content-Type: application/json" -d '{"query": "What is the peak hour?", "user_id": "user123", "company": "remboelan"}'
 url/chat

 OPTIONALLY, add session_id to request body to resume conversation