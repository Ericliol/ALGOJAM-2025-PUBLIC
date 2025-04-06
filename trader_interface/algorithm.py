import numpy as np
import matplotlib.pyplot as plt 

from scipy.stats import zscore

# Custom trading Algorithm
class Algorithm():

    ########################################################
    # NO EDITS REQUIRED TO THESE FUNCTIONS
    ########################################################
    # FUNCTION TO SETUP ALGORITHM CLASS
    def __init__(self, positions):
        # Initialise data stores:
        # Historical data of all instruments
        self.data = {}
        # Initialise position limits
        self.positionLimits = {}
        # Initialise the current day as 0
        self.day = 0
        # Initialise the current positions
        self.positions = positions

        self.uqDollarActionPrice = 0
        self.dogfEMA = 0
      

        self.price_history = {}  # Store price history for plotting
        self.position_history = {}


    # Helper function to fetch the current price of an instrument
    def get_current_price(self, instrument):
        # return most recent price
        return self.data[instrument][-1]
    ########################################################

    # RETURN DESIRED POSITIONS IN DICT FORM
    def get_positions(self):
        # Get current position
        currentPositions = self.positions
        # Get position limits
        positionLimits = self.positionLimits
        
        # Declare a store for desired positions
        desiredPositions = {}
        # Loop through all the instruments you can take positions on.
        for instrument, positionLimit in positionLimits.items():
            # For each instrument initilise desired position to zero
            desiredPositions[instrument] = 0

        # IMPLEMENT CODE HERE TO DECIDE WHAT POSITIONS YOU WANT 
        #######################################################################
        # Display the current trading day
        print("Starting Algorithm for Day:", self.day)
        
        # I only want to trade the UQ Dollar
        # trade_instruments = ["UQ Dollar"]
        # trade_instruments = ["UQ Dollar","Dawg Food"]
        # trade_instruments = ["Dawg Food"]
        # trade_instruments = ["Quantum Universal Algorithmic Currency Koin"]
        trade_instruments = ["Rare Watch"]
        # trade_instruments = ["Goober Eats"]
        
        # Display the prices of instruments I want to trade
        for ins in trade_instruments:
            print(f"{ins}: ${self.get_current_price(ins)}")


        if self.day >= 1:
            for ins in trade_instruments:
                print(ins)
                if ins == "UQ Dollar":
                    # upperb = 100
                    # lowerb = 100
                    # if self.get_current_price(ins) > upperb:
                    #     desiredPositions[ins] = -positionLimits[ins]
                    # elif self.get_current_price(ins) < lowerb:
                    #     desiredPositions[ins] = positionLimits[ins]

                    buff = 0.1
                    if (self.get_current_price(ins) - buff > self.uqDollarActionPrice ) and (self.get_current_price(ins) > 100.1):
                        desiredPositions[ins] = -positionLimits[ins]
                    elif (self.get_current_price(ins) + buff < self.uqDollarActionPrice ) and (self.get_current_price(ins) < 100):
                        desiredPositions[ins] = positionLimits[ins]
                    else:
                        desiredPositions[ins] = self.positions[ins]

                    if desiredPositions[ins] != self.positions[ins]:
                        self.uqDollarActionPrice = self.get_current_price(ins)
                    
                elif ins == "Dawg Food":
                   
                    period = 35
                    k = 2 / (period + 1)
                    if self.day == period:
                        self.dogfEMA = np.mean(self.data[ins][:period])
                    elif self.day >= period:
                        self.dogfEMA = self.get_current_price(ins)*k + self.dogfEMA*(1-k)
                    
                        if self.get_current_price(ins) > self.dogfEMA*(1-k):
                            desiredPositions[ins] = -positionLimits[ins]
                        else:
                            desiredPositions[ins] = positionLimits[ins]
                    else:
                        if self.data[ins][-2] > self.data[ins][-1]:
                            desiredPositions[ins] = positionLimits[ins]
                            desiredPositions[ins] = 0
                        else:
                            desiredPositions[ins] = -positionLimits[ins]

                elif ins == "Quantum Universal Algorithmic Currency Koin":

                    buff = 0.001
                    longShortRatio = 0.4
                    if self.day >= 2:
                        if (2.2 - buff) <= self.get_current_price(ins) <= (2.2 + buff):
                            print("BUy partial in")
                            desiredPositions[ins] = longShortRatio*positionLimits[ins]
                        elif 2.44 < self.get_current_price(ins) :
                            print("Sell all in")
                            desiredPositions[ins] = -positionLimits[ins]
                        elif self.get_current_price(ins) < 1.96:
                            print("BUY all in")
                            desiredPositions[ins] = positionLimits[ins]
                        else:
                            # print("No action taken")
                            # desiredPositions[ins] = self.position_history[ins][-1]
                            if self.data[ins][-2] > self.data[ins][-1]:
                                desiredPositions[ins] = positionLimits[ins]
                                
                            else:
                                desiredPositions[ins] = -positionLimits[ins]
                elif ins == "Rare Watch":
                        if self.day >= 2:
                            buff =0.4
                            # ratio = 0.4

                            diff2 = self.data[ins][-3] -self.data[ins][-2]
                            diff1 = self.data[ins][-2] -self.data[ins][-1]
                            # if abs(abs(diff2) - abs(diff1)) > buff and self.day > 3 and diff2 >0  and (diff1<0 and diff2 <0) or (diff1>0 and diff2 >0):
                            #     desiredPositions[ins] = self.position_history[ins][-1]
                                
                            #     # if self.data[ins][-2] - self.data[ins][-1] < 0 and self.position_history[ins][-1] > 0:
                            #     #     desiredPositions[ins] = -positionLimits[ins]

                            prices = self.data[ins]
                            current_price = self.get_current_price(ins)

                            # Z-score detection
                            if self.day >= 5:
                                if abs(diff1) > buff:   
                                    desiredPositions[ins] = self.position_history[ins][-1]
                                elif self.data[ins][-2] > self.data[ins][-1]:
                                    desiredPositions[ins] = -positionLimits[ins]
                                    
                                else:
                                    desiredPositions[ins] = positionLimits[ins]
    

                            elif self.data[ins][-2] > self.data[ins][-1]:
                                desiredPositions[ins] = -positionLimits[ins]
                                
                            else:
                                desiredPositions[ins] = positionLimits[ins]

                elif ins == "Goober Eats":
                    if self.day >= 2:
                        for ins in trade_instruments:
                            # if price has gone down buy
                            if self.data[ins][-2] > self.data[ins][-1]:
                                desiredPositions[ins] = positionLimits[ins]
                                desiredPositions[ins] = 0
                            else:
                                desiredPositions[ins] = -positionLimits[ins]
                        


                    
                    
        # # Start trading from Day 2 onwards. Buy if price dropped and sell if price rose compared to the previous day
        # if self.day >= 2:
        #     for ins in trade_instruments:
        #         # if price has gone down buy
        #         if self.data[ins][-2] > self.data[ins][-1]:
        #             desiredPositions[ins] = positionLimits[ins]
        #             desiredPositions[ins] = 0
        #         else:
        #             desiredPositions[ins] = -positionLimits[ins]
        # # Display the end of trading day
        for ins in trade_instruments:
            if ins not in self.price_history:
                self.price_history[ins] = []
                self.position_history[ins] = []
            self.price_history[ins].append(self.get_current_price(ins))
            self.position_history[ins].append(desiredPositions[ins])

        print("Ending Algorithm for Day:", self.day, "\n")
        

        #######################################################################
        # Return the desired positions
        return desiredPositions


    def plot_data(self):
        # Plot current_price against day with buy/sell markers
        plt.figure(figsize=(24, 6))
        for instrument, prices in self.price_history.items():
            days = range(len(prices))
            plt.plot(days, prices, label=f"{instrument} Price")

            # Add buy/sell markers
            if instrument in self.position_history:
                positions = self.position_history[instrument]
                for i in range(1, len(positions)):
                    if positions[i] > positions[i - 1]:  # Buy signal
                        plt.scatter(i, prices[i], color='green', label="Buy" if i == 1 else "", zorder=5)
                        plt.text(i, prices[i], f"Day {i}", color='green', fontsize=10, ha='left', va='bottom')
                    elif positions[i] < positions[i - 1]:  # Sell signal
                        plt.scatter(i, prices[i], color='red', label="Sell" if i == 1 else "", zorder=5)
                        plt.text(i, prices[i], f"Day {i}", color='red', fontsize=10, ha='left', va='top')

        plt.xlabel("Day")
        plt.ylabel("Price")
        plt.title("Price vs Day with Buy/Sell Markers")
        plt.legend()
        plt.savefig("price_vs_day_with_markers.png")  # Save the figure
        plt.show()


        # Plot change in position against day
        plt.figure(figsize=(24, 6))
        for instrument, positions in self.position_history.items():
            plt.plot(range(len(positions)), positions, label=f"{instrument} Position")
        plt.xlabel("Day")
        plt.ylabel("Position")
        plt.title("Position vs Day")
        plt.legend()
        plt.savefig("position_vs_day.png")  # Save the figure
        plt.show()