# -*- coding: utf-8 -*-


from cleantext import clean
import pandas as pd
import numpy as np
import re
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
import joblib


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
import joblib


class C:
  def __init__(self , message ):
    self.message = message 
    self.obj = dict()
  
  def predict(self):
    vectorizer = CountVectorizer()
    text_data = [signal, entry_target, take_profit]
    X = vectorizer.fit_transform(text_data)

    new_text_vectorized = vectorizer.transform([self.message])
    clf = joblib.load('Xavi89.sav')
    predicted_label = clf.predict(new_text_vectorized)[0]
    self.obj['message_type'] = predicted_label
    return predicted_label

  def signal_classification(self):
    line_by = [single  for single in self.message.split('\n') if len(single) > 1]
    output = dict()
    output['message_type'] = 'Signal'
    # Signal Values
    output['coin'] = clean([s for s in line_by if "#" in s][0], no_emoji=True).replace('#','')
    output['signal_type'] = [s for s in line_by if "Signal" in s][0].replace('Signal Type: ' , '')
    output['leverage'] = [s for s in line_by if "Leverage" in s][0].replace('Leverage: ' , '')
    output['entry_target'] = [s for s in line_by if "Entry" in s][0].replace('Entry Targets: ' , '').split(' ')
    # output['take_profit_targets(with numbers)'] =  [line for  line in line_by if len(line) == 9]
    output['take_profit_targets'] =  [re.sub(r"\s*\d+\)\s*", "", line) for  line in line_by if len(line) == 9]

    # STOP LOSS
    stop_loss_index = line_by.index([s for s in line_by if "Stop-Loss" in s][0])
    output['stop_loss'] = clean(line_by[stop_loss_index+1],no_emoji=True)

    return output

  def entry_target_classification(self):
    output = dict()
    line_by = [m for m in self.message.split('\n') if len(m) > 1]
    output['message_type'] = 'Entry Target'
    output['coin'] = clean([s for s in line_by if "#" in s][0], no_emoji=True).replace('#','').split(' ')[0]
    output['entry_target'] = clean([s for s in line_by if "#" in s][0].replace('Entry target' , ''), no_emoji=True).replace('#','').replace(output['coin'] , '').replace(' ' , '')
    output['average_entry_price'] = clean([s for s in line_by if "Entry Price" in s][0], no_emoji=True).replace('Average Entry Price: '.lower() , '')
    return output
  def take_profit_classification(self):
    output = dict()
    line_by = [m for m in self.message.split('\n') if len(m) > 1]
    output['message_type'] = 'Take Profit'
    output['coin'] = clean([s for s in line_by if "#" in s][0], no_emoji=True).replace('#','').split(' ')[0]


    output['target'] = clean([s for s in line_by if "#" in s][0].replace('Take-Profit target' , ''), no_emoji=True).replace('#','').replace(output['coin'] , '').replace(' ' , '')
    output['profit'] = clean([s for s in line_by if "Profit" in s][1], no_emoji=True).replace('profit: ' ,'')
    output['period(minutes)'] = clean([s for s in line_by if "Period" in s][0], no_emoji=True).replace('period: ' ,'').replace(' minutes' , '')

    return output



  def output(self):
    message_type = self.predict()
    if(message_type == 'signal'):
      return self.signal_classification()
    elif(message_type == 'entry_target') :
      return self.entry_target_classification()
    elif(message_type == 'take_profit') :
      return self.take_profit_classification()
    else:
      return "Not Classified"


message = """
⚡️⚡️#OCEAN/USDT⚡️⚡️
Signal Type: Long
Leverage: Cross 20x
Entry Targets: 0.2451 0.2350
Take-Profit Targets: 
1) 0.2465
2) 0.2477
3) 0.2489
4) 0.2510
5) 0.2535
6) 0.2560
7) 0.2585
8) 0.2610

Stop-Loss: 
0.2250🚀🚀
"""


C(message).output()




# SIGNALS>>>>>>>>>>>>>>>>>>>>>>>>>

# signal = """
# ⚡️⚡️#OCEAN/USDT⚡️⚡️
# Signal Type: Long
# Leverage: Cross 20x
# Entry Targets: 0.2451 0.2350
# Take-Profit Targets: 
# 1) 0.2465
# 2) 0.2477
# 3) 0.2489
# 4) 0.2510
# 5) 0.2535
# 6) 0.2560
# 7) 0.2585
# 8) 0.2610

# Stop-Loss: 
# 0.2250🚀🚀
# """

# entry_target = """
# Binance Futures, ByBit USDT
# #DYDX/USDT Entry target 1 ✅
# Average Entry Price: 1.361 💵

# """


# take_profit = """
# Binance Futures
# #OCEAN/USDT Take-Profit target 1 ✅
# Profit: 11.4239% 📈
# Period: 7 Minutes ⏰
# """