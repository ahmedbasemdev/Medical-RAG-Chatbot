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
                        def gcpProjectId = 'byteeit-testing-project'
                        def region = 'us-central1'
                        def repositoryName = 'llmops'
                        def imageName = 'rag-medical-chatbot'
                        def tag = "latest"
                        def imageFullTag = "${region}-docker.pkg.dev/${gcpProjectId}/${repositoryName}/${imageName}:${tag}"

                        sh '''
    echo "Starting GCloud authentication and Docker push..."
    gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
    gcloud config set project ''' + gcpProjectId + '''
    
    gcloud auth configure-docker ''' + region + '''-docker.pkg.dev --quiet
    
    docker build -t ''' + imageName + ''':''' + tag + ''' .
    trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ''' + imageName + ''':''' + tag + ''' || true
    docker tag ''' + imageName + ''':''' + tag + ''' ''' + imageFullTag + '''
    docker push ''' + imageFullTag + '''
'''
                    }
                }
            }
        }
    }
    post {
        success {
            echo "Successfully built and pushed image with tag"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}