
pipeline {
    agent any
    environment {
        IMAGE_NAME="tests"
        CONTAINER_NAME="test_run"
    }

    stages {
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