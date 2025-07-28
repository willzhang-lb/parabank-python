pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.53.0-noble'
        }
    }

    environment {
        ALLURE_HOME = "${WORKSPACE}/allure-${ALLURE_VERSION}"
        PATH = "${env.PATH}:${env.ALLURE_HOME}/bin"
        ALLURE_VERSION = '2.27.0'
    }

    triggers {
        cron('H 14 * * *')  // Runs daily at 2:00 PM
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Download and Unzip Allure CLI') {
            steps {
                bat '''
                    apt-get update
                    apt-get install -y wget tar openjdk-11-jre
                    wget https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz
                    tar -zxvf allure-${ALLURE_VERSION}.tgz
                '''
            }
        }

        stage('Clean Trace Folder') {
            steps {
                bat 'if exist trace (rmdir /s /q trace)'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat '''
                        pytest -v --alluredir=allure-results || true
                    '''
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat '''
                    ${ALLURE_HOME}/bin/allure generate allure-results --clean -o allure-report
                '''
            }
        }

        stage('Archive Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }

        stage('Archive Playwright Traces') {
            when {
                expression { return fileExists('trace') }
            }
            steps {
                archiveArtifacts artifacts: 'trace/**', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Allure and trace artifacts are archived."
        }
    }
}
