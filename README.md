:

🏥 MEDICAL RAG CHATBOT — CI/CD with Jenkins, Docker, Trivy, GCP Artifact Registry & Cloud Run
This repository contains a Medical RAG (Retrieval-Augmented Generation) Chatbot project configured with an automated CI/CD pipeline using Jenkins.

The pipeline builds a Docker image, scans it for vulnerabilities with Trivy, pushes it to Google Cloud Platform (Artifact Registry), and deploys it to Cloud Run for serverless production usage.

📦 Clone the Project
bash

Copy
git clone https://github.com/data-guru0/LLMOPS-2-TESTING-MEDICAL.git
cd LLMOPS-2-TESTING-MEDICAL
🐍 Create a Virtual Environment (Windows)
bash

Copy
python -m venv venv
venv\Scripts\activate
📥 Install Dependencies
bash

Copy
pip install -e .
✅ Prerequisites Checklist
Before proceeding, ensure you have completed the following:

 Docker Desktop installed and running
 GitHub repository pushed and up to date
 Dockerfile created and configured for the project
 Custom Jenkins Dockerfile created inside custom_jenkins for Jenkins setup
 GCP Project, Artifact Registry, and Cloud Run enabled
==> 1. 🚀 Jenkins Setup
1. Create Jenkins Setup Directory and Dockerfile
bash

Copy
mkdir custom_jenkins
cd custom_jenkins
Inside, create a Dockerfile with Jenkins + Docker-in-Docker setup.

2. Build Jenkins Docker Image
bash

Copy
docker build -t jenkins-dind .
3. Run Jenkins Container
bash

Copy
docker run -d ^
  --name jenkins-dind ^
  --privileged ^
  -p 8080:8080 ^
  -p 50000:50000 ^
  -v /var/run/docker.sock:/var/run/docker.sock ^
  -v jenkins_home:/var/jenkins_home ^
  jenkins-dind
4. Get Jenkins Initial Password
bash

Copy
docker exec jenkins-dind cat /var/jenkins_home/secrets/initialAdminPassword
Now access Jenkins at: http://localhost:8080

5. Install Python inside Jenkins
bash

Copy
docker exec -u root -it jenkins-dind bash
apt update -y
apt install -y python3 python3-pip
ln -s /usr/bin/python3 /usr/bin/python
exit
docker restart jenkins-dind
==> 2. 🔗 Jenkins Integration with GitHub
Generate a GitHub Personal Access Token (repo + admin:repo_hook access).
Add it to Jenkins → Credentials (global) → ID: github-token.
Create a Pipeline Job in Jenkins → Connect repo using Git + Token.
Add a Jenkinsfile at project root and push it:
bash

Copy
git add Jenkinsfile
git commit -m "Add Jenkinsfile for CI/CD pipeline"
git push origin main
Run pipeline → Verify Jenkins successfully clones repo.
==> 3. 🐳 Build, Scan with Trivy, and Push to GCP Artifact Registry
1. Install Trivy in Jenkins
bash

Copy
docker exec -u root -it jenkins-dind bash
apt update -y
curl -LO https://github.com/aquasecurity/trivy/releases/download/v0.62.1/trivy_0.62.1_Linux-64bit.deb
dpkg -i trivy_0.62.1_Linux-64bit.deb
exit
docker restart jenkins-dind
2. Install Google Cloud SDK
bash

Copy
docker exec -u root -it jenkins-dind bash
apt-get install -y curl unzip gnupg
curl -sSL https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud --version
exit
docker restart jenkins-dind
3. Create a Service Account in GCP
Roles needed:
Artifact Registry Writer
Cloud Run Admin
Service Account User
Download JSON key.
4. Add GCP Credentials to Jenkins
Jenkins → Manage Jenkins → Credentials → Add Secret File
Upload JSON → ID: gcp-credentials
5. Create Artifact Registry Repo
text

Copy
us-central1-docker.pkg.dev/YOUR_PROJECT_ID/medical-rag-repo
==> 4. 🚀 Deployment to GCP Cloud Run
Jenkinsfile Example
groovy

Copy
pipeline {
    agent any

    environment {
        PROJECT_ID = 'your-gcp-project-id'
        REPO_NAME  = 'medical-rag-repo'
        REGION     = 'us-central1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build, Scan, and Push to Artifact Registry') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'gcp-credentials', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh '''
                          gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                          gcloud auth configure-docker ${REGION}-docker.pkg.dev -q
                        '''
                    }

                    sh '''
                      docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/medical-rag:${BUILD_NUMBER} .
                      trivy image --exit-code 0 --severity HIGH,CRITICAL \
                        ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/medical-rag:${BUILD_NUMBER}
                      docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/medical-rag:${BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'gcp-credentials', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh '''
                          gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                          gcloud config set project ${PROJECT_ID}
                          gcloud run deploy medical-rag-service \
                            --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/medical-rag:${BUILD_NUMBER} \
                            --region=${REGION} \
                            --platform=managed \
                            --allow-unauthenticated
                        '''
                    }
                }
            }
        }
    }
}
🧪 Running the Pipeline
Go to Jenkins Dashboard → Select your pipeline → Build Now
Stages should run:
✅ Checkout → ✅ Build Docker Image → ✅ Trivy Scan → ✅ Push to GCP Artifact Registry → ✅ Deploy to Cloud Run

At the end, Jenkins will print your Cloud Run Service URL 🎉

🌐 Access the Application
After deployment, open the printed URL. That’s your production Medical RAG Chatbot running on Cloud Run 🚀

📜 License
MIT License © 2025

