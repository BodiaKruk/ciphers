pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    sh 'git clone https://github.com/BodiaKruk/ciphers.git workspace'
                    dir('workspace') {
                        sh 'ls -la'  // Переконуємося, що файли завантажені
                    }
                }
            }
        }
        stage('Setup Python Environment') {
            steps {
                script {
                    sh 'pip install --user invoke'
                }
            }
        }
        stage('Clean') {
            steps {
                script {
                    dir('workspace') {
                        sh 'invoke clean'
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    dir('workspace') {
                        sh 'invoke test --filename=test_rsa_cipher.py'
                    }
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    dir('workspace') {
                        sh 'invoke build --filename=main.py'
                    }
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    dir('workspace') {
                        sh 'invoke run'
                    }
                }
            }
        }
    }
}
