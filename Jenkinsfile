elifePipeline {
    def commit
    stage 'Checkout', {
        checkout scm
        commit = elifeGitRevision()
    }

    node('containers-jenkins-plugin') {
        stage 'Build images', {
            checkout scm
            sh './build.sh'
        }

        stage 'Smoke tests', {
            try {
                sh './run.sh &'
                sh 'docker-wait-healthy metypeset 60'
            } finally {
                sh 'docker stop metypeset'
            }
        }

        elifeMainlineOnly {
            stage 'Push images', {
                sh './push.sh'
            }
        }
    }
}