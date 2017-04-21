class MovingAvgExperimentModel:
    
    def __init__(self):

        self.component = str()
        self.component_method = str()
        self.ma_type = str()
        self.qc_rules = list()
        self.replicate_data = []
            
    # dumps Result object in json
    def tojson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)
    
class ReplicatePerformanceModel:

    def __init__(self):

        # Ma/QC Parameters
        self.ma_utl = int()
        self.ma_ltl = int()
        self.ma_url = int()
        self.ma_lrl = int()
        self.ma_window = int()
        self.number_of_ma_flags = int()

        # Performance metrics
        self.true_positive = int()
        self.true_negative = int()
        self.false_positive = int()
        self.false_negative = int()
        self.precision = float()
        self.recall = float()

        # datetime("%Y-%m-%d %H:%M:%S")
        # 2017-01-15 00:15:00
        self.ma_flag_ts = str()
        self.qc_flag_ts = str()
        self.ma_qc_diff_secs = str()

    def calculate_timestamp_diff(self):
        return (self.qc_flag_ts - self.ma_flag_ts).seconds     

    def calculate_recall(self):
        return (self.true_positive / (self.true_positive + self.false_negative))

    def calculate_precision(self):
        if (self.true_positive + self.false_positive) == 0:
            return 0
        else:
            return (self.true_positive / (self.true_positive + self.false_positive))
    
    def calculate_number_of_flags(self):
        return (self.true_positive + self.false_positive)

        

def df_to_series(df, method, qc=False, flags=False):
    
    """
    Return a value series for a given method
    """
    
    
    if qc == False:
        # get the requested test and method and create a new DF
        df_ = df.loc[(df.Test != 'QC YH CHEM PANEL 1') & (df.Method == method)]
        test = 'val'
    elif qc == True:
        df_ = df.loc[(df.Test == 'QC YH CHEM PANEL 1') & (df.Method == method)]
        test = 'qc'


    else:
        print "Set qc flag: true if you want qc, false if you want result values"
        
    if flags == False:
        # take just the data and the value columns
        df_ = df_[['Verified','Value']]
    else:
        df_ = df_[['Verified','Decision']]


    try:
        if len(df_) != 0:
            # save to csv
            df_.to_csv('tmp.csv'.format(test, method), index=False)

            # read csv back in as a series
            series = pd.Series.from_csv('tmp.csv'.format(test, method),header=0)
        else:
            print(test)
            sys.exit("in df_to_series(): df_ was null")
            
    except Exception, e:
        print e 
        
    return series


def simple_moving_average(Window, ValTimeSeries):
    """
    Create a simple moving averages TimeSeries
    In: 
    -> Moving averages window
    -> TimeSeries of values
    Out: TimeSeries of MovingAverages for each of the supplied TimeStamps
    """
    
    ma_rs1_series = ValTimeSeries.copy(deep=True)
    
    for i in range(len(ValTimeSeries)):
        if i == 0:
            continue
        elif i < Window:
            ma_rs1_series[i] = ValTimeSeries[:i].mean()
        else:
            start = i - Window
            ma_rs1_series[i] = ValTimeSeries[start:i].mean()

    return ma_rs1_series


def moving_average_flags(MaTimeSeries, UTL, LTL):
    """
    Create a time series of moving average flags:
    1 = "Out"
    0 = "In"
    
    In: TimeSeries of moving average values
    Out: TimeSeries of 0 or 1 digits representing in and out respectively. 
    """
    
    ma_flag_series = MaTimeSeries.copy(deep=True)
    for i in range(len(MaTimeSeries)):

        if LTL <= MaTimeSeries[i] <= UTL:
            # in = 0
            ma_flag_series[i] = 0
        else: 
            # out = 1
            ma_flag_series[i] = 1
    return ma_flag_series


def moving_avg_performance_metrics(ma_perf_model, moving_avg_flag_series, qc_flag_series):
    """
    Takes flags from Moving Averages and QC and compares to get performance metrics
    
    Input: MA and QC flag timeseries'
    Output: Class object of: TP, FP, TN, FN, Precision, Recall
    """

    rep_perf_data = ReplicatePerformanceModel()
    
    # set replicate parameters
    rep_perf_data.ma_window = WINDOW
    rep_perf_data.ma_utl = UTL
    rep_perf_data.ma_ltl = LTL
    rep_perf_data.ma_url = URefL
    rep_perf_data.ma_lrl = LRefL
    rep_perf_data.ma_window = WINDOW
    
    # set counts to zero
    rep_perf_data.true_positive = 0
    rep_perf_data.false_positive = 0
    rep_perf_data.true_negative = 0
    rep_perf_data.false_negative = 0

    # TODO: Need to seperate logic for high and low MA flags
    # loop through all MA flags and compare to QC flags
    for i in range(len(moving_avg_flag_series)):

        # instantiate the time stamp of i'th MA_flag
        rep_perf_data.ma_flag_ts = moving_avg_flag_series.index[i]
        

        # Check MovingAverage "In" flags relative to QC
        # i.e. True Negatives and False Negatives
        if moving_avg_flag_series[i] == 0:
            
            # instantiate startQcLookup variable with i'th MA_flag
            startQcLookup = moving_avg_flag_series.index[i]
            
            for qc in qc_flag_series[startQcLookup:]:

#                 print (startQcLookup, qc_flag_series.index[0])
                
                rep_perf_data.qc_flag_ts = qc_flag_series[startQcLookup:].index[0]

                if qc == 0:
                    # 'True Negative'
                    rep_perf_data.true_negative+=1
                else:
                    # ma_flag = 0 & qc_flag = 1
                    # 'False Negative'
                    rep_perf_data.false_negative+=1

        # Check MovingAverage "Out" flags relative to QC
        # i.e. True Positives and False Positives
        else:
            startQcLookup = moving_avg_flag_series.index[i]
            for qc in qc_flag_series[startQcLookup:]:
                
                # add QC_Flag TimeStamp to MovingAvgPerformanceMetrics
                rep_perf_data.qc_flag_ts = qc_flag_series[startQcLookup:].index[0]
                
                if qc == 1:
                    # 'True Positive'
                    rep_perf_data.true_positive+=1
                else:
                    # ma_flag = 0 & qc_flag = 1
                    # 'False Positive'
                    rep_perf_data.false_positive+=1
                break
    
    # Calculate difference in time between QC flag and MA flag
    rep_perf_data.ma_qc_diff_secs = rep_perf_data.calculate_timestamp_diff()
    rep_perf_data.recall = rep_perf_data.calculate_recall()
    rep_perf_data.precision = rep_perf_data.calculate_precision()
    rep_perf_data.number_of_ma_flags = rep_perf_data.calculate_number_of_flags()
    
    return rep_perf_data

def set_ma_experiment(component, method, ma_type, qc_rules):
    
    ma = MovingAvgExperimentModel()
    
    ma.component = component
    ma.component_method = method
    ma.ma_type = ma_type
    ma.qc_rules = qc_rules

    
    return ma