# import requiredLibraries
# import functionFiles

# ticker = Select_a_stock_ticker_of_your_choice

# # fetch the ohlc data in a pandas dataframe 
# df = fetch_data_from_api

# # performing feature engineering using functions from ta library 

# # add ema 100 and ema 200 with signal
# ema_100(df)
# ema_200(df)
# ema_signal(df)

# # add vwap with signal
# vwap(df)
# vwap_signal(df)

# # add stochastic RSI with signal
# stochasticRSI(df)
# StochRSI_signal(df)

# # add MACD with signal
# macd(df)
# macd_signal(df)

# # add absolute change and change percentage to all features
# abs_change(df)
# abs_pct_change(df)

# # finally add the target variable
# trend(df)

# # clean and normalise the final dataframe 
# clean(df)
# normalise(df) # techniques used are min max scaling and polarizing
# reindex(df)

# # initialize empty np arrays for all the features
# initialize_np_arrays()

# # put data from the df into the numpy arrays in batches of 230 datapoints also including the target variable
# for i in range (0, df.shape[0] - 230):
#     np_arrays.append(df.iloc[i:i+230, featurePositionNumber])
#     y.append(df.iloc[i+230, targetVariablePositionNumber])

# # reshape target variable as it has variable dimensionality
# y = np.reshape(y, (len(y), 1))

# # put all the np arrays except target variable into another np array X
# X = np.stack([all_np_arrays])

# # split the data into training and testing data, 80% is training and 20% is testing data 
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=0)

# # initialize the lstm model
# model = Sequential()

# # defining the architecture of the lstm model
# model.add(LSTM(128, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
# model.add(LSTM(128, return_sequences=False))
# model.add(Dense(128, activation='tanh'))
# model.add(Dense(1))

# # Compile the model with appropriate optimizer, loss function and metrics
# optimizers.SGD(momentum=0.9)
# model.compile(optimizer='SGD', loss='mse', metrics=['mae'])

# # training the model
# model.fit(X_train, y_train, validation_split=0.2, epochs=20, batch_size=12)

# # evaluating the model
# score = model.evaluate(X_test, y_test, verbose=0)
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])

# # graph to look at the performance

# predictions = model.predict(X_test)
# cmp = [1 if x > 0.35 else -1 if x < -0.35 else 0 for x in predictions]

# plt.figure(figsize=(24,12))
# plt.plot(cmp[-200:-100])
# plt.plot(y_test[-200:-100],'r', linestyle='--' )
# plt.show

