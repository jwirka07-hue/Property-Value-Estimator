# Apartment Value Estimator (Georgia multifamily)

Owner uploads a rent roll + answers 3 questions -> estimated value range.

## Files
- app.py          the website (Streamlit)
- engine.py       all valuation math (direct cap, tax reset)
- rentroll.py     reads CSV/Excel rent rolls
- market_data.py  cap rates, millage, vacancy, with sources (update quarterly)
- test_engine.py  checks the math against the spec's worked example
- sample_rent_roll.csv  test file

## Run on your computer
    pip install -r requirements.txt
    streamlit run app.py

## Put it on the web (free)
1. Create a GitHub repo and upload these files.
2. Go to share.streamlit.io, sign in with GitHub, click "Create app".
3. Pick the repo, set main file to app.py, click Deploy.
You get a public link like yourapp.streamlit.app.
