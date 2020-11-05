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
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh "pip3 install -r requirements.txt --user ."
                }
            }
        }
        stage('Test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pytest'
                }
            }
        }
    }
    post {
        cleanup {
            cleanWs()
        }
    }
}