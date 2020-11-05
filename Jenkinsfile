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
                    sh "apt-get install python3-venv"
                    sh "python3 -m venv myenv"
                    sh "source myenv/bin/activate"
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