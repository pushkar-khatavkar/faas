import logging
import yfinance as yf
import azure.functions as func
import wikipedia


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')


    if name:
        org = str(name)
        org = org.upper()
        try:
            ticker = yf.Ticker(org).info
        except:
            logging.info('Invalid Ticker')
        if ticker['regularMarketPrice']:
            market_price = str(ticker['regularMarketPrice'])
            open= str(ticker['open'])
            previous_close_price = str(ticker['regularMarketPreviousClose'])
            longName = str(ticker['longName'])
            try:
                wiki = str(wikipedia.summary(longName, sentences=2))
            except:
                logging.info('No wiki')
                wiki = "No info"
            country = str(ticker['country'])
            city = str(ticker['city'])
            state = str(ticker['state'])
            currency = str(ticker['currency'])
            return func.HttpResponse("\nName : "+longName+"\n\nTicker : "+org+"\n\nAbout : "+wiki+"\nCountry : "+city+","+state+","+country+"\n\nPrice : "+market_price+" "+currency+
                                    "\nOpen : "+open+" "+currency+"\nClose : "+previous_close_price+" "+currency+"\n\n\nNote : To change the ticker edit the name variable in URL. e.g. GOOGL,MSFT,AMZN."
                                   )
        else:
            return func.HttpResponse("Invalid Ticker,Please check the entered ticker.")
    else:
        return func.HttpResponse(
             "Please enter a Ticker in url.",
             status_code=200
        )
