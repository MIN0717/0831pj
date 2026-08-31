pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Environment') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'back-env-file',
                        variable: 'ENV_FILE'
                    )
                ]) {
                    sh '''
                        cp "$ENV_FILE" back/.env
                    '''
                }
            }
        }

        stage('Frontend Install') {
            steps {
                dir('front') {
                    sh '''
                        npm ci
                    '''
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('front') {
                    sh '''
                        npm run build
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker compose build
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker compose up -d
                '''
            }
        }

        stage('Check Containers') {
            steps {
                sh '''
                    docker compose ps
                '''
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                    rm -f back/.env
                    docker image prune -f
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment Success'
        }

        failure {
            echo 'Deployment Failed'
        }
    }
}