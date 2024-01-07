from src.backtest.backtest import BacktestDerivatives
from src.strategy.market_making import NaiveMM
from utils.loading_file import load_csv

class Pipeline():
    def __init__(self, opts):
        self.opts = opts
        self.model = NaiveMM(opts['ALGO']['params'])
        self.train_data = load_csv(opts['DATASET']['TRAIN']['csv_file']).to_numpy()
        self.val_data = load_csv(opts['DATASET']['VAL']['csv_file']).to_numpy()

    def fit(self):
        self.model.fit(self.train_data)
        # self.model.save_model(self.opts['opts']['save_dir'])

    def backtest(self):
        backtest_service = BacktestDerivatives(self.opts['opts'])
        
        
        rs = backtest_service.run_from_csv(self.opts['DATASET']['VAL']['csv_file'])
        backtest_service.save_visualize_chart(self.opts['opts']['save_dir'])