import matplotlib.pyplot as plt
import io

class BidCalculator:
    def __init__(self, starting_price, bid_increment, duration_in_minutes):
        self.starting_price = starting_price
        self.bid_increment = bid_increment
        self.duration_in_minutes = duration_in_minutes

    def calculate_final_price(self):
        # Convert duration to seconds
        duration_in_seconds = self.duration_in_minutes * 60
        
        # Calculate total number of bids
        time_between_bids = 10  # Assume each bid happens every 10 seconds
        total_bids = duration_in_seconds // time_between_bids
        
        # Calculate price increase
        price_increase = self.bid_increment * total_bids
        predicted_final_price = self.starting_price + price_increase
        
        return predicted_final_price

    def simulate_bidding(self):
        duration_in_seconds = self.duration_in_minutes * 60
        time_between_bids = 10
        total_bids = duration_in_seconds // time_between_bids

        times = [i * time_between_bids for i in range(total_bids)]
        prices = [self.starting_price + self.bid_increment * i for i in range(total_bids)]

        return times, prices

    def plot_bidding_progress(self):
        times, prices = self.simulate_bidding()

        plt.figure(figsize=(10, 6))
        plt.plot(times, prices, label='Bid Progression', color='b')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Price ($)')
        plt.title('Bid Progression Over Time')
        plt.legend()

        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        return buffer  # Buffer can be used with any web framework for streaming
