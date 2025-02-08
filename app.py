import streamlit as st

# Dictionary of common future instruments with tick sizes, contract sizes, and tick value in dollars
futures_data = {
    'Nasdaq 100 (Mini)': {'symbol': 'NQ=F', 'tick_index': 0.25, 'contract_size': 20},
    'S&P 500 (Mini)': {'symbol': 'ES=F', 'tick_index': 0.25, 'contract_size': 50},
    'Dow Jones (Mini)': {'symbol': 'YM=F', 'tick_index': 1, 'contract_size': 5},
    'Crude Oil (WTI)': {'symbol': 'CL=F', 'tick_index': 0.01, 'contract_size': 1000},
    'Gold (XAU)': {'symbol': 'GC=F', 'tick_index': 0.10, 'contract_size': 100},
    'Euro/USD (6E)': {'symbol': '6E=F', 'tick_index': 0.00005, 'contract_size': 125000}
}

# Function to calculate target profit, stop loss, and tick sizes
def calculate_ticks_and_points(opening_profit, risk_amount, tick_index, contract_size):
    # Calculate tick value in dollars (tick index * contract size)
    tick_value = tick_index * contract_size
    tick_per_point = 4  # 4 ticks = 1 point

    # Calculate the 30% of the opening profit for target profit
    target_profit = opening_profit * 0.49

    # Calculate the number of ticks needed to achieve the target profit
    target_ticks = target_profit / tick_value
    
    # Calculate the number of points needed for the target profit (4 ticks = 1 point)
    target_points = target_ticks / tick_per_point
    
    # Calculate the number of stop loss ticks based on the amount of risk the user wants
    stop_loss_ticks = risk_amount / tick_value
    stop_loss_points = stop_loss_ticks / tick_per_point  # 4 ticks = 1 point
    
    return target_profit, target_ticks, target_points, stop_loss_ticks, stop_loss_points, tick_value

# Streamlit app layout
st.markdown(
    """
    <style>
    .main {
        background-color: #F5F5F5;  /* Light grey background */
        color: #333333;  /* Dark text for contrast */
        padding: 2rem;
        border-radius: 8px;
    }
    .title {
        text-align: center;
        color: #4CAF50;  /* Green title color */
    }
    .subtitle {
        text-align: center;
        color: black;  /* Black color for subtitles */
    }
    .container {
        text-align: center;
    }
    .image-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .info-container {
        font-size: 1.1rem;
        margin-top: 20px;
    }
    .card {
        padding: 1.5rem;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        color: black;
    }
    .card-target {
        background-color: #FFEB3B;  /* Yellow card background for Target Profit */
    }
    .card-ticks {
        background-color: #4CAF50;  /* Green card background for Ticks */
    }
    .card-stop-loss {
        background-color: #2196F3;  /* Blue card background for Stop Loss */
    }
    </style>
    """, unsafe_allow_html=True
)

# Add image (e.g., a dollar image or currency related)
#st.markdown('<div class="image-container"><img src="https://i.imgur.com/3np29VJ.png" alt="Dollar Image" width="200"></div>', unsafe_allow_html=True)

# Streamlit app title
st.markdown('<h1 class="title">Target and Loss Stop Calculator</h1>', unsafe_allow_html=True)

# Description of the app
st.markdown("""
### Welcome to the **Target and Loss Stop Calculator**!

This tool helps you calculate the target profit, stop loss, and the number of ticks and points required based on your selected futures instrument.

1. **Target Profit**: 49% of your opening profit.
2. **Stop Loss**: Calculated based on your desired risk.
3. **Tick Value**: Based on the selected futures instrument.

### How it works:
1. Select a futures instrument.
2. Input your opening profit and risk amount.
3. The app will calculate the number of ticks required for target profit and stop loss, as well as the price per tick and point based on your instrument's contract size.
""", unsafe_allow_html=True)

# Dropdown to select a futures instrument (with placeholder, no pre-selection)
selected_instrument = st.selectbox("Select a Futures Instrument:", ["--Select an Instrument--"] + list(futures_data.keys()))

# Check if the user has selected an instrument
if selected_instrument != "--Select an Instrument--":
    # Get selected instrument data
    instrument_data = futures_data[selected_instrument]

    # Display instrument details
    st.subheader(f"Details for {selected_instrument}:")
    st.write(f"Symbol: {instrument_data['symbol']}")
    st.write(f"Tick Index: {instrument_data['tick_index']} index points")
    st.write(f"Contract Size: {instrument_data['contract_size']} units")

    # Calculate the tick value and point value in dollars
    tick_value_in_dollars = instrument_data['tick_index'] * instrument_data['contract_size']
    point_value_in_dollars = tick_value_in_dollars * 4  # 4 ticks = 1 point

    st.write(f"Tick Value in Dollars: ${tick_value_in_dollars:.2f}")
    st.write(f"Point Value in Dollars (4 ticks): ${point_value_in_dollars:.2f}")

    # Input fields for the user
    opening_profit = st.number_input("Enter the opening profit before the trade (in dollars):", min_value=0.0, step=1.0)
    risk_amount = st.number_input("Enter the amount you are willing to risk (in dollars):", min_value=0.0, step=1.0)

    # Button to calculate
    calculate_button = st.button("Calculate")

    # Check if the "Calculate" button is pressed and both inputs are provided
    if calculate_button:
        # Ensure both inputs are valid (opening_profit > 0 and risk_amount >= 0)
        if opening_profit > 0 and risk_amount >= 0:
            # Get the tick value and contract size of the selected instrument
            tick_index = instrument_data['tick_index']
            contract_size = instrument_data['contract_size']
            
            # Calculate the result based on the tick value of the selected instrument
            target_profit, target_ticks, target_points, stop_loss_ticks, stop_loss_points, tick_value = calculate_ticks_and_points(
                opening_profit, risk_amount, tick_index, contract_size)
            
            # Display the results in a card with different background colors
            st.markdown('<div class="card card-target"><h3 class="subtitle">49% of your opening profit (${:.2f}):</h3>'.format(opening_profit), unsafe_allow_html=True)
            st.write(f"Target Profit: ${target_profit:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

            # Display the number of ticks and points needed to reach the target profit in a green card
            st.markdown('<div class="card card-ticks"><h3 class="subtitle">To achieve the target profit:</h3>', unsafe_allow_html=True)
            st.write(f"Ticks: {target_ticks:.2f} ticks")
            st.write(f"Points: {target_points:.2f} points")
            st.markdown('</div>', unsafe_allow_html=True)

            # Display the number of stop loss ticks and points in a blue card
            st.markdown('<div class="card card-stop-loss"><h3 class="subtitle">Risk management - Stop loss:</h3>', unsafe_allow_html=True)
            st.write(f"Stop Loss Ticks: {stop_loss_ticks:.2f} ticks")
            st.write(f"Stop Loss Points: {stop_loss_points:.2f} points")
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            # If inputs are not valid, show a message
            st.warning("Please enter both valid opening profit and risk amount values to calculate.")
else:
    # If no instrument selected, inform the user
    st.info("Please select a futures instrument to view details and perform calculations.")
