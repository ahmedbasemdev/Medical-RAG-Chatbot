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

        
    }
}