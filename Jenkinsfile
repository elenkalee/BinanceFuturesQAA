
pipeline {
    agent any
//     environment {
//         PATH = "/hot/new/bin:$PATH"
//         IMAGE_NAME="tests"
//         CONTAINER_NAME="test_run"
//     }

    stages {
//         stage('Checkout') {
//         steps {
//             checkout([$class: 'GitSCM', branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/elenkalee/BinanceFuturesQAA.git']]])
//             sh 'ls -l'
//         }
//     }
        stage('Build') {
//             steps {
//                 echo "PATH is: $PATH"
//                 git branch: 'main', url: 'https://github.com/elenkalee/BinanceFuturesQAA.git'
//                 sh 'docker build -t $IMAGE_NAME .'
//             }
                steps {
                    sh 'chmod +x setup.sh'
                    sh './install.sh'
            }
        }
        stage('Test') {
//             steps {
//                 sh 'docker run --name ${CONTAINER_NAME} ${IMAGE_NAME}'
//                 sh 'docker cp ${CONTAINER_NAME}:/app/allure-results .'
//             }
            steps {
                sh './venv/bin/pytest'
            }
            post{
                always{
                    allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
                }
            }
        }
//         stage('Clean'){
//             steps{
//                 sh """
//                 echo "Cleanup"
//                 docker stop $CONTAINER_NAME
//                 docker rm $CONTAINER_NAME
//                 docker rmi $IMAGE_NAME
//                 """
//             }
//         }
    }
}