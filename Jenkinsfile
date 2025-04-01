pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    bat 'git clone https://github.com/BodiaKruk/ciphers.git workspace'
                    dir('workspace') {
                    }
                }
            }
        }
        stage('Setup Python Environment') {
            steps {
                script {
                    bat 'pip install --user invoke'
                }
            }
        }
        stage('Clean') {
            steps {
                script {
                    dir('workspace') {
                        bat 'invoke clean'
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    dir('workspace') {
                        bat 'invoke test --filename=test_rsa_cipher.py'
                    }
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    dir('workspace') {
                        bat 'invoke build --filename=main.py'
                    }
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    dir('workspace') {
                        bat 'invoke run'
                    }
                }
            }
        }
    }
}
