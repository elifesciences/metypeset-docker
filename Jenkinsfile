elifePipeline {
    def commit
    stage 'Checkout', {
        checkout scm
        commit = elifeGitRevision()
    }

    node('containers-jenkins-plugin') {
        stage 'Build images', {
            checkout scm
            sh "IMAGE_TAG=${commit} ./build.sh"
        }

        stage 'Smoke tests', {
            try {
                sh "IMAGE_TAG=${commit} ./run.sh &"
                sh 'docker-wait-healthy metypeset 60'
            } finally {
                sh 'docker stop metypeset'
            }
        }

        elifeMainlineOnly {
            stage 'Push images', {
                sh "IMAGE_TAG=${commit} ./push.sh"
            }
        }
    }
}
