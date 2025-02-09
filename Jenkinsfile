pipeline {
    agent {
        node {
            label 'zOS_pyRACF'
        }
    }

    options {
        ansiColor('css')
    }

    stages {
        stage('Install Dependencies') {
            steps {
                // Uninstall pyRACF to clean environment.
                // Install wheel to build and publish pyRACF as a python wheel.
                sh """
                    python3 --version
                    python3 -m pip uninstall pyracf -y
                    python3 -m pip install -r requirements.txt
                    python3 -m pip install -r requirements-development.txt
                    python3 -m pip install wheel>=0.41.0
                """
            }
        }
        stage('Unit Test') {
            steps {
                sh """
                    flake8 .
                    pylint --recursive=y .
                    coverage run tests/test_runner.py
                    coverage report -m
                """
            }
        }
        stage('Function Test') {
            steps {
                sh """
                    python3 setup.py install --user
                    cd tests/function_test
                    python3 function_test.py
                """
            }
        }
        stage('Publish') {
            when { tag "*" }
            steps {
                sh "python3 setup.py bdist_wheel upload -r test"
            }
        }
    }
}
