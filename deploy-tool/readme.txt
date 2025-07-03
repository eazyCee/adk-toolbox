https://googleapis.github.io/genai-toolbox/how-to/deploy_toolbox/

Follow the instructions from the link above.

During this step, add the project_id environment variable

gcloud run deploy toolbox \
    --image us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest \
    --service-account toolbox-identity \
    --region us-central1 \
    --set-secrets "/app/tools.yaml=tools:latest" \
    --args="--tools-file=/app/tools.yaml","--address=0.0.0.0","--port=8080"
    --set-env-vars "PROJECT_ID=$PROJECT_ID"