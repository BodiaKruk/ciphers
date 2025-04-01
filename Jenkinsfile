pipeline {
    agent any
    stages {
        stage('Clean') {
            steps {
                script {
                    sh 'invoke clean'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    sh 'invoke test'
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    sh 'invoke build'
                }
            }
        }
        stage('Run') {
            steps {
                script {
                    sh 'invoke run'
                }
            }
        }
    }
}
