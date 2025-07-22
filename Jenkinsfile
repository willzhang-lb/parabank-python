pipeline {
    agent any

    triggers {
        cron('0 14 * * *')  // Runs daily at 2:00 PM
    }

    environment {
        PYTHON_VERSION = '3.11'
        ALLURE_VERSION = '2.27.0'
    }
    options {
        timeout(time: 60, unit: 'MINUTES')
    }
    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                sh '''
                    sudo apt update
                    sudo apt install -y python3 python3-pip python3-venv wget tar unzip curl
                    python3 -m venv venv
                    source venv/bin/activate
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install
                '''
            }
        }

        stage('Install Allure CLI') {
            steps {
                sh '''
                    wget https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz
                    tar -zxvf allure-${ALLURE_VERSION}.tgz
                    sudo mv allure-${ALLURE_VERSION} /opt/allure
                    sudo ln -sf /opt/allure/bin/allure /usr/bin/allure
                    allure --version
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest -v --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                    allure generate allure-results --clean -o allure-report
                '''
            }
        }

        stage('Archive Allure Report') {
            steps {
                archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
            }
        }

        stage('Archive Playwright Traces') {
            when {
                expression { fileExists('trace') }
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
