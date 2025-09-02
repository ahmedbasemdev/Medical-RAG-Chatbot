pipeline {
    agent any
    
    environment {
        REGION = 'us-central1'
        GCP_PROJECT_ID = 'byteeit-testing-project'
        REPOSITORY_NAME = 'llmops'
        IMAGE_NAME = 'rag-medical-chatbot'
        TAG = 'latest'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(
                        branches: [[name: '*/main']], 
                        extensions: [], 
                        userRemoteConfigs: [[
                            credentialsId: 'git-token', 
                            url: 'https://github.com/ahmedbasemdev/Medical-RAG-Chatbot.git'
                        ]]
                    )
                }
            }
        }
        
        stage('Build, Tag, and Push to GCP Artifact Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp-service-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        def imageFullTag = "${REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG}"
                        
                        echo "Starting GCloud authentication and Docker build..."
                        
                        // Authenticate with GCP
                        sh """
                            gcloud auth activate-service-account --key-file="\${GOOGLE_APPLICATION_CREDENTIALS}"
                            gcloud config set project ${GCP_PROJECT_ID}
                            gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
                        """
                        
                        // Build Docker image
                        sh """
                            docker build -t ${IMAGE_NAME}:${TAG} .
                        """
                        
                        // Security scan with Trivy
                        sh """
                            trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ${IMAGE_NAME}:${TAG} || true
                        """
                        
                        // Tag and push to Artifact Registry
                        sh """
                            docker tag ${IMAGE_NAME}:${TAG} ${imageFullTag}
                            docker push ${imageFullTag}
                        """
                    }
                }
            }
        }
        
        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-service-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        def imageFullTag = "${REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPOSITORY_NAME}/${IMAGE_NAME}:${TAG}"
                        def serviceName = 'medical-rag-chatbot'
                        
                        echo "Deploying to Cloud Run..."
                        
                        sh """
                            gcloud auth activate-service-account --key-file="\${GOOGLE_APPLICATION_CREDENTIALS}"
                            gcloud config set project ${GCP_PROJECT_ID}
                            
                            gcloud run deploy ${serviceName} \
                                --image=${imageFullTag} \
                                --region=${REGION} \
                                --platform=managed \
                                --allow-unauthenticated \
                                --port=5000 \
                                --memory=2Gi \
                                --cpu=2 \
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up Docker images to save space
            sh 'docker system prune -f || true'
        }
        success {
            echo "Successfully built and deployed Medical RAG Chatbot to Cloud Run"
            // Archive security scan report
            archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}