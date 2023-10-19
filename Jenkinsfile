pipeline {
    agent any
    stages {
        stage('deploy') {
            steps {
                sshagent(credentials : ['XavVM3855']) {
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@ec2-52-24-139-40.us-west-2.compute.amazonaws.com 'cd ~/mystuff/3855-api-project/deployment; docker-compose down; docker image rm hbibroida/receiver:receiverapp; docker image rm hbibroida/storage:storageapp; docker image rm hbibroida/processing_service:processing_serviceapp; docker image rm hbibroida/audit:auditapp'"
                    // sh "ssh -o StrictHostKeyChecking=no ubuntu@ec2-52-24-139-40.us-west-2.compute.amazonaws.com 'docker pull hbibroida/receiver:receiverapp; docker pull hbibroida/storage:storageapp; docker pull hbibroida/audit:auditapp; docker pull hbibroida/processing_service:processing_serviceapp'"
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@ec2-52-24-139-40.us-west-2.compute.amazonaws.com 'cd ~/mystuff/3855-api-project/deployment; docker-compose up -d'"
                }
            }
        }
    }
}