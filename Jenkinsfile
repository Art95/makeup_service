pipeline {
    agent {
        docker {
            image 'abaraniuk/makeup_service:latest'
            args '--gpus all -v $WORKSPACE:/app/'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'cd /app/ && pip3 install -r requirements.txt .'
            }
        }
        stage('Test') {
            steps {
                sh 'cd /app/ && pytest'
            }
        }
    }
}