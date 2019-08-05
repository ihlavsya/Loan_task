import numpy as np
import pandas as pd
from datetime import datetime
import utilities as ut


class DataValidator():
    
    def __init__(self, data_frame, threshold=10):
        self.df = data_frame
        self.threshold = threshold
        self._filter_users()
        self._create_programs()
        self._create_data_types()
        self._convert_to_array()

    
    def _create_data_types(self):
        self.date_type = np.dtype([
                ('year', np.int16),
                ('month', np.int8),
                ('day', np.int8)
        ])
    
        self.dtype = np.dtype([
            ('user_id', np.int16),
            ('gender', np.int0),
            ('exp_date', self.date_type),
            ('id_program', np.int8),
            ('loans', np.ndarray),
        ])
     
        
    def _filter_users(self):
        filter_mask = self.df.groupby('id_person')['id_person'].transform('size') > self.threshold
        self.invalid_user_list = self.df[filter_mask]
        self.df = self.df[filter_mask!=True]
        
        
    def _convert_to_custom_date(self, date_str):
        custom_date = np.empty(1, dtype = self.date_type)
        datetime_object = datetime.strptime(date_str, '%m/%y')
        custom_date['year'] = datetime_object.year
        custom_date['month'] = datetime_object.month
        custom_date['day'] = ut.get_last_day_of_month(datetime_object.year, datetime_object.month)
        return custom_date    
    
    
    def _fill_in_loans(self, user_id):
        loans = np.empty(10, dtype = np.float64)
        for i in range(len(loans)):
            mask = (self.df['id_person'] == user_id) & (self.df['id_program'] == i)
            loans[i] = 0
            if len(self.df[mask].index) > 0:
                loans[i] = self.df[mask]['total_loan_per_program'].head(1)
            
        return loans
    
        
    def _convert_to_array(self):
        self.df['gender'] = self.df['gender'].apply(lambda x: 0 if x == 'F' else 1)
        self.records = np.empty(len(self.df.index), dtype = self.dtype)
        
        for (_, row), i in zip(enumerate(self.df.itertuples(), 1), range(len(self.records))):
            self.records[i]['user_id'] = row.id_person
            self.records[i]['id_program'] = row.id_program
            self.records[i]['gender'] = row.gender
            self.records[i]['exp_date'] = self._convert_to_custom_date(row.credit_card_exp_date)
            self.records[i]['loans'] = self._fill_in_loans(row.id_person)
            
            
    def get_mapped_data(self):
        return self.records
    
        
    def _create_programs(self):
        self.df['id_program'] = self.df['credit_card_num'].apply(ut.convert_card_to_digit)
        self.df['total_loan_per_program'] = self.df.groupby(['id_person', 'id_program'], sort=False)["loan"].transform('sum')
        

if __name__ == '__main__':
    readed_data = pd.read_csv('InputData_201908_13_20190805004427')
    data_validator = DataValidator(readed_data)