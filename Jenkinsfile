
pipeline {
    agent {
        docker { image 'node:18.16.0-alpine' }
    }
    environment {
        IMAGE_NAME="tests"
        CONTAINER_NAME="test_run"
    }

    stages {
        stage('Checkout') {
        steps {
            checkout([$class: 'GitSCM', branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/elenkalee/BinanceFuturesQAA.git']]])
            sh 'ls -l'
        }
    }
        stage('Build') {
            steps {
                git branch: 'main', url: 'https://github.com/elenkalee/BinanceFuturesQAA.git'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --name ${CONTAINER_NAME} ${IMAGE_NAME}'
                sh 'docker cp ${CONTAINER_NAME}:/app/allure-results .'
            }
            post{
                always{
                    allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
                }
            }
        }
        stage('Clean'){
            steps{
                sh """
                echo "Cleanup"
                docker stop $CONTAINER_NAME
                docker rm $CONTAINER_NAME
                docker rmi $IMAGE_NAME
                """
            }
        }
    }
}