import numpy as np

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

        self.dogfEMA = 0
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
        trade_instruments = ["UQ Dollar","Dawg Food"]
        # trade_instruments = ["Dawg Food"]
        
        # Display the prices of instruments I want to trade
        for ins in trade_instruments:
            print(f"{ins}: ${self.get_current_price(ins)}")


        if self.day >= 1:
            for ins in trade_instruments:
                print(ins)
                if ins == "UQ Dollar":
                    upperb = 100
                    lowerb = 100
                    if self.get_current_price(ins) > upperb:
                        desiredPositions[ins] = -positionLimits[ins]
                    elif self.get_current_price(ins) < lowerb:
                        desiredPositions[ins] = positionLimits[ins]
                    # elif self.get_current_price(ins) == 100:
                    #     desiredPositions[ins] = 0
                    # else:
                    #     perc_v = (self.get_current_price(ins) - 100)/ (upperb - lowerb)
                    #     desiredPositions[ins] = perc_v*positionLimits[ins]
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
        print("Ending Algorithm for Day:", self.day, "\n")
        

        #######################################################################
        # Return the desired positions
        return desiredPositions
