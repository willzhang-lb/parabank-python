pipeline {
    agent any

    triggers {
        cron('0 14 * * *')  // Runs daily at 2:00 PM
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the Git repo (replace URL with your repo)
                git branch: 'main', url: 'https://github.com/willzhang-lb/parabank.git'
            }
        }
        stage('Install dependencies') {
            steps {
                // Use pip to install requirements
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Install Playwright browsers') {
            steps {
                // Run playwright install
                bat 'python -m playwright install'
            }
        }
        stage('Run Tests') {
            steps {
                // Run pytest
                bat 'pytest -v'
            }
        }
    }

    post {
    always {
        // Archive the Playwright report
        archiveArtifacts artifacts: 'report/playwright-report.html', fingerprint: true

        // Archive all files under trace/ folder
        archiveArtifacts artifacts: 'trace/**', fingerprint: true
        }
    }
}
