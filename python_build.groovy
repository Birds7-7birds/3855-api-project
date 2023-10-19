def call(dockerRepoName, imageName, portNum){
    pipeline {
        agent any
        parameters {
            booleanParam(defaultValue: false, description: 'Deploy the App', name: 'DEPLOY')
        }
        stages {
            stage('Build') {
                steps {
                    sh 'pip install -r requirements.txt'
                }
            }
            stage('Linting') {
                steps {
                    sh 'pylint-fail-under --fail_under 5.0 *.py'
                }
            }        
            stage('Test and Coverage') {
                steps {
                    script{
                        def rmfiles = findFiles(glob: "*reports/*.xml")
                        for (rmfile in rmfiles) {
                            sh "rm ${rmfile.path}"
                        }
                        def files = findFiles(glob: "test*.py")
                        for (file in files){
                            sh "coverage run --omit */site-packages/*,*/dist-packages/* ${file.path}"
                        }
                        sh "coverage report"
                    }
                }
                post {
                    always {
                        junit "*reports/*.xml"
                    }
                }
            }
            stage('Package') {
                when {
                    expression {env.GIT_BRANCH == 'origin/main'}
                }
                steps {
                    withCredentials([string(credentialsId: 'DockerHub', variable: 'TOKEN')]) {
                    sh "docker login -u 'hbibroida' -p '$TOKEN' docker.io"
                    sh "docker build -t ${dockerRepoName}:latest --tag hbibroida/${dockerRepoName}:${imageName} ."
                    sh "docker push hbibroida/${dockerRepoName}:${imageName}"
                }
                }
            }
            stage('Zip Artifacts'){
                steps{
                    sh "zip app.zip *.py"
                    archiveArtifacts artifacts: 'app.zip', 
                        fingerprint: true, 
                        onlyIfSuccessful: true
                }
            }
            stage('Deliver'){
                when {
                    expression { params.DEPLOY }
                }
                steps{
                    sh "docker stop ${dockerRepoName} || true && docker rm ${dockerRepoName} || true"
                    sh "docker run -d -p ${portNum}:${portNum} --name ${dockerRepoName} ${dockerRepoName}:latest"
                }
            }
        }
    }
}