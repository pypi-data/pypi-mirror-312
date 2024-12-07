# bidding/bidding_logic.py

class BidResult:
    def __init__(self, success, message):
        self.success = success
        self.message = message

def make_bid_logic(auction, bid_amount, bidder):
    """
    Logic to place a bid on an auction. Assumes the auction object and bidder are provided.
    Returns a BidResult object.
    """
    if auction.highest_bid == 0:  # No bids placed yet
        if bid_amount > auction.starting_price:
            auction.highest_bid = bid_amount
            auction.highest_bidder = bidder  # Use the passed-in bidder
            auction.save()
            return BidResult(True, f'Your bid of ${bid_amount} was successful! You are the highest bidder.')
        else:
            return BidResult(False, f'Your bid must be higher than the starting price of ${auction.starting_price}.')
    else:
        if bid_amount > auction.highest_bid:
            auction.highest_bid = bid_amount
            auction.highest_bidder = bidder  # Use the passed-in bidder
            auction.save()
            return BidResult(True, f'Your bid of ${bid_amount} was successful! You are the highest bidder.')
        else:
            return BidResult(False, f'Your bid must be higher than the current highest bid of ${auction.highest_bid}.')
