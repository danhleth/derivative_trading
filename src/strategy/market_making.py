from typing import Any
import numpy as np
import matplotlib.pyplot as plt

class NaiveMM:
    def __init__(self, opts):
        # Parameters for mid price simulation:
        self.S0 = opts['S0'] 			# initial price
        self.T = opts['T']  			# time
        self.sigma = 2 			# volatility
        self.M = 20000 			# number of time steps
        self.gamma = opts['gamma'] 		# risk aversion
        self.k = opts['k']				#
        self.A = opts['A']				# order probability
        self.I = opts['I']				# stocks
        

    
    def fit(self, X:np.array):
        # Parameters for mid price simulation:
        AverageSpread = []
        Profit = []
        Std = []
        self.M = len(X)
        dt = self.T/float(self.M)
       
        S = np.zeros((self.M+1, self.I))
        Bid = np.zeros((self.M+1, self.I))
        Ask = np.zeros((self.M+1, self.I))
        ReservPrice = np.zeros((self.M+1, self.I))
        spread = np.zeros((self.M+1, self.I))
        # deltaB = np.zeros((self.M+1, self.I))
        # deltaA = np.zeros((self.M+1, self.I))
        q = np.zeros((self.M+1, self.I))
        w = np.zeros((self.M+1, self.I))
        equity = np.zeros((self.M+1, self.I))

        S[0] = self.S0
        ReservPrice[0] = self.S0
        Bid[0] = self.S0
        Ask[0] = self.S0
        spread[0] = 0
        # deltaB[0] = 0
        # deltaA[0] = 0
        q[0] = 0 		# position
        w[0] = 0 		# wealth
        equity[0] = 0
        
        
        for t in range(len(X)):
            
            S[t] = X[t][1]
            ReservPrice[t] = S[t] - q[t-1] * self.gamma * (self.sigma ** 2) * (self.T - t/float(self.M)) # Mid Price estimation
            spread[t] = self.gamma * (self.sigma ** 2) * (self.T - t/float(self.M)) + (2/self.gamma) * np.log(1 + (self.gamma/self.k))	 # Spread estimation
            Bid[t] = ReservPrice[t] - spread[t]/2.
            Ask[t] = ReservPrice[t] + spread[t]/2.

            deltaB = S[t] - Bid[t]
            deltaA = Ask[t] - S[t]

            lambdaA = self.A * np.exp(-self.k * deltaA)
            ProbA = 1 - np.exp(-lambdaA*dt)
            fa = np.random.random()

            lambdaB = self.A * np.exp(-self.k * deltaB)
            ProbB = 1 - np.exp(-lambdaB*dt)
            fb = np.random.random()

            if ProbB > fb and ProbA < fa:				# buy market order filling our limit order
                q[t] = q[t-1] + 1						# position
                w[t] = w[t-1] - Bid[t]					# wealth

            if ProbB < fb and ProbA > fa:				# sell market order filling our limit order
                q[t] = q[t-1] - 1						# position
                w[t] = w[t-1] + Ask[t]					# wealth

            if ProbB < fb and ProbA < fa:				# no order
                q[t] = q[t-1]							# position
                w[t] = w[t-1]							# wealth

            if ProbB > fb and ProbA > fa:				# both sides order
                q[t] = q[t-1]							# position
                w[t] = w[t-1] - Bid[t]					# wealth
                w[t] = w[t] + Ask[t]

            equity[t] = w[t] + q[t] * S[t]
        
        AverageSpread.append(spread.mean())
        Profit.append(equity[-1])
        Std.append(np.std(equity))

        print("                   Results              ")
        print("----------------------------------------")
        print("%14s %21s" % ('statistic', 'value'))
        print(40 * "-")
        print("%14s %20.5f" % ("Average spread :", np.array(AverageSpread).mean()))
        print("%16s %20.5f" % ("Profit :", np.array(Profit).mean()))
        print("%16s %20.5f" % ("Std(Profit) :", np.array(Std).mean()))

        # Plots:
        x = np.linspace(0., self.T, num=(self.M+1))

        fig = plt.figure(figsize=(10, 8))
        plt.subplot(2, 2, 1)   						# number of rows, number of  columns, number of the subplot
        plt.plot(x, S[:], lw=1., label='S')
        plt.plot(x, Ask[:], lw=1., label='Ask')
        plt.plot(x, Bid[:], lw=1., label='Bid')
        plt.grid(True)
        plt.legend(loc=0)
        plt.ylabel('P')
        plt.title('Prices')

        plt.subplot(2, 2, 2)
        plt.plot(x, q[:], 'g', lw=1., label='q') 	# plot 2 lines
        plt.grid(True)
        plt.legend(loc=0)
        plt.axis('tight')
        plt.xlabel('Time')
        plt.ylabel('Position')
        #plt.show()


        plt.subplot(2, 2, 4)
        plt.plot(x, equity[:], 'b', lw=1., label='equity')
        plt.grid(True)
        plt.legend(loc=0)
        plt.axis('tight')
        plt.xlabel('Time')
        plt.ylabel('Position')

        # Histogram of profit:
        #plt.figure(figsize=(7, 5))
        plt.subplot(2, 2, 3)
        plt.hist(np.array(Profit), label=['Inventory strategy'], bins=100)
        plt.legend(loc=0)
        plt.grid(True)
        plt.xlabel('pnl')
        plt.ylabel('number of values')
        plt.title('Histogram')
        plt.show()
        
        


    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass