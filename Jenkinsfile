pipeline {
    agent {
        docker {
            image 'abaraniuk/makeup_service:latest'
            args '-u root:root --name makeup_service_jenkins --gpus all -v $WORKSPACE:/app/'
        }
    }
    stages {
        stage('Build') {
            steps {
                    sh "pip3 install -r requirements.txt ."
            }
        }
        stage('Test') {
            steps {
                    sh 'pytest'
            }
        }
    }
    post {
        cleanup {
            cleanWs()
        }
    }
}