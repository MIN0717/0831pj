pipeline {
    agent any


    environment {
        OPENAI_API_KEY = credentials(
            'openai-api-key'
        )

        AWS_ACCESS_KEY_ID = credentials(
            'aws-access-key-id'
        )

        AWS_SECRET_ACCESS_KEY = credentials(
            'aws-secret-access-key'
        )

        AWS_S3_BUCKET_NAME = credentials(
            'aws-s3-bucket-name'
        )

        AWS_REGION = 'ap-northeast-2'
    }


    stages {

        stage('Checkout') {
            steps {
                checkout scm
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


        stage('Create Environment') {
            steps {
                sh '''
                    cat > .env <<EOF
OPENAI_API_KEY=${OPENAI_API_KEY}
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
AWS_REGION=${AWS_REGION}
AWS_S3_BUCKET_NAME=${AWS_S3_BUCKET_NAME}
EOF
                '''
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


        always {
            sh '''
                rm -f .env
            '''
        }
    }
}