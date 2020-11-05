pipeline {
    agent {
        docker {
            image 'abaraniuk/makeup_service:latest'
            args '--name makeup_service_jenkins --gpus all -v $WORKSPACE:/app/'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'ls /'
            }
        }
        stage('Test') {
            steps {
                sh 'cd /app/ && pytest'
            }
        }
    }
}