import numpy as np  
from scipy.stats import median_abs_deviation
from statsmodels import robust
from scipy.special import zeta
import math

class rnbwavelet:

    def __init__(self):
        print("rnb-wavelet initialized")


    def fractsplineautocorr(self,alpha, nu):
        """
        Frequency domain computation of the autocorrelation filter A(exp(2*i*Pi*nu)) 
        of a fractional spline of degree alpha (and dummy shift tau).  It uses an acceleration 
        technique to improve the convergence of the infinite sum by 4 orders (see Ref. [1]).
        
        References:
        ----------
        [1] Unser, M. & Blu, T.,"Fractional Splines and Wavelets", SIAM Review, Vol. 42 (1), pp. 43-67, March 2000. 
        [2] Blu, T. & Unser, M.,"The Fractional Spline Wavelet Transform: Definition and Implementation", Proc. IEEE International 
            Conference on Acoustics, Speech, and Signal Processing (ICASSP'00), Istanbul, Turkey, Vol. {I}, pp. 512-515, June 5--9, 2000.  
        [3] Blu, T. & Unser, M.,"A Complete Family of Scaling Functions: The $($-Fractional Splines", Proc. IEEE International 
            Conference on Acoustics, Speech, and Signal Processing (ICASSP'03), Hong Kong, China, Vol. {VI}, pp. 421-424, April 6--10, 2003.

        Author:
        -------
        Thierry Blu
        The Chinese University of Hong Kong.
        This software is downloadable at http://www.ee.cuhk.edu.hk/~tblu/demos/
        """
        N = 100
        if alpha <= -0.5:
            print('The autocorrelation of the fractional splines exists only for degrees strictly larger than -0.5!')
            A = []
            return A

        S = np.zeros_like(nu)

        err = []
        err0 = []
        for n in range(-N, N+1):
            S = S + np.abs(np.sinc(nu+n))**(2*alpha+2)
            U = 2/(2*alpha+1)/N**(2*alpha+1)
            U = U - 1/N**(2*alpha+2)
            U = U + (alpha+1)*(1/3+2*nu**2)/N**(2*alpha+3)
            U = U - (alpha+1)*(2*alpha+3)*nu**2/N**(2*alpha+4)
            U = U*np.abs(np.sin(np.pi*nu)/np.pi)**(2*alpha+2)
            A = S + U
            A = A.astype(float)

        return A


    def FFTfractsplinefilters(self,M, alpha, tau, typ):
        """"
        Provides the frequency response of the low- and high-pass filters that 
        generate the orthonormal or semi-orthonormal (B-spline or dual) fractional 
        splines of degree alpha, shift tau, and a specified type.

        Parameters:
        ----------
        M : Size of the input signal, equal to the length of FFT filters (must be 2^N).
        alpha : Degree of the fractional splines, must be greater than -0.5.
        tau : Shift or asymmetry of the fractional splines. It is recommended to restrict 
            this value to the interval [-1/2, +1/2]. Particular cases:
                - tau=0: Symmetric splines.
                - tau=±1/2: Maximally dissymmetric splines.
                - tau=(alpha+1)/2: Causal splines.
        filter_type : Type of B-splines:
                - 'ortho' (orthonormal, default)
                - 'bspline' (B-spline)
                - 'dual' (dual, flipped version of 'bspline').

        Returns:
        -------
        FFTanalysisfilters : ndarray
            Array of FFT filters [lowpassfilter, highpassfilter].
        FFTsynthesisfilters : ndarray
            Array of FFT filters [lowpassfilter, highpassfilter].

        References:
        ----------
        [1] Unser, M. & Blu, T. "Fractional Splines and Wavelets", SIAM Review, Vol. 42 (1), pp. 43-67, March 2000.
        [2] Blu, T. & Unser, M. "The Fractional Spline Wavelet Transform: Definition and Implementation", 
            Proc. IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP'00), 
            Istanbul, Turkey, Vol. I, pp. 512-515, June 5-9, 2000.
        [3] Blu, T. & Unser, M. "A Complete Family of Scaling Functions: The Fractional Splines", 
            Proc. IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP'03), 
            Hong Kong, China, Vol. VI, pp. 421-424, April 6-10, 2003.

        Author:
        -------
        Thierry Blu
        The Chinese University of Hong Kong.
        This software is downloadable at http://www.ee.cuhk.edu.hk/~tblu/demos/
        """
        u = (alpha/2 - tau)
        v = (alpha/2 + tau)
        if alpha <= -0.5:
            print('The autocorrelation of the fractional splines exists only\nfor degrees strictly larger than -0.5!')
            return None
        if M != 2**np.round(np.log2(M)):
            print('\nThe size of the FFT must be a power of two!\n')
            return None

        nu = np.arange(0, 1, 1/M)
        A = self.fractsplineautocorr(alpha, nu)

        A2 = np.concatenate((A, A))
        A2 =A2[::2]  # A2(z) = A(z^2)

        if typ[0] == 'o' or typ[0] == 'O':
            # orthonormal spline filters
            lowa = np.sqrt(2) * ((1 + np.exp(2j * np.pi * nu)) / 2) ** (u + 0.5) * ((1 + np.exp(-2j * np.pi * nu)) / 2) ** (v + 0.5) * np.sqrt(A / A2)

            higha = np.exp(2j * np.pi * nu) * lowa
            higha = np.concatenate((np.conj(higha[M//2:M]), np.conj(higha[0:M//2])))

            lows = lowa
            highs = higha

            FFTanalysisfilters = np.vstack((lowa, higha))
            FFTsynthesisfilters = np.vstack((lows, highs))

            return FFTanalysisfilters,FFTsynthesisfilters
        else:
            # semi-orthonormal spline filters
            lowa = np.sqrt(2) * ((1 + np.exp(2j * np.pi * nu)) / 2) ** (u + 0.5) * ((1 + np.exp(-2j * np.pi * nu)) / 2) ** (v + 0.5)

            higha = np.exp(2j * np.pi * nu) * lowa * A
            higha = np.concatenate((higha[M // 2:], higha[:M // 2][::-1].conjugate()))

            lows = lowa * A / A2
            highs = higha / (A2 * np.concatenate((A[M // 2:], A[:M // 2])))

            if typ[0] == 'd' or typ[0] == 'D':
                # dual spline wavelets
                FFTanalysisfilters = np.vstack((lowa, higha))
                FFTsynthesisfilters = np.vstack((lows, highs))
            else:
                # B-spline wavelets
                if typ[0] == 'b' or typ[0] == 'B':
                    FFTsynthesisfilters = np.vstack((lowa, higha))
                    FFTanalysisfilters = np.vstack((lows, highs))
                else:
                    raise ValueError(f"'{typ}' is an unknown filter type!")


    def FFTwaveletsynthesis1D(self,w, FFTsynthesisfilters, J):
        """"
        FFT-based implementation of the inverse wavelet transform (see ref. [2]). It computes the 
        inverse wavelet transform of "w" using a Fourier method. This function is the inverse of 
        FFTWAVELETANALYSIS. It uses periodic boundary conditions. The length of the signal must be 
        a power of two and the frequency responses of the filters are specified in FFTsynthesisfilters.
        
        The wavelet coefficient vector has the following fine-to-coarse 
     	organization: w=[wav1 wav2 ...  wavJ lowJ]

        Parameters:
        ----------
        w : wavelet transform, of size 2^N=length of FFTsynthesisfilters
        J : depth of the decomposition, i.e., J wavelet bands + 1 lowpass
        FFTsynthesisfilters = [lowpassfilter;highpassfilter]
        
        Returns:
        -------
        x : signal of size 2^N

        References:
        ----------
        [1] Unser, M. & Blu, T.,"Fractional Splines and Wavelets", SIAM Review, Vol. 42 (1), pp. 43-67, March 2000. 
        [2] Blu, T. & Unser, M.,"The Fractional Spline Wavelet Transform: Definition and Implementation", Proc. IEEE International 
           Conference on Acoustics, Speech, and Signal Processing (ICASSP'00), Istanbul, Turkey, Vol. {I}, pp. 512-515, June 5--9, 2000.  
        [3] Blu, T. & Unser, M.,"A Complete Family of Scaling Functions: The $($-Fractional Splines", Proc. IEEE International 
            Conference on Acoustics, Speech, and Signal Processing (ICASSP'03), Hong Kong, China, Vol. {VI}, pp. 421-424, April 6--10, 2003. 

        Author:
        -------
        Thierry Blu
        The Chinese University of Hong Kong.
        This software is downloadable at http://www.ee.cuhk.edu.hk/~tblu/demos/
        """
        M = len(w)

        if FFTsynthesisfilters.ndim == 1:
            num_cols = len(FFTsynthesisfilters)
        elif FFTsynthesisfilters.ndim == 2:
            num_rows, num_cols = FFTsynthesisfilters.shape

        # check if M is a power of 2
        if M != 2**round(np.log2(M)):
            print('The size of the input signal must be a power of two!')
            return None

        # check if the size of the filters matches the size of the input signal
        if num_cols != M:
            #print('allo1')
            print('The size of the input signal and of the filters must match!')
            return None

        # Reconstruction of the signal from its bandpass components
        G = np.conj(FFTsynthesisfilters[0,:])
        H = np.conj(FFTsynthesisfilters[1,:])

        M = int(M/2**J)
        y = w[-M:]
        w = w[:-M]
        Y = np.fft.fft(y,M)

        for j in range(J,0,-1):
            z = w[-M:]
            w = w[:-M]
            Z = np.fft.fft(z,M)
            M = 2*M
            H1 = H[::2**(j-1)]
            G1 = G[::2**(j-1)]
            Y0 = G1[:M//2]*Y + H1[:M//2]*Z
            Y1 = G1[M//2:]*Y + H1[M//2:]*Z
            Y = np.concatenate((Y0,Y1))

        x = np.real(np.fft.ifft(Y,M))

        return x        


    def FFTwaveletanalysis1D(self,x,FFTanalysisfilters,J):
        """"
        FFT-based implementation of the wavelet transform (see ref. [2]). It computes the wavelet transform of a 
        signal "x" using a Fourier method. It uses periodic boundary conditions.  The length of the signal 
        must be a power of two and the frequency responses of the filters is specified in FFTanalysisfilters.
        
        Parameters:
        ----------
        x : input signal, of size 2^N=length of FFTanalysisfilters
        J : depth of the decomposition, i.e., J wavelet bands (wav1 to wavJ) 
            + 1 lowpass (lowJ) 
        FFTanalysisfilters : [lowpassfilter;highpassfilter]
        
        Returns:
        -------
        d : [wav1 wav2 ...  wavJ lowJ]: vector of pooled wavelet coefficients, size 2^N

        References:
        ----------
 	    [1] Unser, M. & Blu, T.,"Fractional Splines and Wavelets", SIAM Review, Vol. 42 (1), pp. 43-67, March 2000. 
 	    [2] Blu, T. & Unser, M.,"The Fractional Spline Wavelet Transform: Definition and Implementation", Proc. IEEE International 
            Conference on Acoustics, Speech, and Signal Processing (ICASSP'00), Istanbul, Turkey, Vol. {I}, pp. 512-515, June 5--9, 2000.  
        [3] Blu, T. & Unser, M.,"A Complete Family of Scaling Functions: The $($-Fractional Splines", Proc. IEEE International 
            Conference on Acoustics, Speech, and Signal Processing (ICASSP'03), Hong Kong, China, Vol. {VI}, pp. 421-424, April 6--10, 2003. 
        
        Author:
        -------
        Thierry Blu
        The Chinese University of Hong Kong.
        This software is downloadable at http://www.ee.cuhk.edu.hk/~tblu/demos/
        """
        if FFTanalysisfilters.ndim == 1:
            num_cols = len(FFTanalysisfilters)
        elif FFTanalysisfilters.ndim == 2:
            num_rows, num_cols = FFTanalysisfilters.shape

        M = len(x)

        # check if M is a power of 2
        if M != 2**round(np.log2(M)):
            print('The size of the input signal must be a power of two!')
            return None

        # check if the size of the filters matches the size of the input signal
        if num_cols != M:
            print('The size of the input signal and of the filters must match!')
            return None

        X = np.fft.fft(x,M)
        G=FFTanalysisfilters[0,:]
        H=FFTanalysisfilters[1,:]

        w = np.array([])  # Initialize w as an empty array
        for i in range(J):
            # Compute outputs Y and Z
            Y = G * X
            Z = H * X

            # Average corresponding parts of the signal
            half_M = int(M) // 2
            Y = 0.5 * (Y[:half_M] + Y[half_M:half_M * 2])
            Z = 0.5 * (Z[:half_M] + Z[half_M:half_M * 2])

            # Inverse FFT of Z and append to w
            z = np.fft.ifft(Z, half_M)
            w = np.concatenate((w, z)) if len(w) > 0 else z

            # Update variables for the next iteration
            M = half_M
            X = Y
            G = G[::2]
            H = H[::2]

        # Final concatenation of w and the real part of the inverse FFT of X
        u = np.fft.ifft(X, M)
        d = np.concatenate((np.real(w), np.real(u)))

        return d


    def FracSplineAnal(self,s0,j12,alpha):
        """
        Calculate Beta

        Parameters:
        ----------
        s0: EEG Data (Nepocs X Nsample) 
            'Nsample' must be a power of 2 in length
        J12: []
        FFTan: Analysis filter (considering only alpha value)
        
        Returns:
        -------
        beta: Beta value for one epoch
        """
        if not alpha:
            alpha = 3

        tau   = 0
        typ  = 'ortho'
        M1    = len(s0)

        J = int(math.log2(M1))-1
        M2 = 2**int(J+1)
        FFTan,_ = self.FFTfractsplinefilters(int(M2),alpha,tau,typ)

        w  = self.FFTwaveletanalysis1D(s0,FFTan,J)
        w = np.array(w)
        beta = self.beta_estimator(w,J,[])
        return beta


    def beta_estimator(self,w,J,j12):
        """
        Calculate beta based on wavelet coefficients

        Parameters:
        ----------
        w: wavelet coefficients 
        J:  number of wavelet decomposition scale in w
        J12: []

        Returns: Estimated beta value for one epoch
        -------
        """
        N = int(len(w))
        o = int(0) 
        N0 = int(N)

        etatj = np.zeros(J)
        nj = np.zeros(J)
        Sj = np.zeros(J)
        jSj = np.zeros(J)
        j2Sj = np.zeros(J)
        eSj = np.zeros(J)
        jeSj = np.zeros(J)

        for i in range(J):
            N= int(N/2)
            a = np.arange(o, o+N)
            o=o+N
            nj[i] = np.size(a)
            etatj[i] = np.log2(np.sum(np.abs(w[a])**2)/nj[i])
            Sj[i] = N0*np.log(2)*np.log(2)/2/2**(i+1)
            jSj[i] = (i+1)*Sj[i];
            j2Sj[i] = (i+1)*jSj[i];
            eSj[i] = etatj[i]*Sj[i];
            jeSj[i] = (i+1)*eSj[i];

         #double check len
        if len(j12) == 0:
            j1 = 0
            j2 = J-2
        else:
            j1 = 0
            j2 = 4

        beta = (np.sum(Sj[j1:j2])*sum(jeSj[j1:j2]) - sum(jSj[j1:j2])*sum(eSj[j1:j2]))/(sum(Sj[j1:j2])*sum(j2Sj[j1:j2]) - sum(jSj[j1:j2])*sum(jSj[j1:j2]));
        
        return beta


    def soft_schrinkage(self,w, J):
        """
        Apply soft shrinkage on wavelets.

        Parameters:
        ----------
        w: Wavelet coefficients.
        J: Number of wavelet decomposition scales in w.

        Returns:
        -------
        wt: Shrinked wavelet coefficients.
        r: Percentage of coefficients equal to zero.
        """
        def soft(x, l):
            return np.maximum(np.abs(x) - l, 0) * np.sign(x)
        
        jnoise = 1
        N = len(w)
        wt = []
        o = 0  # Start from 0 for Python indexing

        indices = []
        values = []
        levels = []

        for j in range(1, J + 1):
            N //= 2
            a = np.arange(o, o + N)
            o += N

            indices.extend(a)
            values.extend(w[a])
            levels.extend([j] * N)
        
        indices = np.array(indices)
        values = np.array(values)
        levels = np.array(levels)

        # Threshold for shrinkage:
        sigma = median_abs_deviation((values[levels == jnoise]))
        lambda_ = sigma * np.sqrt(2 * np.log(len(w)))

        # Shrinkage:
        nWt = soft(values, lambda_)
        r = 100 * np.sum(nWt == 0) / len(nWt)
        
        w[indices] = nWt  
        wt = w
        return wt, r


    def wavelet_indices(self, N, J):
        """
        Compute wavelet indices for each scales
            
        Parameters:
        ----------            
        N: Number of sample in the signal
        J: Numbers of scales

        Returns:
        -------
        a: Array of start indices for each scales
        b: Array of end indices for each scales
        """
        a = np.zeros(J+1, dtype=int)
        nj = np.zeros(J+1, dtype=int)
        b = np.zeros(J+1, dtype=int)

        # Initialize the first elements
        a[0] = 0 
        nj[0] = N / 2
        b[0] = a[0] + nj[0] - 1

        # Loop through indices from 1 to J (inclusive)
        for i in range(1, J + 1):
            a[i] = a[i - 1] + nj[i - 1]
            nj[i] = nj[i - 1] / 2
            b[i] = a[i] + nj[i] - 1

        return a, b


    def K(self,b, a):
        """
        Compute Kappa parameter 

        Parameters:
        ----------
        b: beta value 
        a:  alpha value

        Returns:
        -------
        kappa: Wavelet basis change between alpha and beta
        """
    
        kappa = (4 * math.pi) ** b
        u = 2 ** (a + 1) - 1
        v = 2 ** (a + b + 1) - 1
        w = zeta(a + 1) / zeta(a + b + 1)
        kappa = kappa * u / v * w
        
        return kappa


    def extract_RnB_signals(self,s):
        """
        Extract the rhytmic signal for each epoch of a dataset
        
        Parameters:
        ----------            
        s : EEG Data (Nepocs X Nsample)
            'Nsample' must be a power of 2 in length
        
        alpha: Regularity parameter of the reconstruction wavelet
        
        J: number of wavelet decomposition scale
            'J' must be lower than the logarithm base 2 of 'Nsample'
        
        Returns:
        -------
        sR: Extracted rhytmic signal (Nepocs X Nsamples)
              
        References:
        ----------
        In progress (2024)
        Blu, T. & Unser, M.,"The Fractional Spline Wavelet Transform: Definition and Implementation", Proc. IEEE International
        Conference on Acoustics, Speech, and Signal Processing (ICASSP'00), Istanbul, Turkey, Vol. {I}, pp. 512-515, June 5--9, 2000.
        """
        
        if s.ndim == 1:
            s = s[np.newaxis, :]  # Convert to 2D with shape (1, N)
        Nepo, N = s.shape 
   
        J = 8
        alpha0 = 4
        tau    = 0
        typ   = 'ortho'

        _, FFTsynthesisfilters = self.FFTfractsplinefilters(N, alpha0, tau, typ)

        a,b = self.wavelet_indices( N, J)

        betas = np.zeros(Nepo)  # Array to store beta values for each signal
        sR = np.zeros((Nepo, N))
        for isignal in range(Nepo):

            # current epoch
            se = np.array([s[isignal]])

            # normalize epoch           
            nh = np.sqrt(np.dot(se, se.T))  
            sh = se / nh

            #flatten epochs 
            se = np.ravel(se)
            sh = np.ravel(sh)

            # Compute beta
            BETA = self.FracSplineAnal(se, _, alpha0)
            alpha = BETA/2

            # Analysis Filter (considers alpha and beta value)
            FFTanalysisfilters,_ = self.FFTfractsplinefilters(N, alpha0+alpha, tau, typ)

            #  Wavelet analysis
            w = self.FFTwaveletanalysis1D(sh, FFTanalysisfilters, J)

            # Denoising : soft schrinkage
            w,r = self.soft_schrinkage(w, J)

            # Filtering arrhythmic component
            wr = np.zeros_like(w)
            for i in range(J):
                aWj = w[a[i]-1:b[i]]  # Adjusting for MATLAB to Python indexing
                aWp = self.K(alpha, alpha0) * 2**(-i * alpha) * aWj
                wr[a[i]-1:b[i]] = aWp

            # Wavelet synthesis
            sR[isignal] = self.FFTwaveletsynthesis1D(wr, FFTsynthesisfilters,J)
            sR[isignal] = sR[isignal] * nh; # re-scale signal

            betas[isignal] = BETA;

        return {
            "rhythmic signal": sR, 
            "spectral exponent": betas 
        }