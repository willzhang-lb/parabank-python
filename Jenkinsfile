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
        stage('Install Depemdencies') {
            steps {
                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install
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
                        pytest -v --env qa
                    '''
                }
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
