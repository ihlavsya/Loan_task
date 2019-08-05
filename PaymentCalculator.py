import numpy as np
import utilities as ut
from datetime import datetime

class PaymentCalculator():
    
    def __init__(self, records):
        self.records = records
        self.standard_monthly_payment_rate = 1e-4
        self.mortality_correc_for_payment_rate_male = 1.01
        self.mortality_correc_for_payment_rate_female = 0.99
        self.floating_limit = 700000
        self.standard_deviation_for_floating_rate = np.arange(0.01, 0.1, 0.01)
        self.valuation_date = datetime(2019, 1, 31)
        self.projections = {}
        
        self._calculate_payments()
        
        
    def _get_projection_step(self, current_loan, user_id, gender, id_program, standart_rate):     
        payment = self._get_payment(standart_rate, current_loan, gender)
        projection = current_loan + payment
        return projection
    
    
    def get_projections(self):
        return self.projections
    
    
    def _get_projections(self, record):
        first_loan = record['loans'][record['id_program']]
        overall_loan = np.sum(record['loans'])
        exp_tuple = record['exp_date']
        exp_date = datetime(exp_tuple['year'], exp_tuple['month'], exp_tuple['day'])
        
        projections_count = ut.diff_month(exp_date, self.valuation_date)
        projections = np.zeros(projections_count + 1, dtype = float)
        
        standart_rate = self._get_standart_rate(record['user_id'], record['id_program'], overall_loan)
        
        projections[0] = self._get_projection_step(first_loan, record['user_id'], record['gender'], 
                   record['id_program'], standart_rate)
        
        if projections_count == 1:
            return projections
        
        for i in range(1, projections_count + 1):
            prev_projection = projections[i-1]
            projections[i] = self._get_projection_step(prev_projection, record['user_id'], record['gender'], 
                   record['id_program'], standart_rate)
        
        return projections
            
      
    def _get_payment(self, standart_rate, current_loan, gender):
        mortality_correc = self.mortality_correc_for_payment_rate_female
        if gender == 1:
            mortality_correc = self.mortality_correc_for_payment_rate_male
        
        payment = current_loan * mortality_correc * standart_rate
        return payment
    
            
    def _get_standart_rate(self, user_id, id_program, overall_loan):
        standart_rate = self.standard_monthly_payment_rate
        
        if overall_loan > self.floating_limit:
            np.random.seed(user_id)
            mu = self.standard_monthly_payment_rate
            sigma = self.standard_deviation_for_floating_rate[id_program]
            standart_rate = np.random.lognormal(mu, sigma)
        
        return standart_rate

        
    def _calculate_payments(self):
        for i in range(len(self.records)):
            self.projections[i] = []
            record = self.records[i]
            self.projections[i] = {record['id_program']: self._get_projections(record)}
                

if __name__ == '__main__':
    
    records = np.load('MappedInputData_201908_13_20190805004427.npy', allow_pickle=True)
    pc = PaymentCalculator(records)
    res = pc.get_projections()
    print(res[0:2, 0:2])
                
                