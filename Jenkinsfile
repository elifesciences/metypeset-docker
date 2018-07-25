elifePipeline {
    def commit
    stage 'Checkout', {
        checkout scm
        commit = elifeGitRevision()
    }

    node('containers-jenkins-plugin') {
        stage 'Build images', {
            checkout scm
            sh "IMAGE_TAG=${commit} docker-compose build"
        }

        stage 'Smoke tests', {
            try {
                sh "IMAGE_TAG=${commit} docker-compose up &"
                sh 'docker-wait-healthy metypeset_metypeset_1 60'
            } finally {
                sh 'docker-compose down'
            }
        }

        elifeMainlineOnly {
            stage 'Push images', {
                sh "IMAGE_TAG=${commit} ./push.sh"
            }
        }
    }
}
