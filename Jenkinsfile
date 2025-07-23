pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.11'
        ALLURE_VERSION = '2.27.0'
    }

    triggers {
        cron('H 14 * * *')  // Runs daily at 2:00 PM
    }

    stages {
        stage('Set up Python') {
            steps {
                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install
                '''
            }
        }

        stage('Download and Unzip Allure CLI') {
            steps {
                bat '''
                    curl -L -o allure.zip https://github.com/allure-framework/allure2/releases/download/%ALLURE_VERSION%/allure-%ALLURE_VERSION%.zip
                    powershell -Command "Expand-Archive -Force 'allure.zip' ."
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                bat '''
                    pytest -v --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat '''
                    set PATH=%CD%\\allure-%ALLURE_VERSION%\\bin;%PATH%
                    allure generate allure-results --clean -o allure-report
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
