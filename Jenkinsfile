pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    bat 'if exist workspace rmdir /s /q workspace'
                    bat 'git clone https://github.com/BodiaKruk/ciphers.git workspace'
                    dir('workspace') {
                    }
                }
            }
        }
        stage('Setup Python Environment') {
            steps {
                script {
                    bat 'pip install invoke'
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
                        bat 'invoke test'
                    }
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    dir('workspace') {
                        bat 'invoke build'
                    }
                }
            }
        }
    }
}
