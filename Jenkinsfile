pipeline {
    agent any

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'git-token', url: 'https://github.com/ahmedbasemdev/Medical-RAG-Chatbot.git']])
                }
            }
        }
        stage('Build, Tag, and Push to GCP Artifact Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp-service-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        def gcpProjectId = 'rag-medical-chatbot'
                        def region = 'us-central1'
                        def repositoryName = 'llmops'
                        def imageName = 'rag-medical-chatbot'
                        def tag = "latest"
                        def imageFullTag = "${region}-docker.pkg.dev/${gcpProjectId}/${repositoryName}/${imageName}:${tag}"

                        sh """
                        # Install gcloud CLI if not present
                        if ! command -v gcloud &> /dev/null; then
                            echo "Installing gcloud CLI..."
                            curl -sSL https://sdk.cloud.google.com | bash
                            export PATH=\$PATH:/var/jenkins_home/google-cloud-sdk/bin
                        fi
                        
                        # Use gcloud
                        export PATH=\$PATH:/var/jenkins_home/google-cloud-sdk/bin
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT_ID}
                        gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
                        
                        # Build and push Docker image
                        docker build -t ${IMAGE_NAME}:${tag} .
                        docker tag ${IMAGE_NAME}:${tag} ${imageFullTag}
                        docker push ${imageFullTag}
                        """

                    }
                }
            }
        }
    }
    post {
        success {
            echo "Successfully built and pushed image "
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }

}