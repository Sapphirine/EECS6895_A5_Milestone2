import cv2.cv as cv

class motionkalm(object):
    

    def __init__(self, processNoiseCovariance=1e-4, measurementNoiseCovariance=1e-1, errorCovariancePost=0.1):
        

        self.kalman = cv.CreateKalman(4, 2, 0)
        self.kalman_state = cv.CreateMat(4, 1, cv.CV_32FC1)
        self.kalman_process_noise = cv.CreateMat(4, 1, cv.CV_32FC1)
        self.kalman_measurement = cv.CreateMat(2, 1, cv.CV_32FC1)

        for j in range(4):
            for k in range(4):
                self.kalman.transition_matrix[j,k] = 0
            self.kalman.transition_matrix[j,j] = 1

        cv.SetIdentity(self.kalman.measurement_matrix)

        cv.SetIdentity(self.kalman.process_noise_cov, cv.RealScalar(processNoiseCovariance))
        cv.SetIdentity(self.kalman.measurement_noise_cov, cv.RealScalar(measurementNoiseCovariance))
        cv.SetIdentity(self.kalman.error_cov_post, cv.RealScalar(errorCovariancePost))

        self.predicted = None
        self.esitmated = None

    def update(self, x, y):

        self.kalman_measurement[0, 0] = x
        self.kalman_measurement[1, 0] = y

        # self.predicted = cv.KalmanPredict(self.kalman)
        # self.corrected = cv.KalmanCorrect(self.kalman, self.kalman_measurement)

    def getEstimate(self):
        
        return self.corrected[0,0], self.corrected[1,0]

    def getPrediction(self):
        self.predicted = cv.KalmanPredict(self.kalman)
        

        return self.predicted[0,0], self.predicted[1,0]

    def ComputeMotion(self,x,y):
        # For the whole pipeline
        # Firstly create the kalman filter.
        # Getting several frames with data for the previous state x,y
        # Set the Kalman filter.
        # Change the kalman measurements.
        # Do prediction using kamlan filter.
        # Do the correction of it.
        # Update the coefficients for the state.
        self.__init__()
        predictx, predicty = self.getPrediction()
        self.update(x,y)
        correctx,correcty = self.getEstimate()

        return correctx, correcty








